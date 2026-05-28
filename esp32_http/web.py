import gc
import re
import os, sys
from pdc import PdcSingleton as PDC
from flowpy.simplelogger import SimpleLogger
logger = SimpleLogger(path=__name__ + '.log', level='DEBUG')
try:
    import uasyncio as asyncio
except Exception:
    import asyncio

# internal synchronization for pattern changes
_pattern_lock = None
_pattern_in_progress = False

if sys.platform == 'esp32':
    cwd = os.getcwd()
else:
    from env import HOME
    cwd = HOME

url_pat = re.compile(
    r'^(([^:/\\?#]+):)?' +  # scheme                # NOQA
    r'//([^/\\?#]*)?' +     # user:pass@host:port   # NOQA
    r'([^\\?#]*)' +         # route                 # NOQA
    r'(\\?([^#]*))?' +      # query                 # NOQA
    r'(#(.*))?')            # fragment              # NOQA


def route(file):
    file = cwd + file
    async def _func(writer):
        await send_file(writer, file)

    return _func


async def send_file(writer, file):
    fstat = os.stat(file)
    fsize = fstat[6]

    if file.endswith('.css'):
        ctype = b'text/css'
    elif file.endswith('.js'):
        ctype = b'application/javascript'
    else:
        ctype = b'text/html'

    header = (
        b'HTTP/1.0 200 OK\r\n'
        b'Content-Type: ' + ctype + b'\r\n' +
        ('Content-Length: {}\r\n'.format(fsize)).encode('utf-8') +
        b'\r\n'
    )
    writer.write(header)
    await writer.drain()

    with open(file, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
            gc.collect()

    writer.close()
    await writer.wait_closed()
    gc.collect()


async def set_pattern(pat):
    pdc = PDC()
    pat_name = pat
    # Confirmation for non-status request
    print("SETTING: ", pat_name)
    # schedule the potentially blocking pattern change in background
    async def _apply_pattern_in_background(name):
        global _pattern_lock, _pattern_in_progress
        try:
            # ensure we have a lock object
            if _pattern_lock is None:
                try:
                    _pattern_lock = asyncio.Lock()
                except Exception:
                    _pattern_lock = None

            logger.debug(f"Background pattern change requested: {name}")
            if _pattern_lock is not None:
                async with _pattern_lock:
                    _pattern_in_progress = True
                    logger.debug(f"Starting pattern change: {name}")
                    pd = PDC()
                    ok = pd.board.set_pattern(name)
                    if ok:
                        try:
                            pd.set_current_pattern(name)
                        except Exception:
                            pass
                    else:
                        logger.error(f"Failed to set pattern (background): {name}")
                    _pattern_in_progress = False
                    logger.debug(f"Finished pattern change: {name}")
            else:
                # no lock available: perform directly but still mark progress
                _pattern_in_progress = True
                logger.debug(f"Starting pattern change (no-lock): {name}")
                pd = PDC()
                ok = pd.board.set_pattern(name)
                if ok:
                    try:
                        pd.set_current_pattern(name)
                    except Exception:
                        pass
                else:
                    logger.error(f"Failed to set pattern (background no-lock): {name}")
                _pattern_in_progress = False
                logger.debug(f"Finished pattern change (no-lock): {name}")
        except Exception as e:
            _pattern_in_progress = False
            logger.error(f"Exception in background set_pattern: {e}")

    try:
        # create_task requires a running loop; this handler is async so it normally is
        asyncio.create_task(_apply_pattern_in_background(pat_name))
    except Exception:
        # fallback: run synchronously if create_task not available
        try:
            pdc.board.set_pattern(pat_name)
            pdc.set_current_pattern(pat_name)
        except Exception as e:
            logger.error(f"set_pattern fallback failed: {e}")
    # return success immediately to the HTTP client
    return True

async def set_velo(item):
    velo = int(item)
    """
    if velo < 80:
        velo = 2 * velo
    if velo > 180:
        velo = velo / 2
    """
    # Confirmation for non-status request
    print("velo", velo)
    pdc = PDC()
    pdc.sleep_ms = int(60000 / velo)
    pdc.current_bpm = velo
    return True

async def set_track(item):
    track_id = int(item)
    pdc = PDC()
    # Setze den Track direkt am Board-Objekt
    if hasattr(pdc, 'board') and hasattr(pdc.board, 'track'):
        pdc.board.track.set_track(track_id)
        pdc.set_current_track(track_id)
        # Confirmation for non-status request
        print(f"Track wurde auf {track_id} umgestellt.")
    else:
        logger.error("Fehler: pdc.board oder pdc.board.track nicht gefunden!")
    return True

async def get_status(writer):
    import json
    pdc = PDC()
    bpm = getattr(pdc, 'current_bpm', None)
    if bpm is None and hasattr(pdc, 'sleep_ms') and pdc.sleep_ms > 0:
        bpm = round(60000 / pdc.sleep_ms)
    data = {
        'track':   getattr(pdc, 'current_track',   None),
        'bpm':     bpm,
        'pattern': getattr(pdc, 'current_pattern', None),
        'pattern_busy': _pattern_in_progress,
    }
    body = json.dumps(data).encode('utf-8')
    response = (
        b'HTTP/1.0 200 OK\r\n'
        b'Content-Type: application/json\r\n'
        + ('Content-Length: {}\r\n'.format(len(body))).encode('utf-8') +
        b'\r\n'
        + body
    )
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


routes = {
    '/':              route('/www/page.htm'),
    '/www/style.css': route('/www/style.css'),
    '/status':        get_status,
    '/patterns':      None,  # placeholder, will be set below
}
rpat = {
    r'/pat/(.*)':   set_pattern,
    r'/bpm/(.*)':   set_velo,
    r'/track/(.*)': set_track,
}


async def get_patterns(writer):
    """Return available pattern names as JSON array."""
    import json
    pdc = PDC()
    patterns = []
    try:
        if hasattr(pdc, 'board') and hasattr(pdc.board, 'total_pattern_list'):
            patterns = list(pdc.board.total_pattern_list() or [])
        else:
            # fallback: try to inspect DisplayBase if present
            try:
                from lib.DisplayBase_uP import DisplayBase
                patterns = list(getattr(DisplayBase, 'pattern_list', []) or [])
            except Exception:
                patterns = []
    except Exception:
        patterns = []

    body = json.dumps(patterns).encode('utf-8')
    response = (
        b'HTTP/1.0 200 OK\r\n'
        b'Content-Type: application/json\r\n' +
        ("Content-Length: {}\r\n".format(len(body))).encode('utf-8') +
        b'\r\n' + body
    )
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# set route now that get_patterns is defined
routes['/patterns'] = get_patterns

async def parse_route(route, writer):
    if route in routes:
        await routes[route](writer)
        return True
    else:
        for p in rpat:
            m = re.match(p, route)
            if m:
                # Confirmation for non-status request
                await rpat[p](m.group(1))
                # AJAX-Aufruf: 200 OK mit leerem Body reicht aus
                response = b'HTTP/1.0 200 OK\r\nContent-Length: 0\r\n\r\n'
                writer.write(response)
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return True

    return False

async def not_found(writer):
    response = b'HTTP/1.0 404 Not Found\r\n\r\n'
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    #gc.collect()

async def http_server(reader, writer):
    req = await reader.readline()
    if req == b"" or req == b"\r\n":
        writer.close()
        await writer.wait_closed()
        return

    method, uri, proto = req.split(b" ")
    try:
        # Extrahiere den Pfad robust, unabhängig von Query-String
        route = uri.decode().split('?', 1)[0]
    except Exception as e:
        logger.error(f"Fehler beim Parsen der URI: {e}")
        response = b'HTTP/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nUngueltige Anfrage.'
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    while True:
        h = await reader.readline()
        if h == b"" or h == b"\r\n":
            break
        #print(h)
    #print("route: {}".format(route))

    suc = await parse_route(route, writer)

    if not suc:
        await not_found(writer)

    gc.collect()
