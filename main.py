from models.agent import Agent
from models.coordinate import Coordinate
from operator import attrgetter
from plot import Plot
from intermediate import Intermediate
import os, time
import numpy as np
import collections
import random


def print_grid():
    for row in range(num_rows):
        for col in range(num_cols):
            num = grid[row][col].get_num()
            if (grid[row][col].agent == None):
                print(num, end=" ")
            else:
                print("X", end=" ")
        print("")

def in_agents_coords(row, col):
    for agent in agents:
        agent_row = agent.curr_coords[0]
        agent_col = agent.curr_coords[1]
        if (row == agent_row and col == agent_col):
            return True
    return False

def in_agents_coords_initial(row, col):
    for coord in agents_coords_initial:
        agent_row = coord[0]
        agent_col = coord[1]
        if (row == agent_row and col == agent_col):
            return True
    return False

def in_obs_coords(row, col):
    for coord in obstacles:
        obs_row = coord[0]
        obs_col = coord[1]
        if (row == obs_row and col == obs_col):
            return True
    return False

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

def init_grid(rows, cols, goal):
    if (not is_coord_in_bounds(rows, cols, goal)):
        raise Exception("goal coords not in bounds of grid dimensions")
    goal_row = goal[0]
    goal_col = goal[1]
    grid[goal_row][goal_col] = Coordinate(0, [goal_row, goal_col], None, False)

    some_coords_in_bounds = True
    dist = 1
    while (some_coords_in_bounds):
        some_coords_in_bounds = False
        up = [goal[0] - dist, goal[1]]
        down = [goal[0] + dist, goal[1]]
        left = [goal[0], goal[1] - dist]
        right = [goal[0], goal[1] + dist]
        if (is_coord_in_bounds(rows, cols, up)):
            some_coords_in_bounds = True
            grid[up[0]][up[1]] = Coordinate(dist, up, None, False)
        if (is_coord_in_bounds(rows, cols, down)):
            some_coords_in_bounds = True
            grid[down[0]][down[1]] = Coordinate(dist, down, None, False)
        if (is_coord_in_bounds(rows, cols, left)):
            some_coords_in_bounds = True
            grid[left[0]][left[1]] = Coordinate(dist, left, None, False)
        if (is_coord_in_bounds(rows, cols, right)):
            some_coords_in_bounds = True
            grid[right[0]][right[1]] = Coordinate(dist, right, None, False)

        up_to_right = [up[0] + 1, up[1] + 1]
        while (up_to_right[0] != right[0] and up_to_right[1] != right[1]):
            if (is_coord_in_bounds(rows, cols, up_to_right)):
                some_coords_in_bounds = True
                grid[up_to_right[0]][up_to_right[1]] = Coordinate(dist, up_to_right, None, False)
            up_to_right = [up_to_right[0] + 1, up_to_right[1] + 1]

        right_to_down = [right[0] + 1, right[1] - 1]
        while (right_to_down[0] != down[0] and right_to_down[1] != down[1]):
            if (is_coord_in_bounds(rows, cols, right_to_down)):
                some_coords_in_bounds = True
                grid[right_to_down[0]][right_to_down[1]] = Coordinate(dist, right_to_down, None, False)
            right_to_down = [right_to_down[0] + 1, right_to_down[1] - 1]

        down_to_left = [down[0] - 1, down[1] - 1]
        while (down_to_left[0] != left[0] and down_to_left[1] != left[1]):
            if (is_coord_in_bounds(rows, cols, down_to_left)):
                some_coords_in_bounds = True
                grid[down_to_left[0]][down_to_left[1]] = Coordinate(dist, down_to_left, None, False)
            down_to_left = [down_to_left[0] - 1, down_to_left[1] - 1]

        left_to_up = [left[0] - 1, left[1] + 1]
        while (left_to_up[0] != up[0] and left_to_up[1] != up[1]):
            if (is_coord_in_bounds(rows, cols, left_to_up)):
                some_coords_in_bounds = True
                grid[left_to_up[0]][left_to_up[1]] = Coordinate(dist, left_to_up, None, False)
            left_to_up = [left_to_up[0] - 1, left_to_up[1] + 1]

        dist += 1

def init_agents():
    for agent in agents:
        row = agent.curr_coords[0]
        col = agent.curr_coords[1]
        grid[row][col].update_agent(agent, False)
        grid[row][col].agent.add_to_path()

