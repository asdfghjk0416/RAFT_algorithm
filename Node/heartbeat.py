from email import message
import threading
import json



def AppendEntryMessage(leaderId,prevLogTerm):
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
def RequestVoteRPC(term,candidateId):
    f = open("Message.json")

    msg = json.load(f)  

    msg["request"] = "VOTE_REQUEST"
    msg["sender_name"] = candidateId
    msg["entries"] = []
    msg["prevLogIndex"] = -1
    msg["prevLogTerm"] = term

    return (json.dumps(msg)).encode("utf-8")