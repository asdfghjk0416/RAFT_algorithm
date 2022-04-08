import heartbeat

# q = heartbeat.AppendEntryMessage("a", [], -1,0)

q = heartbeat.RequestVoteRPC(0, "node1")
print(q)