def check_ones():
    agents_with_ones = []
    temp = False
    if (agents[0].get_coord_num() == 1):
        temp = True
    else:
        return None
    index = 0
    while (temp):
        if (index >= len(agents) or agents[index].get_coord_num() != 1):
            temp = False
            break
        else:
            agents_with_ones.append(agents[index])
            index += 1
    agents_with_ones.sort(key=attrgetter('velocity'), reverse=True)
    # print(agents_with_ones)
    return agents_with_ones[0]

def detect_failure(rows, cols):
    fail = True
    index = 0
    for agent in agents:
        fail = True # if you want all other agents to reach goal before finding failed agent, comment this line out
        row = agent.get_curr_coords()[0]
        col = agent.get_curr_coords()[1]
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        if (is_coord_in_bounds(rows, cols, up) and (grid[up[0]][up[1]].get_num() < agent.get_coord_num()) and (grid[up[0]][up[1]].agent == None)):
            fail = False
            index += 1
            continue
        if (is_coord_in_bounds(rows, cols, down) and (grid[down[0]][down[1]].get_num() < agent.get_coord_num()) and (grid[down[0]][down[1]].agent == None)):
            fail = False
            index += 1
            continue
        if (is_coord_in_bounds(rows, cols, left) and (grid[left[0]][left[1]].get_num() < agent.get_coord_num()) and (grid[left[0]][left[1]].agent == None)):
            fail = False
            index += 1
            continue
        if (is_coord_in_bounds(rows, cols, right) and (grid[right[0]][right[1]].get_num() < agent.get_coord_num()) and (grid[right[0]][right[1]].agent == None)):
            fail = False
            index += 1
            continue
        print(agent.id)
        print(index)
        print("")
        break
    if fail:
        return index
    else:
        return -1
    
def detect_failure_agent(rows, cols, index):
    print("det fail agent")
    print(agents)
    agent = agents[index]
    row = agent.get_curr_coords()[0]
    col = agent.get_curr_coords()[1]
    up = [row - 1, col]
    down = [row + 1, col]
    left = [row, col - 1]
    right = [row, col + 1]
    if (is_coord_in_bounds(rows, cols, up) and (grid[up[0]][up[1]].get_num() < agent.get_coord_num()) and (grid[up[0]][up[1]].agent == None)):
        return -1
    if (is_coord_in_bounds(rows, cols, down) and (grid[down[0]][down[1]].get_num() < agent.get_coord_num()) and (grid[down[0]][down[1]].agent == None)):
        return -1  
    if (is_coord_in_bounds(rows, cols, left) and (grid[left[0]][left[1]].get_num() < agent.get_coord_num()) and (grid[left[0]][left[1]].agent == None)):
        return -1
    if (is_coord_in_bounds(rows, cols, right) and (grid[right[0]][right[1]].get_num() < agent.get_coord_num()) and (grid[right[0]][right[1]].agent == None)):
        return -1
    return 0

def cause_intermediate(rows, cols):
    fail = detect_failure_agent(rows, cols, 0)
    temp = 0
    while (fail != -1 and temp < len(agents)): #problem here
        fail = detect_failure_agent(rows, cols, temp)
        temp += 1
    return fail != -1
        
