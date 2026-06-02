try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import json
from app.core.logger import log
class WebServer:
    def __init__(self, get_pattern_cb, set_pattern_cb, get_patterns_cb, get_playlists_cb, set_playlist_cb, get_layouts_cb, set_layout_cb, get_current_layout_cb, set_speed_cb):
        self.get_pattern = get_pattern_cb
        self.set_pattern = set_pattern_cb
        self.get_patterns = get_patterns_cb
        self.get_playlists = get_playlists_cb
        self.set_playlist = set_playlist_cb
        self.get_layouts = get_layouts_cb
        self.set_layout = set_layout_cb
        self.get_current_layout = get_current_layout_cb
        self.set_speed = set_speed_cb
    async def handle_client(self, reader, writer):
        try:
            req_line = await reader.readline()
            if not req_line:
                writer.close()
                await writer.wait_closed()
                return
            req = req_line.decode('utf-8').strip().split()
            if len(req) < 2:
                writer.close()
                await writer.wait_closed()
                return
            method, path = req[0], req[1]
            # Header überspringen (schont Arbeitsspeicher)
            while True:
                line = await reader.readline()
                if not line or line == b'\r\n':
                    break
            log.debug(f"WEB: {method} {path}")

            if path == '/':
                # Angepasst: Dynamischer Basispfad statt Hardcode
                await self.serve_file(writer, 'app/web/static/index.html', 'text/html')
            elif path.startswith('/static/'):
                filename = path.replace('/static/', '')
                filepath = f"app/web/static/{filename}"
                ext = filename.split('.')[-1]
                mime = {"css": "text/css", "js": "application/javascript"}.get(ext, "text/plain")
                await self.serve_file(writer, filepath, mime)
            elif path == '/api/status':
                await self.handle_status(writer)
            elif path.startswith('/api/pattern'):
                name = ""
                if '?' in path:
                    query = path.split('?')[1]
                    for param in query.split('&'):
                        if param.startswith('name='):
                            name = param.split('=')[1]
                await self.handle_set_pattern(writer, name)
            elif path.startswith('/api/playlist'):
                name = ""
                if '?' in path:
                    query = path.split('?')[1]
                    for param in query.split('&'):
                        if param.startswith('name='):
                            name = param.split('=')[1]
                await self.handle_set_playlist(writer, name)
            elif path.startswith('/api/layout'):
                name = ""
                if '?' in path:
                    query = path.split('?')[1]
                    for param in query.split('&'):
                        if param.startswith('name='):
                            name = param.split('=')[1]
                await self.handle_set_layout(writer, name)
            elif path.startswith('/api/speed'):
                val = ""
                if '?' in path:
                    query = path.split('?')[1]
                    for param in query.split('&'):
                        if param.startswith('val='):
                            val = param.split('=')[1]
                await self.handle_set_speed(writer, val)
            else:
                await self.send_response(writer, 404, "text/plain", "Not Found")
        except Exception as e:
            log.error(f"Webserver Error: {e}")
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
    async def serve_file(self, writer, filepath, content_type):
        try:
            # Chunked reading to save RAM on MicroPython!
            await self.send_headers(writer, 200, content_type)
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    writer.write(chunk)
                    await writer.drain()
        except OSError:
            await self.send_response(writer, 404, "text/plain", "File Not Found")
    async def send_headers(self, writer, status_code, content_type):
        status_text = {200: "OK", 400: "Bad Request", 404: "Not Found"}.get(status_code, "Unknown")
        writer.write(f"HTTP/1.1 {status_code} {status_text}\r\n".encode('utf-8'))
        writer.write(f"Content-Type: {content_type}\r\n".encode('utf-8'))
        writer.write(b"Connection: close\r\n\r\n")
        await writer.drain()
    async def send_response(self, writer, status_code, content_type, body):
        await self.send_headers(writer, status_code, content_type)
        writer.write(body.encode('utf-8'))
        await writer.drain()
    async def handle_status(self, writer):
        status = {
            "current_pattern": self.get_pattern(),
            "patterns": self.get_patterns(),
            "playlists": self.get_playlists(),
            "layouts": self.get_layouts(),
            "current_layout": self.get_current_layout()
        }
        await self.send_response(writer, 200, "application/json", json.dumps(status))
    async def handle_set_pattern(self, writer, name):
        if not name:
            await self.send_response(writer, 400, "application/json", '{"error": "Pattern name required"}')
            return
        if self.set_pattern(name):
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Unknown pattern"}')

    async def handle_set_playlist(self, writer, name):
        if not name:
            await self.send_response(writer, 400, "application/json", '{"error": "Playlist name required"}')
            return

        if self.set_playlist(name):
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Unknown playlist"}')

    async def handle_set_layout(self, writer, name):
        if not name:
            await self.send_response(writer, 400, "application/json", '{"error": "Layout name required"}')
            return

        if self.set_layout(name):
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Unknown layout"}')

    async def handle_set_speed(self, writer, val):
        if not val:
            await self.send_response(writer, 400, "application/json", '{"error": "Value required"}')
            return
            
        if self.set_speed(val):
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Invalid speed"}')

    async def start(self, port=8080):
        log.info(f"Starting webserver on 0.0.0.0:{port}")
        await asyncio.start_server(self.handle_client, "0.0.0.0", port)
