import gc
import re
import os, sys
from pdc import PdcSingleton as PDC

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
    print("SETTING: ", pat_name)
    suc = pdc.board.set_pattern(pat_name)
    #if suc:
    pdc.set_current_pattern(pat_name)
    return suc

async def set_velo(item):
    velo = int(item)
    """
    if velo < 80:
        velo = 2 * velo
    if velo > 180:
        velo = velo / 2
    """
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
        print(f"Track wurde auf {track_id} umgestellt.")
    else:
        print("Fehler: pdc.board oder pdc.board.track nicht gefunden!")
    return True

async def get_status(writer):
    import json
    pdc = PDC()
    bpm = getattr(pdc, 'current_bpm', None)
    if bpm is None and hasattr(pdc, 'sleep_ms') and pdc.sleep_ms > 0:
        bpm = round(60000 / pdc.sleep_ms)
    print(bpm)
    data = {
        'track':   getattr(pdc, 'current_track',   None),
        'bpm':     bpm,
        'pattern': getattr(pdc, 'current_pattern', None),
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
}
rpat = {
    r'/pat/(.*)':   set_pattern,
    r'/bpm/(.*)':   set_velo,
    r'/track/(.*)': set_track,
}

async def parse_route(route, writer):
    if route in routes:
        await routes[route](writer)
        return True
    else:
        for p in rpat:
            m = re.match(p, route)
            if m:
                print("FOUND", m.group(1))
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
    #print("start http_server")
    req = await reader.readline()
    print(req)
    if req == b"" or req == b"\r\n":
        writer.close()
        await writer.wait_closed()
        return

    method, uri, proto = req.split(b" ")
    try:
        # Extrahiere den Pfad robust, unabhängig von Query-String
        route = uri.decode().split('?', 1)[0]
    except Exception as e:
        print(f"Fehler beim Parsen der URI: {e}")
        response = b'HTTP/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nUngültige Anfrage.'
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
