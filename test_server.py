# Minimaler TCP-Server für MicroPython/ESP32
# Lauscht auf Port 8080 und gibt bei jeder Verbindung eine Meldung aus

import socket

HOST = '0.0.0.0'  # oder explizit die WLAN-IP, z.B. '192.168.43.10'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print(f"[TEST] TCP-Server läuft auf {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    print(f"[TEST] Verbindung von {addr}")
    try:
        data = conn.recv(1024)
        print(f"[TEST] Empfangen: {data}")
        conn.send(b'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from ESP32!')
    except Exception as e:
        print(f"[TEST] Fehler: {e}")
    finally:
        conn.close()

