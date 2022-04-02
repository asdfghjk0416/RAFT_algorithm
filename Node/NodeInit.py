import follower

IDtoUse = 0

class Node: 

    
    def __init__(self):
        global IDtoUse
        self.id = IDtoUse
        IDtoUse += 1
        self.state = follower()

    def changeID(self):
        self.id = 1000