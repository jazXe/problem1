# machine2_receiver.py
import socket, json, logging
from datetime import datetime, timezone
logging.basicConfig(
   filename='machine2.log',
   level=logging.INFO,
   format='%(asctime)s %(message)s',
   datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
)
HOST = ''
PORT = 2000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"[Machine2] Listening on UDP port {PORT}...")
while True:
   data, addr = sock.recvfrom(1024)
   recv_time = datetime.now(timezone.utc)
   msg = json.loads(data.decode())
   send_time = datetime.fromisoformat(msg['send_time'])
   delay = (recv_time - send_time).total_seconds()
   log_line = (
       f"Received from {addr}: delay={delay:.6f}s, "
       f"send_time={send_time}, recv_time={recv_time}"
   )
   print("[Machine2]", log_line)
   logging.info(log_line)
