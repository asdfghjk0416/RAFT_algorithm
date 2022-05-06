from operator import truediv
import socket
import this
import threading
import os
import json
import time
import random

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
    if msg["request"] == "LEADER_INFO":
        leader=msg["value"]
        print(msg)
    


def listener(skt: socket):
    while alive:
        try: 
            (msg, addr) = skt.recvfrom(1024)
            StrVal = msg.decode("utf-8")
            req = json.loads(StrVal)
            sender = req["sender_name"]
            if req["request"] == 'LEADER_INFO':
                threading.Thread(target=leader_info, args=[req,skt].start())
        except:
            print("not receving anyth")





if __name__ == "__main__":
    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind the node to sender ip and port
    skt.bind(('Controller', 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)