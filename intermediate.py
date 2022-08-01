from plot import Plot
from models.agent import Agent
import math, sys

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

class Intermediate:
    grid = []
    agents = []
    goal_coords = []
    step = 0
    finished_agents = []

    intermediate_candidates = []
    intermediate_candidates_2 = []
    stuck_agent_ids = []
    ids_to_intermediate_coords = {}


    def __init__(self, grid, agents, goal, step, finished_agents):
        self.grid = grid
        self.agents = agents
        self.goal_coords = goal
        self.step = step
        self.finished_agents = finished_agents

    def get_grid(self):
        return self.grid

    def get_agents(self):
        return self.agents

    def get_step(self):
        return self.step

    def get_finished_agents(self):
        return self.finished_agents

    def find_intermediate_candidates(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.path_to_coord_exists(row, col, self.goal_coords[0], self.goal_coords[1]) and not self.grid[row][col].obstacle and not (row == self.goal_coords[0] and col == self.goal_coords[1]):
                    self.intermediate_candidates.append([row, col])
        print(self.intermediate_candidates)

    def path_to_coord_exists(self, row, col, goal_row, goal_col):
        if (row == goal_row and col == goal_col):
            return True
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        moves = [up, down, left, right]
        for move in moves:
            check = False
            if (is_coord_in_bounds(len(self.grid), len(self.grid[0]), move) and self.grid[move[0]][move[1]].agent == None and not self.grid[move[0]][move[1]].obstacle and self.grid[move[0]][move[1]].get_num() < self.grid[row][col].get_num()):
                check = self.path_to_coord_exists(move[0], move[1], goal_row, goal_col)
            if (not check):
                continue
            else:
                return True
        return False
    
    def path_btwn_two_coords_exists(self, coord1, coord2):
        visited = [[False for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        path_exists = self.path_btwn_two_coords_recursion(coord1[0], coord1[1], coord2, visited)
        return path_exists
    
    def path_btwn_two_coords_recursion(self, row, col, coord2, visited):
        if (is_coord_in_bounds(len(self.grid), len(self.grid[0]), [row, col]) and not self.grid[row][col].obstacle and not visited[row][col]):
            visited[row][col] = True
            if (row == coord2[0] and col == coord2[1]):
                return True
            up = self.path_btwn_two_coords_recursion(row - 1, col, coord2, visited)
            if (up):
                return True
            down = self.path_btwn_two_coords_recursion(row + 1, col, coord2, visited)
            if (down):
                return True
            left = self.path_btwn_two_coords_recursion(row, col - 1, coord2, visited)
            if (left):
                return True
            right = self.path_btwn_two_coords_recursion(row, col + 1, coord2, visited)
            if (right):
                return True
        return False

    def is_agent_stuck(self, agent):
        row = agent.get_curr_coords()[0]
        col = agent.get_curr_coords()[1]
        for coord in self.intermediate_candidates:
            if (self.path_btwn_two_coords_exists(coord, [row, col])):
                return False
        return True
    
    def find_agent_by_id(self, id):
        index = 0
        for agent in self.agents:
            if (agent.get_id() == id):
                return agent, index
            index += 1  
        return -1, index

    def find_closest_intermediate_coord(self, agent):
        shortest_dist = 1000000000
        shortest_coords = []
        for coords in self.intermediate_candidates:
            dist = math.dist(agent.get_curr_coords(), coords)
            if (dist < shortest_dist):
                shortest_dist = dist
                shortest_coords = coords
        return shortest_coords
    
    def create_agent_intermediate_goal_mapping(self):
        for agent in self.agents:
           if (self.is_agent_stuck(agent)):
                self.stuck_agent_ids.append(agent.get_id())
           else:
                id = agent.get_id()
                closest_coord = self.find_closest_intermediate_coord(agent)
                self.ids_to_intermediate_coords[id] = closest_coord
                self.intermediate_candidates_2.append(closest_coord)
                self.intermediate_candidates.remove(closest_coord)
        for coord in self.intermediate_candidates:
            self.intermediate_candidates_2.append(coord)
        print(self.stuck_agent_ids)
        print(self.ids_to_intermediate_coords)
    
    def simulate(self):
        a = 1
        # Check if agent is in interm coords array
            # If so, move agents to coord in interm coords array that has smaller tile number than itself

        # If not in interm coords array, move agent towards associated interm coord
            # Move based on which move will reduce distance 
            # Avoid going to most recently visited tile (trajectory list final elem)

            

    



    
