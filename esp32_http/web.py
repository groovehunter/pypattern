import gc
import re
import os
import sys
# sys.path anpassen, damit das esp32-Modul gefunden wird
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from esp32.pdc import PdcSingleton as PDC

# Kompatibilität für CPython (lokal) und MicroPython (ESP32)
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from flowpy.utils import setup_logger
logger = setup_logger(__name__, __name__)

url_pat = re.compile(
    r'^(([^:/\\?#]+):)?' +  # scheme                # NOQA
    r'(//([^/\\?#]*))?' +   # user:pass@host:port   # NOQA
    r'([^\\?#]*)' +         # route                 # NOQA
    r'(\\?([^#]*))?' +      # query                 # NOQA
    r'(#(.*))?')            # fragment              # NOQA


def route(file):

    async def _func(writer):
        await send_file(writer, file)

    return _func


async def send_file(writer, file):
    logger.debug("file: %s", file)
    try:
        with open(file, 'rb') as f:
            content = f.read()
        fsize = len(content)
    except OSError:
        # Fehlerausgabe bei fehlender Datei
        writer.write(b'HTTP/1.0 404 Not Found\r\n')
        writer.write(b'Content-Type: text/plain\r\n')
        writer.write(b'Content-Length: 0\r\n')
        writer.write(b'Connection: close\r\n')
        writer.write(b'\r\n')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    # Content-Type bestimmen
    if file.endswith('.htm') or file.endswith('.html'):
        content_type = 'text/html'
    elif file.endswith('.css'):
        content_type = 'text/css'
    elif file.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'application/octet-stream'

    # Header senden
    writer.write(b'HTTP/1.1 200 OK\r\n')
    writer.write(f'Content-Type: {content_type}\r\n'.encode('utf-8'))
    writer.write(f'Content-Length: {fsize}\r\n'.encode('utf-8'))
    writer.write(b'Connection: close\r\n')
    writer.write(b'\r\n')
    await writer.drain()
    # Body senden
    # Sende die Datei in kleinen Chunks, um Buffer-Probleme zu vermeiden
    chunk_size = 1024
    for i in range(0, fsize, chunk_size):
        writer.write(content[i:i+chunk_size])
        await writer.drain()
    writer.close()
    await writer.wait_closed()
    gc.collect()

async def config(cfg):
    pdc = PDC()
    wifi = cfg.decode()
    suc = pdc.config(wifi)
    return suc

async def set_track(val):
  pdc = PDC()
  val = int(val.decode())
  suc = pdc.board.track.set_track(val)
  return suc

async def set_pattern(pat):
  pdc = PDC()
  pat_name = pat.decode()
  print("SETTING: ", pat_name)
  suc = pdc.board.set_pattern(pat_name)
  return suc

def set_attr(attr_name, value, default=None):
  if not value:  value = default
  #print(value)
  pdc = PDC()
  setattr(pdc, attr_name, value)

def calc_sleep_ms(bpm):
  bps = bpm / 60
  sl_ms = int(1000 / bps)
  return sl_ms

def middle_bpm(bpm):
  if bpm < 80:
    bpm = bpm * 2
  if bpm > 200:
    bpm = int(bpm/2)
  return bpm

async def set_bpm(value):
  bpm = int(value.decode())
  #bpm = middle_bpm(bpm)
  sl_ms = calc_sleep_ms(bpm)
  pdc = PDC()
  pdc.sleep_ms = sl_ms
  print("sl_ms", sl_ms)
  #set_attr('sleep_ms', sl_ms, default=200)
  return True

async def set_velo(item):
  velo = int(item.decode())
  if not velo:  velo= 5
  #print(velo)
  bpm = velo
  sl_ms = calc_sleep_ms(bpm)
  #print(sl_ms)
  set_attr('sleep_ms', sl_ms, default=200)
  return True


async def stop():
    # Kompatibel für CPython und MicroPython
    try:
        loop = asyncio.get_event_loop()
        loop.close()
    except Exception as e:
        print('Fehler beim Stop:', e)
    # sys.exit() entfernt, da nach loop.close() nicht mehr erreichbar
    return True

# Basisverzeichnis für statische Dateien
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../www'))

# Inline-Handler für die wichtigsten Endpunkte
routes = {
    b'/': lambda writer: send_file(writer, os.path.join(STATIC_DIR, 'page.htm')),
    b'/static/jquery.js': lambda writer: send_file(writer, os.path.join(STATIC_DIR, 'jquery-3.5.1.min.js')),
    b'/css/style.css': lambda writer: send_file(writer, os.path.join(STATIC_DIR, 'style.css')),
}
rpat = {
    r'/pat/(.*)': lambda arg: set_pattern(arg),
    r'/velo/(.*)': lambda arg: set_velo(arg),
    r'/bpm/(.*)': lambda arg: set_bpm(arg),
    r'/track/(.*)': lambda arg: set_track(arg),
    r'/stop/': lambda arg=None: stop(),
    r'/config/': lambda arg: config(arg),
}

async def parse_route(route, writer):
    if route in routes:
        await routes[route](writer)
        return True
    else:
        for p in rpat:
            m = re.match(p, route)
            if m:
                print("FOUND urlpattern x with arg y:", p, m.group(1) if m.lastindex else None)
                await rpat[p](m.group(1) if m.lastindex else None)
                await routes[b'/'](writer)
                return True
        else:
            writer.write(b'HTTP/1.0 404 Not Found\r\n')
            writer.write(b'\r\n')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return False
    gc.collect()

async def http_server(reader, writer):
    req = await reader.readline()
    #print(req)
    method, uri, proto = req.split(b" ")
    print("method, uri, proto", method, uri, proto)
    m = re.match(url_pat, uri.decode())
    route = m.group(5)
    l = None
    while True:
        h = await reader.readline()
        if h == b"" or h == b"\r\n":
            break
        #print(h)
        if b'Content-Length: ' in h:
          try:
            l = int(h[16:-2])
            print ('Content Length is : ', l)
          except:
            continue

    if l :
      postquery = reader.read(l)
      print(postquery)

    print("route: {}".format(route))

    suc = await parse_route(route, writer)

    if not suc:
        writer.write(b'HTTP/1.0 404 Not Found\r\n')
        writer.write(b'\r\n')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    gc.collect()

# Am Ende des Skripts: Serverstart für beide Varianten
if __name__ == '__main__':
    async def main():
        server = await asyncio.start_server(http_server, '127.0.0.1', 8080)
        print('Server läuft auf http://127.0.0.1:8080')
        async with server:
            await server.serve_forever()
    asyncio.run(main())
