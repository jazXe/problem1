# machine1_client.py
import socket, json, logging
from datetime import datetime, timezone, timedelta
logging.basicConfig(
   filename='machine1.log',
   level=logging.INFO,
   format='%(asctime)s %(message)s',
   datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
)
# CONFIG
SERVER_IP = '192.168.1.100'     # NTP server IP
NTP_PORT = 12345
MACHINE2_IP = '192.168.1.101'   # Machine 2 IP
MACHINE2_PORT = 2000
LOCAL_PORT = 1000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))
# Step 1: Contact NTP mimic server
ntp_msg = json.dumps({"request": "time"}).encode()
sock.sendto(ntp_msg, (SERVER_IP, NTP_PORT))
data, _ = sock.recvfrom(1024)
ntp_reply = json.loads(data.decode())
ntp_server_time = datetime.fromisoformat(ntp_reply["server_time"])
# Step 2: Simulate clock drift (+3s)
local_fake_time = datetime.now(timezone.utc) + timedelta(seconds=3)
# Step 3: Send message to Machine 2
payload = json.dumps({
   "msg": "Hello from Machine 1",
   "send_time": local_fake_time.isoformat(),
   "ntp_time": ntp_server_time.isoformat()
}).encode()
sock.sendto(payload, (MACHINE2_IP, MACHINE2_PORT))
print(f"[Machine1] Sent message at fake_time={local_fake_time}, ntp_time={ntp_server_time}")
logging.info(f"Sent message to Machine2 at fake_time={local_fake_time}, NTP={ntp_server_time}")
sock.close()
