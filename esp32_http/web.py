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
    r'(//([^/\\?#]*))?' +   # user:pass@host:port   # NOQA
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

    writer.write(b'HTTP/1.0 200 OK\r\n')
    writer.write(b'Content-Type: text/html\r\n')
    writer.write('Content-Length: {}\r\n'.format(fsize).encode('utf-8'))
    writer.write(b'Accept-Ranges: none\r\n')
    writer.write(b'Transfer-Encoding: chunked\r\n')
    writer.write(b'\r\n')
    await writer.drain()

    #gc.collect()
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


async def set_pattern(pat):
    pdc = PDC()
    #pdc.init()
    pat_name = pat
    print("SETTING: ", pat_name)
    suc = pdc.board.set_pattern(pat_name)
    return suc

async def set_velo(item):
  velo = int(item)
  if not velo:  velo= 5
  print(velo)
  pdc = PDC()
  pdc.velocity = velo
  return True

routes = {
    b'/': route('/www/page.htm'),
    b'/static/jquery.js': route('/www/jquery-3.5.1.min.js'),
    }
rpat = {
    r'/pat/(.*)': set_pattern,
    r'/velo/(.*)': set_velo,
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
                # Nach erfolgreicher Aktion: HTTP-Redirect senden
                writer.write(b'HTTP/1.0 302 Found\r\n')
                writer.write(b'Location: /\r\n')
                writer.write(b'Content-Type: text/html\r\n\r\n')
                writer.write(b'<html><body>Redirecting...</body></html>')
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return True
    return False

async def not_found(writer):
    writer.write(b'HTTP/1.0 404 Not Found\r\n')
    writer.write(b'\r\n')
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    #gc.collect()

async def http_server(reader, writer):
    req = await reader.readline()
    print(req)
    if req is b"":
        writer.close()
        await writer.wait_closed()
        return

    method, uri, proto = req.split(b" ")
    m = re.match(url_pat, uri.decode())
    route = m.group(5)

    while True:
        h = await reader.readline()
        if h == b"" or h == b"\r\n":
            break
        print(h)

    print("route: {}".format(route))

    suc = await parse_route(route, writer)

    if not suc:
        await not_found(writer)

    gc.collect()
