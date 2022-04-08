import socket
import threading
import os
from heartbeat import AppendEntryMessage, RequestVoteRPC
import heartbeat
import nodes
import json
import random
import time
import traceback

# persistent data
voted_for = None
# global which_term
which_term = 0
Log = []
AllNodes = ["node1", "node2", "node3", "node4", "node5"]
thisNode = os.environ["node"]
AllNodes.remove(thisNode)
global state
state = "follower"
global votes_receieved
votes_receieved = 0



# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(skt):
    print("leader is executed")
    msg = AppendEntryMessage(thisNode, which_term)

    for x in AllNodes:
        skt.sendto(msg, (x, 5555))


def send_vote_request(skt):

    voteReq = RequestVoteRPC(which_term, thisNode)
    for x in AllNodes:
        skt.sendto(voteReq, (x, 5555))





def listener(skt: socket):
    state = "follower"
    global endOfTimeout, which_term, votes_receieved
    while True:
        t = random.uniform(100, 500)
        skt.settimeout(t)
        timeNow = time.monotonic()
        try:
            (msg, addr) = skt.recvfrom(1024)
            print("here1")
            StrVal = msg.decode("utf-8")
            JsonVal = json.loads(StrVal)

        except:
            print("timeout")

            if state == "follower":
                print("here4")
                which_term += 1
                state = "candidate"
                votes_receieved += 1
                threading.Thread(target=send_vote_request, args=[skt]).start()
                # request vote from other nodes
            else:
                print("state is: ", state, timeNow)
                # possible issue that the value keeps reseting everytime it doesn't recieve a heartbeat, essentially pushing the timedout val later andlater
                # timeout = random.uniform(100, 500)
                # endOfTimeout += timeout
                # endOfTimeout = time.monotonic() + timeout

    # start election if timeout reached


if __name__ == "__main__":

    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  
    # Bind the node to sender ip and port
    skt.bind((thisNode, 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)
