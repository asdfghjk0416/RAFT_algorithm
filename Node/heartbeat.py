import threading
import NodeInit


a = NodeInit.Node()
b = NodeInit.Node()
c = NodeInit.Node()
print(c.id)
c.changeID()
print(c.id)