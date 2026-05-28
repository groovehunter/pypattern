# Minimaler asyncio-basierter TCP-Server für MicroPython/ESP32
# Lauscht auf Port 8080 und gibt bei jeder Verbindung eine Meldung aus

import uasyncio as asyncio

HOST = '0.0.0.0'
PORT = 8080

async def simple_handler(reader, writer):
    print("[ASYNCIO TEST] Verbindung empfangen!")
    try:
        data = await reader.read(1024)
        print(f"[ASYNCIO TEST] Empfangen: {data}")
        writer.write(b'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from asyncio!')
        await writer.drain()
    except Exception as e:
        print(f"[ASYNCIO TEST] Fehler: {e}")
    finally:
        await writer.wait_closed()

loop = asyncio.get_event_loop()
server = asyncio.start_server(simple_handler, HOST, PORT)
print(f"[ASYNCIO TEST] Starte asyncio-Server auf {HOST}:{PORT}")
loop.run_until_complete(server)
loop.run_forever()

