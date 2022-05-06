from operator import truediv
import socket
import this
import threading
import os
import json
import time
import random
leader = 0

alive = True


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

def leader_info(msg,skt):
    global leader
    if msg["request"] == "LEADER_INFO":
        leader=msg["value"]
        print(msg)
    elif msg["request"] == "RETRIEVE":
        print("retrieve messages: ",msg['value'])
    


def listener(skt: socket):
    print("in listener")
    while alive:
        # try: 
            (msg, addr) = skt.recvfrom(1024)
            print("msg")
            StrVal = msg.decode("utf-8")
            req = json.loads(StrVal)
            sender = req["sender_name"]
            if req["request"] == 'LEADER_INFO':
                threading.Thread(target=leader_info, args=[req,skt]).start()
            
        # except:
        #     print("not receving anyth")

def trySending(skt):
    print("sending")
    global leader
    msg = createmsg(request="STORE",key="4",value="value4")
    print(msg)
    skt.sendto(json.dumps(msg).encode("utf-8"),("node4",5555))
    
    


if __name__ == "__main__":
    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind the node to sender ip and port
    skt.bind(('Controller', 5555))
    print("hi")
    time.sleep(10)
    trySending(skt);

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)