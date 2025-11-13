# client2.py
import socket, json
from datetime import datetime, timezone, timedelta
import logging
logging.basicConfig(
   filename='client.log',
   level=logging.INFO,
   format='%(asctime)s %(message)s',
   datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
)
SERVER_IP = '192.168.1.100'  # NTP server IP
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# --- Add +3 seconds offset to simulate unsynced clock ---
local_time = datetime.now(timezone.utc) + timedelta(seconds=3)
msg = json.dumps({"request": "time", "client_time": local_time.isoformat()}).encode()
sock.sendto(msg, (SERVER_IP, SERVER_PORT))
data, addr = sock.recvfrom(1024)
resp = json.loads(data.decode())
server_time = datetime.fromisoformat(resp["server_time"])
client_time_sent = datetime.fromisoformat(resp["client_time"])
offset = (server_time - client_time_sent).total_seconds()
logging.info(f"Client_time_sent={client_time_sent}, Server_time={server_time}, Offset={offset:.6f}s")
print(f"Offset: {offset:.6f}s")
sock.close()
