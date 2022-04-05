import socket
import threading
import os
from Node.heartbeat import AppendEntryMessage
import heartbeat
import nodes
import json
#persistent data
voted_for = None
which_term = 0
Log =[]
node1 = nodes.nodes[0].name




# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(name):
    msg = AppendEntryMessage({ "leaderId": name,"Entries":[],"prevLogIndex":-1,"prevLogTerm":-1})
    # need to figure out how to send info to other threads 
    for x in nodes.nodes:
         if x.name != name:
            skt.sendto(json.dumps(msg).encode('utf-8'), (x))


if __name__ =='__main__':
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    skt.bind((node1, 5555))


