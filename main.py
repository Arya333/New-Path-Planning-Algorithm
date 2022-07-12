from models.agent import Agent
from models.coordinate import Coordinate
from operator import attrgetter
from plot import Plot

def print_grid():
    for row in range(num_rows):
        for col in range(num_cols):
            num = grid[row][col].get_num()
            if (grid[row][col].agent == None):
                print(num, end = " ")
            else:
                print("X", end = " ")
        print("")

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols 

def init_grid(rows, cols, goal):
    if (not is_coord_in_bounds(rows, cols, goal)):
        raise Exception("goal coords not in bounds of grid dimensions")
    goal_row = goal[0]
    goal_col = goal[1]
    grid[goal_row][goal_col] = Coordinate(0, [goal_row, goal_col], None)

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
            grid[up[0]][up[1]] = Coordinate(dist, up, None)
        if (is_coord_in_bounds(rows, cols, down)):
            some_coords_in_bounds = True
            grid[down[0]][down[1]] = Coordinate(dist, down, None)
        if (is_coord_in_bounds(rows, cols, left)):
            some_coords_in_bounds = True
            grid[left[0]][left[1]] = Coordinate(dist, left, None)
        if (is_coord_in_bounds(rows, cols, right)):
            some_coords_in_bounds = True
            grid[right[0]][right[1]] = Coordinate(dist, right, None)
        
        up_to_right = [up[0] + 1, up[1] + 1]
        while (up_to_right[0] != right[0] and up_to_right[1] != right[1]):
            if (is_coord_in_bounds(rows, cols, up_to_right)):
                some_coords_in_bounds = True
                grid[up_to_right[0]][up_to_right[1]] = Coordinate(dist, up_to_right, None)
            up_to_right = [up_to_right[0] + 1, up_to_right[1] + 1]

        right_to_down = [right[0] + 1, right[1] - 1]
        while (right_to_down[0] != down[0] and right_to_down[1] != down[1]):
            if (is_coord_in_bounds(rows, cols, right_to_down)):
                some_coords_in_bounds = True
                grid[right_to_down[0]][right_to_down[1]] = Coordinate(dist, right_to_down, None)
            right_to_down = [right_to_down[0] + 1, right_to_down[1] - 1]
        
        down_to_left = [down[0] - 1, down[1] - 1]
        while (down_to_left[0] != left[0] and down_to_left[1] != left[1]):
            if (is_coord_in_bounds(rows, cols, down_to_left)):
                some_coords_in_bounds = True
                grid[down_to_left[0]][down_to_left[1]] = Coordinate(dist, down_to_left, None)
            down_to_left = [down_to_left[0] - 1, down_to_left[1] - 1]
        
        left_to_up = [left[0] - 1, left[1] + 1]
        while (left_to_up[0] != up[0] and left_to_up[1] != up[1]):
            if (is_coord_in_bounds(rows, cols, left_to_up)):
                some_coords_in_bounds = True
                grid[left_to_up[0]][left_to_up[1]] = Coordinate(dist, left_to_up, None)
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
    while(temp):
        if (index >= len(agents) or agents[index].get_coord_num() != 1):
            temp = False
            break
        else:
            agents_with_ones.append(agents[index])
            index += 1
    agents_with_ones.sort(key=attrgetter('velocity'), reverse=True)
    print(agents_with_ones)
    return agents_with_ones[0]

def simulate(rows, cols, goal, max_num_steps):
    step = 0
    while (step < max_num_steps):
        if (not agents):
            break
        step += 1
        
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

                if (is_coord_in_bounds(rows, cols, up) and grid[up[0]][up[1]].agent == None and grid[up[0]][up[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = up[0]
                    next_coords[1] = up[1]
                elif (is_coord_in_bounds(rows, cols, down) and grid[down[0]][down[1]].agent == None and grid[down[0]][down[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = down[0]
                    next_coords[1] = down[1]
                elif (is_coord_in_bounds(rows, cols, left) and grid[left[0]][left[1]].agent == None and grid[left[0]][left[1]].get_num() < agent.get_coord_num()):
                    next_coords[0] = left[0]
                    next_coords[1] = left[1]
                elif (is_coord_in_bounds(rows, cols, right) and grid[right[0]][right[1]].agent == None and grid[right[0]][right[1]].get_num() < agent.get_coord_num()):
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
        print_grid()
        print("")

num_rows = 5
num_cols = 5
goal_coord = [0, 1]
grid = [[0 for i in range(num_cols)] for j in range(num_rows)] 
init_grid(num_rows, num_cols, goal_coord)

agent_id_index = 0
agents = []
finished_agents = []

agents.append(Agent(agent_id_index, 5, [3, 0], grid[3][0].get_num(), []))
agent_id_index += 1
agents.append(Agent(agent_id_index, 10, [2, 3], grid[2][3].get_num(), []))
agent_id_index += 1
agents.sort(key=attrgetter('coord_num'))
init_agents()
print("step = 0")
print_grid()
print("")

plot = Plot(grid)
plot.visualize()

simulate(num_rows, num_cols, goal_coord, 8)
print(finished_agents[0].trajectory)
