from plot import Plot

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

class Intermediate:
    grid = []
    agents = []
    goal_coords = []
    step = 0

    intermediate_candidates = []

    def __init__(self, grid, agents, goal, step):
        self.grid = grid
        self.agents = agents
        self.goal_coords = goal
        self.step = step

    def get_grid(self):
        return self.grid

    def get_agents(self):
        return self.agents

    def get_step(self):
        return self.step

    def find_intermediate_candidates(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.path_to_goal_exists(row, col) and not self.grid[row][col].obstacle and not (row == self.goal_coords[0] and col == self.goal_coords[1]):
                    self.intermediate_candidates.append([row, col])
        print(self.intermediate_candidates)

    def path_to_goal_exists(self, row, col):
        if (row == self.goal_coords[0] and col == self.goal_coords[1]):
            return True
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        moves = [up, down, left, right]
        for move in moves:
            check = False
            if (is_coord_in_bounds(len(self.grid), len(self.grid[0]), move) and self.grid[move[0]][move[1]].agent == None and not self.grid[move[0]][move[1]].obstacle and self.grid[move[0]][move[1]].get_num() < self.grid[row][col].get_num()):
                check = self.path_to_goal_exists(move[0], move[1])
            if (not check):
                continue
            else:
                return True
        return False
