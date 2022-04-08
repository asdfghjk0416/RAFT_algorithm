from operator import truediv
import socket
import threading
import os
from heartbeat import AppendEntryMessage, RequestVoteRPC, SendVote
import heartbeat
import nodes
import json
import random
import time
import traceback

# CONVERT_FOLLOWER - convert the node to the follower state
# TIMEOUT - timeout the node immediately
# SHUTDOWN - shutdown all threads running on the node, no errors should be thrown LEADER_INFO - return leader info with key=LEADER and value=Node? which is the
# current leader
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
alive = True

# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(skt):
    msg = AppendEntryMessage(thisNode, which_term)

    while True:
        for x in AllNodes:
            skt.sendto(msg, (x, 5555))


def send_vote_request(skt):

    voteReq = RequestVoteRPC(which_term, thisNode)
    for x in AllNodes:
        skt.sendto(voteReq, (x, 5555))


def send_vote(skt, c):
    msg = SendVote(thisNode)
    skt.sendto(msg, (c, 5555))


def listener(skt: socket):
    state = "follower"
    global endOfTimeout,alive, which_term, votes_receieved, voted_for
    while alive:
        t = random.uniform(1, 5)
        skt.settimeout(t)
        timeNow = time.monotonic()
        try:
            (msg, addr) = skt.recvfrom(1024)
            StrVal = msg.decode("utf-8")
            voteRequest = json.loads(StrVal)
            c = voteRequest["sender_name"]
            if c == "Controller":
            if voteRequest["request"] == "CONVERT_FOLLOWER":
                state = "follower"

            elif voteRequest["request"] == "VOTE_REQUEST":
                if voteRequest["prevLogTerm"] > which_term and voted_for == None:
                    threading.Thread(target=send_vote, args=[skt, c]).start()
                    which_term += 1
            elif voteRequest["request"] == "VOTE_ACK":
                votes_receieved += 1
                if votes_receieved >= 3:
                    state = "leader"
                    print(thisNode, " has become a leader.")
                    threading.Thread(target=send_heartbeat, args=[skt]).start()

            elif voteRequest["request"] == "APPEND_RPC":
                pass
            elif voteRequest["request"] == "TIMEOUT":
                break
            elif voteRequest["request"] == "SHUTDOWN":
                
                alive = False
            else:
                print("")

        except:
            if state == "follower":
                
                which_term += 1
                state = "candidate"
                print(thisNode, " has become a candidate.")
                votes_receieved += 1
                threading.Thread(target=send_vote_request, args=[skt]).start()
                
            else:
                break
               
    print("system shut down.")



if __name__ == "__main__":

    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind the node to sender ip and port
    skt.bind((thisNode, 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)
