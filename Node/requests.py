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


def AppendEntryMessage(leaderId, prevLogTerm):
    f = open("Message.json")

    msg = json.load(f)
    msg["request"] = "APPEND_RPC"
    msg["sender_name"] = leaderId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = -1

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


def RetrieveMessage(term, candidateId, log):
    f = open("Message.json")

    msg = json.load(f)

    msg["request"] = "RETRIEVE"
    msg["sender_name"] = candidateId
    msg["term"] = "null"
    msg["key"] = "COMMITTED_LOGS"
    msg["value"] = log

    return msg
    # return (json.dumps(msg)).encode("utf-8")
