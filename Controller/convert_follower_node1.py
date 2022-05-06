import json
import socket
import traceback
import time
import threading
import random
alive = True
leader =0 

def createmsg(
    sender_name="Controller", request="null", term="null", key="null", value="null"
):
    msg = json.load(open("Message.json"))

    msg["sender_name"] = sender_name
    msg["request"] = request
    msg["term"] = term
    msg["key"] = key
    msg["value"] = value

    return msg


def trySending(msg, target="node4", port=5555, sender="Controller"):

    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    skt.bind((sender, port))
    try:
        # Encoding and sending the message
        skt.sendto(json.dumps(msg).encode("utf-8"), (target, port))
    except:
        #  socket.gaierror: [Errno -3] would be thrown if target IP container does not exist or exits, write your listener
        print(f"ERROR WHILE SENDING REQUEST ACROSS : {traceback.format_exc()}")


# REQUESTS
time.sleep(10)
print("EXECUTING STORE")
msg = createmsg(request="STORE",key="4",value="value4")

print(msg)
trySending(msg=msg)
def receive(msg,skt):
    global leader
    if msg["request"] == "LEADER_INFO":
        leader = msg['value']
        print("leader: ",leader)
        print("leader_info sent back to controller")
        print(msg)

def listener(skt):
    print('starting listener')
    while alive:
        t = random.uniform(1, 4)
        skt.settimeout(t)
        try:
            (msg, addr) = skt.recvfrom(1024)
            # Decoding the Message received from leader
            decoded_msg = json.loads(msg.decode('utf-8'))
            # print(f"Message Received : {decoded_msg} From : {addr}")
            threading.Thread(target=receive, args=[decoded_msg, skt]).start()
        except:
            print("dint receive anyth")




if __name__ == "__main__":

    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind the node to sender ip and port
    skt.bind(('controller', 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)
# time.sleep(5)
# print("EXECUTING RETRIEVE")
# msg1 = createmsg(request="RETRIEVE")
# trySending(msg=msg1)
