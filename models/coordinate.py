from models import agent

class Coordinate:
    num = -1
    coords = [-1, -1]
    agent = None
    #reserved = False

    def __init__(self, num, coords, agent):
        self.num = num
        self.coords = coords
        self.agent = agent
    
    def update_agent(self, agent, is_remove):
        if (is_remove):
            self.agent = None
        else:
            self.agent = agent
    
    def get_num(self):
        return self.num