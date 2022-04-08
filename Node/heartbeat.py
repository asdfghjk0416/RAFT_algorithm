from email import message
import threading
import json



def AppendEntryMessage(leaderId,prevLogTerm):
    f = open("Message.json")

    msg = json.load(f)
    msg["type"] = "AppendEntryMessage"
    msg["sender_name"] = leaderId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = prevLogTerm

    return (json.dumps(msg)).encode("utf-8")
    

def RequestVoteRPC(term,candidateId):
    f = open("Message.json")

    msg = json.load(f)  

    msg["type"] = RequestVoteRPC
    msg["sender_name"] = candidateId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = term

    return (json.dumps(msg)).encode("utf-8")