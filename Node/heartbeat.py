import threading


class AppendEntryMessage():
    def __init__(self,leaderId,entries,prevLogIndex,prevLogTerm):
        self.leaderId = leaderId
        self.entries =entries
        self.prevLogIndex = prevLogIndex
        self.prevLogTerm = prevLogTerm

class RequestVoteRPC():
    def __init__(self,term,candidateId,lastLogIndex,lastlogTerm):
        self.term = term
        self.candidateId = candidateId
        self.lastLogIndex = lastLogIndex
        self.lastLogTerm = lastlogTerm

