from operator import truediv
import socket
import this
import threading
import os
from requests import (
    ShutDown,
    AppendEntryMessage,
    RequestVoteRPC,
    SendVote,
    TimedOut,
    store,
    RetrieveMessage,
)
import nodes
import json
import random
import time
import traceback

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
leaader = ""

# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(skt):
    time.sleep(2)
    msg = AppendEntryMessage(thisNode, which_term)

    while alive:
        for x in AllNodes:
            skt.sendto(msg, (x, 5555))


def send_vote_request(skt):

    voteReq = RequestVoteRPC(which_term, thisNode)
    for x in AllNodes:
        skt.sendto(voteReq, (x, 5555))


def leaderInfo(skt):
    msg = store(thisNode, which_term, leader)
    print(msg)
    skt.sendto(msg, ("Controller", 5555))


def retryRetrieve(skt):
    msg = RetrieveMessage(thisNode, Log)
    for x in AllNodes:
        skt.sendto(msg, (x, 5555))


def retryStore(skt):
    msg = store(thisNode, which_term, leader, "STORE")
    for x in AllNodes:
        skt.sendto(msg, (x, 5555))


def sendCommittedLogs(skt):
    msg = RetrieveMessage(thisNode, Log)
    print("SENDING COMMITTED LOGS TO THE CONTROLLER")
    skt.sendto(msg, ("Controller", 5555))


def send_vote(skt, c):
    msg = SendVote(thisNode)
    skt.sendto(msg, (c, 5555))
    print(thisNode, f" voted for {c}")


def shutdown(skt):
    msg = ShutDown(thisNode)
    for x in AllNodes:
        skt.sendto(msg, (x, 5555))


def timeout(skt):
    msg = TimedOut(thisNode)
    for x in AllNodes:
        skt.sendto(msg, (x, 5555))


def listener(skt: socket):
    state = "follower"
    global endOfTimeout, alive, which_term, leader, votes_receieved, voted_for
    while alive:
        t = random.uniform(1, 4)
        skt.settimeout(t)
        timeNow = time.monotonic()

        try:
            (msg, addr) = skt.recvfrom(1024)
            StrVal = msg.decode("utf-8")
            req = json.loads(StrVal)
            sender = req["sender_name"]
            if req["request"] == "SHUTDOWN":
                threading.Thread(target=shutdown, args=[skt]).start()

                # print("alive is false")
                alive = False
            elif req["request"] == "VOTE_REQUEST":
                if req["prevLogTerm"] > which_term and voted_for == None:
                    threading.Thread(target=send_vote, args=[skt, sender]).start()
                    which_term += 1
            elif req["request"] == "TIMEOUT":
                threading.Thread(target=timeout, args=[skt]).start()
                # print("breaking")
                break
            elif req["request"] == "NodeTimeout":
                AllNodes.remove(sender)
            elif req["request"] == "CONVERT_FOLLOWER":
                if state == "follower":
                    print(thisNode, " is already a follower")
                state = "follower"

            elif req["request"] == "VOTE_ACK":
                votes_receieved += 1
                if votes_receieved == 3:
                    state = "leader"
                    print(thisNode, " has become the leader.")
                    print(thisNode, " is sending heartbeats")
                    threading.Thread(target=send_heartbeat, args=[skt]).start()

            elif req["request"] == "APPEND_RPC":
                leader = req["sender_name"]

            elif req["request"] == "LEADER_INFO":
                print("leader=", leader, " log=", Log)

            elif req["request"] == "STORE":
                if state == "leader":
                    print("LEADER IS STORING LOG")
                    info = {
                        "Term": which_term,
                        "Key": msg["key"],
                        "Value": msg["value"],
                    }
                    Log.append(info)
                else:
                    print("not leader")
                    threading.Thread(target=leaderInfo, args=[skt]).start()
                    if req["sender_name"] == "Controller":
                        threading.Thread(target=retryStore, args=[skt]).start()

            elif req["request"] == "RETRIEVE":
                if state == "leader":
                    print("RETRIEVE REQUEST TO THE LEADER")
                    threading.Thread(target=sendCommittedLogs, args=[skt]).start()
                else:
                    print("RETRIEVE REQUEST NOT TO LEADER")
                    threading.Thread(target=leaderInfo, args=[skt]).start()
                    if req["sender_name"] == "Controller":
                        threading.Thread(target=retryRetrieve, args=[skt]).start()

            else:
                print("")

        except:
            if state == "follower":
                which_term += 1
                state = "candidate"
                print(thisNode, "has become a canidate.")
                votes_receieved += 1
                threading.Thread(target=send_vote_request, args=[skt]).start()

            elif state == "leader":
                pass
            else:
                print("breaking in else")
                break

    print(f"{thisNode} has shut down.")


if __name__ == "__main__":

    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind the node to sender ip and port
    skt.bind((thisNode, 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)