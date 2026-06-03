try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import json
from app.core.logger import log
class WebServer:
    def __init__(self, get_pattern_cb, set_pattern_cb, get_patterns_cb, get_playlists_cb, set_playlist_cb, get_layouts_cb, set_layout_cb, get_current_layout_cb, set_speed_cb, start_cb, stop_cb, get_running_cb, get_pins_status_cb=None, set_pin_cb=None, save_pins_cb=None, clone_layout_cb=None):
        self.get_pattern = get_pattern_cb
        self.set_pattern = set_pattern_cb
        self.get_patterns = get_patterns_cb
        self.get_playlists = get_playlists_cb
        self.set_playlist = set_playlist_cb
        self.get_layouts = get_layouts_cb
        self.set_layout = set_layout_cb
        self.get_current_layout = get_current_layout_cb
        self.set_speed = set_speed_cb
        self.start_playback = start_cb
        self.stop_playback = stop_cb
        self.get_running = get_running_cb
        self.get_pins_status = get_pins_status_cb
        self.set_pin = set_pin_cb
        self.save_pins = save_pins_cb
        self.clone_layout = clone_layout_cb

    def _parse_query(self, path):
        params = {}
        if '?' not in path:
            return params
        query = path.split('?', 1)[1]
        for param in query.split('&'):
            if not param:
                continue
            if '=' in param:
                key, value = param.split('=', 1)
            else:
                key, value = param, ''
            # Minimal-Decode fuer Browser-Querys.
            params[key] = value.replace('+', ' ').replace('%20', ' ')
        return params

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
            route_path = path.split('?', 1)[0]
            query = self._parse_query(path)
            if route_path != '/':
                route_path = route_path.rstrip('/')
            # Header überspringen (schont Arbeitsspeicher)
            while True:
                line = await reader.readline()
                if not line or line == b'\r\n':
                    break
            log.debug(f"WEB: {method} {path}")

            if route_path == '/':
                # Angepasst: Dynamischer Basispfad statt Hardcode
                await self.serve_file(writer, 'app/web/static/index.html', 'text/html')
            elif route_path == '/pins':
                await self.serve_file(writer, 'app/web/static/pins.html', 'text/html')
            elif route_path.startswith('/static/'):
                filename = route_path.replace('/static/', '')
                filepath = f"app/web/static/{filename}"
                ext = filename.split('.')[-1]
                mime = {"css": "text/css", "js": "application/javascript"}.get(ext, "text/plain")
                await self.serve_file(writer, filepath, mime)
            elif route_path == '/api/status':
                await self.handle_status(writer)
            elif route_path == '/api/pattern':
                name = query.get('name', '')
                await self.handle_set_pattern(writer, name)
            elif route_path == '/api/playlist':
                name = query.get('name', '')
                await self.handle_set_playlist(writer, name)
            elif route_path == '/api/layout':
                name = query.get('name', '')
                await self.handle_set_layout(writer, name)
            elif route_path == '/api/speed':
                val = query.get('val', '')
                await self.handle_set_speed(writer, val)
            elif route_path == '/api/start':
                await self.handle_start(writer)
            elif route_path == '/api/stop':
                await self.handle_stop(writer)
            elif route_path == '/api/pins/status':
                await self.handle_pins_status(writer)
            elif route_path == '/api/pins/set':
                await self.handle_pins_set(
                    writer,
                    query.get('layout', ''),
                    query.get('panel', ''),
                    query.get('slot', ''),
                    query.get('pin', ''),
                )
            elif route_path == '/api/pins/save':
                await self.handle_pins_save(writer, query.get('layout', ''))
            elif route_path == '/api/pins/clone':
                await self.handle_pins_clone(writer, query.get('src', ''), query.get('dst', ''))
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
        writer.write(b"Cache-Control: no-store, no-cache, must-revalidate\r\n")
        writer.write(b"Pragma: no-cache\r\n")
        writer.write(b"Expires: 0\r\n")
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
            "current_layout": self.get_current_layout(),
            "is_running": self.get_running()
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

    async def handle_start(self, writer):
        if self.start_playback():
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Start failed"}')

    async def handle_stop(self, writer):
        if self.stop_playback():
            await self.send_response(writer, 200, "application/json", '{"success": true}')
        else:
            await self.send_response(writer, 400, "application/json", '{"error": "Stop failed"}')

    async def handle_pins_status(self, writer):
        if not self.get_pins_status:
            await self.send_response(writer, 404, "application/json", '{"error": "Pins API not configured"}')
            return
        status = self.get_pins_status()
        await self.send_response(writer, 200, "application/json", json.dumps(status))

    async def handle_pins_set(self, writer, layout_name, panel_index, slot_index, pin):
        if not self.set_pin:
            await self.send_response(writer, 404, "application/json", '{"error": "Pins API not configured"}')
            return
        if not layout_name or not panel_index or not slot_index or not pin:
            await self.send_response(writer, 400, "application/json", '{"error": "layout, panel, slot and pin are required"}')
            return

        ok, message = self.set_pin(layout_name, panel_index, slot_index, pin)
        if ok:
            await self.send_response(writer, 200, "application/json", json.dumps({"success": True, "message": message}))
        else:
            await self.send_response(writer, 400, "application/json", json.dumps({"error": message}))

    async def handle_pins_save(self, writer, layout_name):
        if not self.save_pins:
            await self.send_response(writer, 404, "application/json", '{"error": "Pins API not configured"}')
            return
        if not layout_name:
            await self.send_response(writer, 400, "application/json", '{"error": "layout is required"}')
            return

        ok, message = self.save_pins(layout_name)
        if ok:
            await self.send_response(writer, 200, "application/json", json.dumps({"success": True, "message": message}))
        else:
            await self.send_response(writer, 400, "application/json", json.dumps({"error": message}))

    async def handle_pins_clone(self, writer, source_name, target_name):
        if not self.clone_layout:
            await self.send_response(writer, 404, "application/json", '{"error": "Pins API not configured"}')
            return
        if not source_name or not target_name:
            await self.send_response(writer, 400, "application/json", '{"error": "src and dst are required"}')
            return

        ok, message = self.clone_layout(source_name, target_name)
        if ok:
            await self.send_response(writer, 200, "application/json", json.dumps({"success": True, "message": message}))
        else:
            await self.send_response(writer, 400, "application/json", json.dumps({"error": message}))

    async def start(self, port=8080):
        log.info(f"Starting webserver on 0.0.0.0:{port}")
        await asyncio.start_server(self.handle_client, "0.0.0.0", port)
