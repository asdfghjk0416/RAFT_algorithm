from email import message
import threading
import json


def TimedOut(timedOutNode):

    f = open("Message.json")

    msg = json.load(f)
    msg["request"] = "NodeTimeout"
    msg["sender_name"] = timedOutNode
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = -1

    return (json.dumps(msg)).encode("utf-8")


def ShutDown(sender):
    f = open("Message.json")

    msg = json.load(f)
    msg["request"] = "SHUTDOWN"
    msg["sender_name"] = sender
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = -1

    return (json.dumps(msg)).encode("utf-8")


# def AppendEntryMessage(leaderId, prevLogTerm,entries=None,Log=[],commitIndex= -1,prevLogIndex= -1):
#     f = open("Message.json")

#     msg = json.load(f)
#     msg["request"] = "APPEND_RPC"
#     msg["sender_name"] = leaderId
#     msg["entries"] = []
#     msg["log"] = Log
#     msg["prevLogIndex"] = -1
#     msg["prevLogTerm"] = -1

#     return (json.dumps(msg)).encode("utf-8")

def AppendEntryMessage(leaderId, term):
    f = open("Message.json")

    msg = json.load(f)
    msg["request"] = "APPEND_RPC"
    msg["sender_name"] = leaderId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = -1
    msg["term"] = term

    return (json.dumps(msg)).encode("utf-8")



def SendVote(thisNode):
    f = open("Message.json")

    msg = json.load(f)

    msg["request"] = "VOTE_ACK"
    msg["sender_name"] = thisNode
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = -1

    return (json.dumps(msg)).encode("utf-8")


def RequestVoteRPC(term, candidateId):
    f = open("Message.json")

    msg = json.load(f)

    msg["request"] = "VOTE_REQUEST"
    msg["sender_name"] = candidateId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = term

    return (json.dumps(msg)).encode("utf-8")


def store(thisNode, term, leaderId, request="LEADER_INFO"):
    f = open("Message.json")

    msg = json.load(f)
    msg["sender_name"] = thisNode
    msg["term"] = term
    msg["request"] = request
    msg["key"] = "LEADER"
    msg["value"] = leaderId
    return (json.dumps(msg)).encode("utf-8")


def RetrieveMessage(candidateId, log):
    f = open("Message.json")

    msg = json.load(f)

    msg["request"] = "RETRIEVE"
    msg["sender_name"] = candidateId
    msg["term"] = "null"
    msg["key"] = "COMMITTED_LOGS"
    msg["value"] = log

    return (json.dumps(msg)).encode("utf-8")