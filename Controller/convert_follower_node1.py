
from contextlib import nullcontext
import json
import socket
import traceback
import time

# Wait following seconds below sending the controller request
time.sleep(5)

# Read Message Template
msg = json.load(open("Message.json"))
msg2 = json.load(open("Message.json"))
# Initialize
sender = "Controller"
target = "node4"
port = 5555
msg2['sender_name'] = sender
msg2['term'] = "null"
msg2['request'] = "STORE"
msg2['key'] = "K4"
msg2['value'] = "Value4"

# Request
msg['sender_name'] = sender
msg['request'] = "SHUTDOWN"
print(f"Request Created : {msg}")
 
# Socket Creation and Binding
skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
skt.bind((sender, port))

# Send Message
try:
    # Encoding and sending the message
    skt.sendto(json.dumps(msg).encode('utf-8'), (target, port))
    skt.sendto(json.dumps(msg2).encode('utf-8'), (target,port))
except:
    #  socket.gaierror: [Errno -3] would be thrown if target IP container does not exist or exits, write your listener
    print(f"ERROR WHILE SENDING REQUEST ACROSS : {traceback.format_exc()}")