def simulate(rows, cols, goal, max_num_steps):
    step = 0
    while (step < max_num_steps):
        if (not agents):
            break

        # Intermediate goals / delayed stop

        stuck = cause_intermediate(rows, cols)
        if (stuck):
            fail_agent_id = agents[detect_failure(rows, cols)].get_id()
            plot.failure(fail_agent_id)
            intermediate = Intermediate(grid, agents, goal_coord, step)
            intermediate.find_intermediate_candidates()
            break

        # Stop at first failure

        # fail = detect_failure(rows, cols)
        # print("fail = " + str(fail))
        # if (fail != -1):
        #     fail_agent_id = agents[fail].get_id()
        #     plot.failure(fail_agent_id)
        #     break

        step += 1
        agents.sort(key=attrgetter('coord_num'))

        # Check for collision

        coords_at_current_time = [a.get_curr_coords for a in agents]
        collisions = [x for n, x in enumerate(coords_at_current_time) if x in coords_at_current_time[:n]]
        num_collisions = len(collisions)
        print(num_collisions)

        agent_ones = check_ones()
        if (agent_ones != None):
            curr_coords = agent_ones.get_curr_coords()
            grid[curr_coords[0]][curr_coords[1]].update_agent(agent_ones, True)
            grid[goal_coord[0]][goal_coord[1]].update_agent(agent_ones, False)
            agent_ones.update_coords(goal_coord)
            agent_ones.add_to_path()
            agent_ones.reached()
            finished_agents.append(agent_ones)
            grid[goal_coord[0]][goal_coord[1]].update_agent(agent_ones, True)
            index_remove = 0
            for a in agents:
                if (a.get_id() == agent_ones.get_id()):
                    break
                index_remove += 1
            del agents[index_remove]

        for agent in agents:
            if (agent.get_coord_num() != 1):
                cur_row = agent.curr_coords[0]
                cur_col = agent.curr_coords[1]
                next_coords = [cur_row, cur_col]
                up = [cur_row - 1, cur_col]
                down = [cur_row + 1, cur_col]
                left = [cur_row, cur_col - 1]
                right = [cur_row, cur_col + 1]

                if (is_coord_in_bounds(rows, cols, up) and grid[up[0]][up[1]].agent == None and grid[up[0]][
                    up[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = up[0]
                    next_coords[1] = up[1]
                elif (is_coord_in_bounds(rows, cols, down) and grid[down[0]][down[1]].agent == None and grid[down[0]][
                    down[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = down[0]
                    next_coords[1] = down[1]
                elif (is_coord_in_bounds(rows, cols, left) and grid[left[0]][left[1]].agent == None and grid[left[0]][
                    left[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = left[0]
                    next_coords[1] = left[1]
                elif (is_coord_in_bounds(rows, cols, right) and grid[right[0]][right[1]].agent == None and
                      grid[right[0]][right[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = right[0]
                    next_coords[1] = right[1]

                if (next_coords[0] != cur_row or next_coords[1] != cur_col):
                    new_coord_row = next_coords[0]
                    new_coord_col = next_coords[1]
                    grid[new_coord_row][new_coord_col].update_agent(agent, False)
                    grid[cur_row][cur_col].update_agent(agent, True)
                    agent.update_coords(next_coords)
                agent.add_to_path()
        plot.set_grid(grid)
        plot.visualize()
        print("step = " + str(step))
        print(agents)
        # print_grid()
        print("")


num_rows = 6
num_cols = 6
num_agents = 6
vels = [i for i in range(1, 1 + num_agents)]
goal_coord = list(np.random.randint(1, num_rows, 2))
#goal_coord = [0, 3]
grid = [[0 for i in range(num_cols)] for j in range(num_rows)]
init_grid(num_rows, num_cols, goal_coord)

agent_id_index = 0
agents = []
finished_agents = []

agents_coords_initial = []
temp = 0
while temp < num_agents:
    rand_row = random.randint(0, num_rows - 1)
    rand_col = random.randint(0, num_cols - 1)
    if (not (in_agents_coords_initial(rand_row, rand_col) or (rand_row == goal_coord[0] and rand_col == goal_coord[1]))):
        agents_coords_initial.append([rand_row, rand_col])
        temp += 1

for i in range(num_agents):
    agents.append(Agent(agent_id_index, vels[i], agents_coords_initial[i],
                        grid[agents_coords_initial[i][0]][agents_coords_initial[i][1]].get_num(), []))
    agent_id_index += 1

agents.sort(key=attrgetter('coord_num'))
init_agents()

num_obstacles = 10
obs_num_id = num_rows + num_cols
temp = 0
obstacles = []
while temp < num_obstacles:
    rand_row = random.randint(0, num_rows - 1)
    rand_col = random.randint(0, num_cols - 1)
    if (not (in_agents_coords(rand_row, rand_col) or in_obs_coords(rand_row, rand_col) or (rand_row == goal_coord[0] and rand_col == goal_coord[1]))):
        grid[rand_row][rand_col] = Coordinate(obs_num_id, [rand_row, rand_col], None, True)
        obstacles.append([rand_row, rand_col])
        temp += 1
print(obstacles)

print("step = 0")
print(agents)
print_grid()
print("")

plot = Plot(grid)
plot.visualize()
start = time.time()
simulate(num_rows, num_cols, goal_coord, 20)
print("time taken:", time.time() - start)
pro = os.system("ffmpeg -r 1 -f image2 -i ./images/step%d.png -s 1000x1000 -y simulation.avi")
