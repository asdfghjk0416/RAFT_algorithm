import heartbeat
import threading
import socket
import json
import traceback



def send(message):
    sender = "Leader"
    target = "Node1"
    port = 5555

    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    skt.bind((sender, port))
    

    try:
    # Encoding and sending the message
        skt.sendto(json.dumps(message).encode('utf-8'), (target, port))
    except:
    #  socket.gaierror: [Errno -3] would be thrown if target IP container does not exist or exits, write your listener
        print(f"ERROR WHILE SENDING REQUEST ACROSS : {traceback.format_exc()}")

        
def _send_heart_beat(self):
    message = heartbeat.AppendEntryMessage(1, [], -1, -1)
    t1 = threading.Thread(target=send)