import gc
import re
import os
import sys
from pdc import PdcSingleton as PDC

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
    fstat = os.stat(file)
    fsize = fstat[6]

    writer.write(b'HTTP/1.0 200 OK\r\n')
    writer.write(b'Content-Type: text/html\r\n')
    writer.write('Content-Length: {}\r\n'.format(fsize).encode('utf-8'))
    writer.write(b'Accept-Ranges: none\r\n')
    writer.write(b'Transfer-Encoding: chunked\r\n')
    writer.write(b'\r\n')
    await writer.drain()
    gc.collect()
    max_chunk_size = 1024
    with open(file, 'rb') as f:
        for x in range(0, fsize, max_chunk_size):
            chunk_size = min(max_chunk_size, fsize-x)
            chunk_header = "{:x}\r\n".format(chunk_size).encode('utf-8')
            writer.write(chunk_header)
            writer.write(f.read(chunk_size))
            writer.write(b'\r\n')
            await writer.drain()
            gc.collect()
    writer.write(b"\r\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    gc.collect()

async def config(cfg):
    pdc = PDC()
    wifi = cfg.decode()
    suc = pdc.config(wifi)
    return suc

async def set_pattern(pat):
    pdc = PDC()
    #pdc.init()
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
  loop = uasyncio.get_event_loop()
  loop.close()
  sys.exit()
  return True

routes = {
    b'/': route('/www/page.htm'),
    b'/static/jquery.js': route('/www/jquery-3.5.1.min.js'),
}
rpat = {
    r'/pat/(.*)': set_pattern,
    r'/velo/(.*)': set_velo,
    r'/bpm/(.*)': set_bpm,
    r'/stop/': stop,
    r'/config/': config,
}

async def parse_route(route, writer):
  if route in routes:
    await routes[route](writer)
  else:
    for p in rpat:
      m = re.match(p, route)
      if m:
        print("FOUND urlpattern x with arg y:", p, m.group(1))
        await rpat[p](m.group(1))
        await routes[b'/'](writer)
  return True

async def http_server(reader, writer):
    req = await reader.readline()
    #print(req)
    method, uri, proto = req.split(b" ")
    m = re.match(url_pat, uri)
    route = m.group(5)
    l = None
    while True:
        h = await reader.readline()
        if h == b"" or h == b"\r\n":
            break
        #print(h)
        if 'Content-Length: ' in h:
          try:
            l = int(h[16:-2])
            print ('Content Length is : ', l)
          except:
            continue

    if l :
      postquery = reader.read(l)
      print(postquery)

    print("route: {}".format(route.decode('utf-8')))

    suc = await parse_route(route, writer)

    if not suc:
        writer.write(b'HTTP/1.0 404 Not Found\r\n')
        writer.write(b'\r\n')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    gc.collect()
