from platform import node
import socket
import threading
import os
from heartbeat import AppendEntryMessage
import heartbeat
import nodes
import json
import random
import time

#persistent data
voted_for = None
which_term = 0
Log =[]
node1 = nodes.nodes[0].name
global state



# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(skt, name):
    msg = AppendEntryMessage({ "leaderId": name,"Entries":[],"prevLogIndex":-1,"prevLogTerm":-1})

    #  does this need to be an infinite loop
    for x in nodes.nodes:
         if x.name != name:
            skt.sendto(json.dumps(msg).encode('utf-8'), (x))

def listener(skt):
    timeoutBool = False
    global endOfTimeout
    while True:
        try: 
            (val, address)  = skt.recvfrom(1024)
            StrVal = val.decode('utf-8')
            JsonVal = json.loads(StrVal)
            print(JsonVal["leaderId"])
        except:
            if state == "follower" and timeoutBool and time.monotonic() >= endOfTimeout:
                state = "candidate"
                # send to tohers for vote?
            elif state=="candidate" and timeoutBool and time.monotonic() >= endOfTimeout:
                state == "leader"
                # need to send in node id val
                threading.Thread(target=send_heartbeat, args=[skt, "dv"]).start()
            else:
                # possible issue that the value keeps reseting everytime it doesn't recieve a heartbeat, essentially pushing the timedout val later andlater
                timeout = random.uniform(100, 500)
                endOfTimeout += timeout


            # start election if timeout reached




if __name__ =='__main__':
 
    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


    host = '127.0.0.1'
    # Bind the node to sender ip and port
    skt.bind((host, 5555))

    #Starting thread 1
    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)
    


