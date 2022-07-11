from models import coordinate

class Agent:
    id = -1
    velocity = 0
    curr_coords = [-1, -1]
    trajectory = []
    coord_num = -1
    reached_goal = False

    def __init__(self, agent_id, vel, coords, coord_num, trajectory):
        self.id = agent_id
        self.velocity = vel
        self.curr_coords = coords
        self.coord_num = coord_num
        self.trajectory = trajectory
        self.reached_goal = False

    def update_coords(self, new_coords):
        self.curr_coords = new_coords
        self.coord_num -= 1
    
    def add_to_path(self):
        self.trajectory.append(self.curr_coords)

    def get_coord_num(self):
        return self.coord_num
    
    def get_id(self):
        return self.id
    
    def get_curr_coords(self):
        return self.curr_coords

    def reached(self):
        self.reached_goal = True
    
    def __repr__(self):
        return "{ " + str(self.id) + " " + str(self.curr_coords) + " " + str(self.coord_num) + " " + str(self.velocity) + " }"
