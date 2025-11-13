# ntp_server.py
import socket
from datetime import datetime, timezone
import json
HOST = ''       # Listen on all interfaces
PORT = 12345    # Example NTP-mimic port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"[NTP Server] Listening on UDP port {PORT}...")
while True:
   data, addr = sock.recvfrom(1024)
   recv_time = datetime.now(timezone.utc)
   msg = json.loads(data.decode())
   # Client sends: {"request": "time", "client_time": "..."}
   client_time = datetime.fromisoformat(msg["client_time"])
   server_time = datetime.now(timezone.utc)
   response = json.dumps({
       "server_time": server_time.isoformat(),
       "client_time": msg["client_time"]
   }).encode()
   sock.sendto(response, addr)
   print(f"[Server] Responded to {addr}, server_time={server_time}")
