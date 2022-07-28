from models import agent

class Coordinate:
    num = -1
    coords = [-1, -1]
    agent = None
    obstacle = False

    def __init__(self, num, coords, agent, obs):
        self.num = num
        self.coords = coords
        self.agent = agent
        self.obstacle = obs
    
    def update_agent(self, agent, is_remove):
        if (is_remove):
            self.agent = None
        else:
            self.agent = agent
    
    def get_num(self):
        return self.num