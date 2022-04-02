import follower
import Leader

IDtoUse = 0

class Node: 

    
    def __init__(self):
        global IDtoUse
        self.id = IDtoUse
        IDtoUse += 1
        self.state = follower()

    def ChangeState(self):
        self.state = Leader()