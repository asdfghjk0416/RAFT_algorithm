import threading
import NodeInit


class AppendEntryMessage():
    def __init__(self,leaderId,entries,prevLogIndex,prevLogTerm):
        self.leaderId = leaderId
        self.entries =entries
        self.prevLogIndex = prevLogIndex
        self.prevLogTerm = prevLogTerm



a = NodeInit.Node()
b = NodeInit.Node()
c = NodeInit.Node()
print(c.id)
c.changeID()
print(c.id)