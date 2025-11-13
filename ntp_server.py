# ntp_server.py
import socket, json
from datetime import datetime, timezone
HOST = ''        # Listen on all interfaces
PORT = 12345     # NTP mimic port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"[NTP Server] Listening on UDP port {PORT}...")
while True:
   data, addr = sock.recvfrom(1024)
   recv_time = datetime.now(timezone.utc)
   msg = json.loads(data.decode())
   server_time = datetime.now(timezone.utc)
   reply = json.dumps({
       "server_time": server_time.isoformat()
   }).encode()
   sock.sendto(reply, addr)
   print(f"[NTP Server] Replied to {addr} with {server_time}")
