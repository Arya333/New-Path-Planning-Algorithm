from plot import Plot
from models.agent import Agent
from operator import attrgetter
import math, sys

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

class Intermediate:
    grid = []
    agents = []
    goal_coords = []
    step = 0
    max_num_steps = 0
    finished_agents = []

    intermediate_candidates = []
    intermediate_candidates_2 = []
    stuck_agent_ids = []
    ids_to_intermediate_coords = {}


    def __init__(self, grid, agents, goal, step, max_steps, finished_agents):
        self.grid = grid
        self.agents = agents
        self.goal_coords = goal
        self.step = step
        self.max_num_steps = max_steps
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
        #print(self.intermediate_candidates)

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
    
    def find_closest_intermediate_coord2(self, new_coords):
        shortest_dist = 1000000000
        shortest_coords = []
        for coords in self.intermediate_candidates_2:
            dist = math.dist(new_coords, coords)
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
        #print(self.stuck_agent_ids)
        #print(self.ids_to_intermediate_coords)
    
    def check_ones(self):
        agents_with_ones = []
        temp = False
        if (self.agents[0].get_coord_num() == 1):
            temp = True
        else:
            return None
        index = 0
        while (temp):
            if (index >= len(self.agents) or self.agents[index].get_coord_num() != 1):
                temp = False
                break
            else:
                agents_with_ones.append(self.agents[index])
                index += 1
        agents_with_ones.sort(key=attrgetter('velocity'), reverse=True)
        # print(agents_with_ones)
        return agents_with_ones[0]

    def move_agent_towards_interm_coord(self, agent, up, down, left, right, rows, cols):
        curr_coords = agent.get_curr_coords()
        id = agent.get_id()
        interm_coord = self.ids_to_intermediate_coords[id]
        next_coords = [curr_coords[0], curr_coords[1]]
        moves = [up, down, left, right]
        order = []
        while (len(moves) > 0):
            min_dist = 1000000000
            coords_min_dist = []
            for move in moves:
                dist = math.dist(move, interm_coord)
                if (dist < min_dist):
                    min_dist = dist
                    coords_min_dist = move
            order.append(coords_min_dist)
            moves.remove(coords_min_dist)
        recent_coords = agent.trajectory[len(agent.trajectory) - 2]
        for move in order:
            if (is_coord_in_bounds(rows, cols, move) and self.grid[move[0]][move[1]].agent == None 
                and not self.grid[move[0]][move[1]].obstacle and not (move[0] == recent_coords[0] and move[1] == recent_coords[1])):
                next_coords = move
                break
        new_interm_target = self.find_closest_intermediate_coord2(next_coords)
        self.ids_to_intermediate_coords[id] = new_interm_target
        return next_coords


    def simulate(self):
        
        # Check if agent is in interm coords array
            # If so, move agents to coord in interm coords array that has smaller tile number than itself

        # If not in interm coords array, move agent towards associated interm coord
            # Move based on which move will reduce distance 
            # Avoid going to most recently visited tile (trajectory list final elem)
        plot = Plot(self.grid, self.step)
        while (self.step < self.max_num_steps):
            if (not self.agents):
                break
            if (len(self.stuck_agent_ids) == len(self.agents)):
                break
            
            self.step += 1
            self.agents.sort(key=attrgetter('coord_num'))
            rows = len(self.grid)
            cols = len(self.grid[0])

            agent_ones = self.check_ones()
            if (agent_ones != None):
                curr_coords = agent_ones.get_curr_coords()
                self.grid[curr_coords[0]][curr_coords[1]].update_agent(agent_ones, True)
                self.grid[self.goal_coords[0]][self.goal_coords[1]].update_agent(agent_ones, False)
                agent_ones.update_coords(self.goal_coords)
                agent_ones.add_to_path()
                agent_ones.reached()
                self.finished_agents.append(agent_ones)
                self.grid[self.goal_coords[0]][self.goal_coords[1]].update_agent(agent_ones, True)
                index_remove = 0
                for a in self.agents:
                    if (a.get_id() == agent_ones.get_id()):
                        break
                    index_remove += 1
                del self.agents[index_remove]

            for agent in self.agents:
                if (agent.get_coord_num() != 1):
                    id = agent.get_id()
                    cur_row = agent.curr_coords[0]
                    cur_col = agent.curr_coords[1]
                    next_coords = [cur_row, cur_col]
                    up = [cur_row - 1, cur_col]
                    down = [cur_row + 1, cur_col]
                    left = [cur_row, cur_col - 1]
                    right = [cur_row, cur_col + 1]
                    if (agent.get_curr_coords() in self.intermediate_candidates_2):
                        if (id in self.ids_to_intermediate_coords.keys()):
                            del self.ids_to_intermediate_coords[id]
                        if (is_coord_in_bounds(rows, cols, up) and self.grid[up[0]][up[1]].agent == None and self.grid[up[0]][
                            up[1]].get_num() < agent.get_coord_num() and up in self.intermediate_candidates_2):
                            next_coords[0] = up[0]
                            next_coords[1] = up[1]
                        elif (is_coord_in_bounds(rows, cols, down) and self.grid[down[0]][down[1]].agent == None and self.grid[down[0]][
                            down[1]].get_num() < agent.get_coord_num() and down in self.intermediate_candidates_2):
                            next_coords[0] = down[0]
                            next_coords[1] = down[1]
                        elif (is_coord_in_bounds(rows, cols, left) and self.grid[left[0]][left[1]].agent == None and self.grid[left[0]][
                            left[1]].get_num() < agent.get_coord_num() and left in self.intermediate_candidates_2):
                            next_coords[0] = left[0]
                            next_coords[1] = left[1]
                        elif (is_coord_in_bounds(rows, cols, right) and self.grid[right[0]][right[1]].agent == None and self.grid[right[0]][
                            right[1]].get_num() < agent.get_coord_num() and right in self.intermediate_candidates_2):
                            next_coords[0] = right[0]
                            next_coords[1] = right[1]
                    elif (id in self.ids_to_intermediate_coords.keys()):
                        next_coords = self.move_agent_towards_interm_coord(agent, up, down, left, right, rows, cols)

                    if (next_coords[0] != cur_row or next_coords[1] != cur_col):
                        new_coord_row = next_coords[0]
                        new_coord_col = next_coords[1]
                        self.grid[new_coord_row][new_coord_col].update_agent(agent, False)
                        self.grid[cur_row][cur_col].update_agent(agent, True)
                        agent.update_coords(next_coords)
                        agent.coord_num = self.grid[new_coord_row][new_coord_col].get_num()
                    agent.add_to_path()
            plot.set_grid(self.grid)
            plot.visualize()
            print("step = " + str(self.step))
            print("")
            print("Agents")
            print(self.agents)
            print("Interm Candidates")
            print(self.intermediate_candidates_2)
            print("Mapping")
            print(self.ids_to_intermediate_coords)
            print("")

    



    
