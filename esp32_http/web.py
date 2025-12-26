import gc
import socket
import sys
import os

gc.collect()

STATIC_DIR = '/www'
status_message = None

# Hilfsfunktion: Sende statische Datei

def send_file(filename, message=None):
    path = STATIC_DIR + '/' + filename
    try:
        with open(path, 'rb') as f:
            content = f.read().decode('utf-8')
    except OSError:
        return '404 Not Found', 'text/plain', 404
    if filename.endswith('.htm') or filename.endswith('.html'):
        content_type = 'text/html'
    elif filename.endswith('.css'):
        content_type = 'text/css'
    elif filename.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'application/octet-stream'
    if message:
        content = content.replace('<body>', '<body><div class="status-message">{}</div>'.format(message), 1)
    return content, content_type, 200

# Routing: 1 Ebene

def handle_request(path):
    global status_message
    # Root
    if path == '/':
        msg = status_message
        status_message = None
        content, ctype, code = send_file('page.htm', message=msg)
        return code, ctype, content
    # CSS
    elif path == '/css/style.css':
        content, ctype, code = send_file('style.css')
        return code, ctype, content
    # jQuery
    elif path == '/static/jquery.js':
        content, ctype, code = send_file('jquery-3.5.1.min.js')
        return code, ctype, content
    # BPM
    elif path.startswith('/bpm/'):
        try:
            bpm = int(path.split('/')[-1])
            from esp32.pdc import PdcSingleton as PDC
            sl_ms = int(1000 / (bpm / 60))
            pdc = PDC()
            pdc.sleep_ms = sl_ms
            status_message = 'BPM wurde auf {} umgestellt.'.format(bpm)
            return 302, 'text/html', '<meta http-equiv="refresh" content="0; url=/" />'
        except Exception as e:
            return 400, 'text/plain', 'Bad BPM'
    # Pattern
    elif path.startswith('/pat/'):
        try:
            pat = path.split('/')[-1]
            from esp32.pdc import PdcSingleton as PDC
            pdc = PDC()
            pdc.board.set_pattern(pat)
            status_message = 'Pattern wurde auf {} umgestellt.'.format(pat)
            return 302, 'text/html', '<meta http-equiv="refresh" content="0; url=/" />'
        except Exception as e:
            return 400, 'text/plain', 'Bad Pattern'
    # Track
    elif path.startswith('/track/'):
        try:
            track = int(path.split('/')[-1])
            from esp32.pdc import PdcSingleton as PDC
            pdc = PDC()
            pdc.board.track.set_track(track)
            status_message = 'Track wurde auf {} umgestellt.'.format(track)
            return 302, 'text/html', '<meta http-equiv="refresh" content="0; url=/" />'
        except Exception as e:
            return 400, 'text/plain', 'Bad Track'
    # Stop
    elif path == '/stop/':
        status_message = 'Server wurde gestoppt.'
        return 302, 'text/html', '<meta http-equiv="refresh" content="0; url=/" />'
    # Not found
    else:
        return 404, 'text/plain', 'Not found'

# Minimaler HTTP-Server

def http_server(host='0.0.0.0', port=8080):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print('HTTP Server läuft auf {}:{}'.format(host, port))
    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024)
            if not request:
                conn.close()
                continue
            # Request parsen
            try:
                req_line = request.decode().split('\r\n')[0]
                method, path, _ = req_line.split()
            except Exception:
                conn.close()
                continue
            # Nur GET unterstützen
            if method != 'GET':
                conn.send(b'HTTP/1.0 405 Method Not Allowed\r\n\r\n')
                conn.close()
                continue
            code, ctype, content = handle_request(path)
            # Header
            header = 'HTTP/1.0 {}\r\nContent-Type: {}\r\n\r\n'.format(code, ctype)
            conn.send(header.encode())
            if isinstance(content, str):
                conn.send(content.encode())
            else:
                conn.send(content)
            conn.close()
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            continue

# Für Import in main.py
