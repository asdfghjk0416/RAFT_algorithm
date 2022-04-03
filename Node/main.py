import socket
import threading
import os
from Node.heartbeat import AppendEntryMessage
import heartbeat
import nodes

def send_heartbeat(name):
    msg = AppendEntryMessage({ "leaderId": name,"Entries":[],"prevLogIndex":-1,"prevLogTerm":-1})
    # need to figure out how to send info to other threads 
    # for x in nodes.nodes:
    #     if x.name != name:
    #         print("sedning to follower node")
        
