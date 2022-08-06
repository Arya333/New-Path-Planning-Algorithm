from matplotlib import pyplot
import numpy as np

class Plot:
    # Current state of grid (with Coordinate objects) to be displayed with graphics
    grid = []
    # Grid of tile numbers (0 is goal, tiles surrounding goal are 1, and so on)
    grid_nums = []
    # Current time step of simulation
    step = 0

    # Constructor
    def __init__(self, grid, step):
        self.step = step
        self.grid = grid
        self.grid_nums = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]
        # Initialize grid_nums with values 
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    # Update grid to the new one in the parameter
    # Update values in grid_num
    # Increment step because this method is called every time step (before visualize method)
    def set_grid(self, grid):
        self.step += 1
        self.grid = grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    # Initial visualization method for the simulation
    def visualize(self):
        pyplot.figure(figsize=(10,10))
        # Set up grid of coordinates with tile numbers on corresponding coordinates
        # Each tile number will have an associated color (coords with same tile number will be colored the same color for ease of visualization)
        pyplot.imshow(self.grid_nums)
        ax = pyplot.gca()
        # Set up row and column axis labels
        num_cols = len(self.grid[0])
        x_labels = range(num_cols)
        ax.set_xticklabels(x_labels, fontsize = 14)
        ax.set_xticks(x_labels)
        num_rows = len(self.grid)
        y_labels = range(num_rows)
        ax.set_yticklabels(y_labels, fontsize = 14)
        ax.set_yticks(y_labels)
        ax.set_xlabel('Column', fontsize = 16)
        ax.set_ylabel('Row', fontsize = 16)
        
        grid_nums_transposed = np.array(self.grid_nums).T
        for row in range(len(grid_nums_transposed)):
            for col in range(len(grid_nums_transposed[0])):
                num = grid_nums_transposed[row][col]
                # Tile Number
                pyplot.text(row + .25, col - .25, num, fontweight = 850, fontsize = 11)
                # Draw agents as white circles
                if (self.grid[col][row].agent != None):
                    circle = pyplot.Circle((row - .05, col + .05), radius = .3, color='white')
                    pyplot.text(row - .3, col + .05, "Agent " + str(self.grid[col][row].agent.get_id()), fontweight = 500, fontsize = 11)
                    ax.add_patch(circle)
                # Draw obstacles as black squares covering the entire coordinate
                if (self.grid[col][row].obstacle == True):
                    square = pyplot.Rectangle((row - .51, col - .51), height = 1.02, width = 1.02, color='black')
                    ax.add_patch(square)
        pyplot.figtext(.05, .95, "step = " + str(self.step), fontsize = 15)
        # Save this snapshot of the simulation in the images folder
        pyplot.savefig("images/step" + str(self.step) + ".png")
        
    # Visualization method for when a failure is detected (agent is stuck)
    def failure(self, id):
        pyplot.figure(figsize=(10,10))
        pyplot.imshow(self.grid_nums)
        ax = pyplot.gca()
        num_cols = len(self.grid[0])
        x_labels = range(num_cols)
        ax.set_xticklabels(x_labels, fontsize = 14)
        ax.set_xticks(x_labels)
        num_rows = len(self.grid)
        y_labels = range(num_rows)
        ax.set_yticklabels(y_labels, fontsize = 14)
        ax.set_yticks(y_labels)
        ax.set_xlabel('Column', fontsize = 16)
        ax.set_ylabel('Row', fontsize = 16)
        
        grid_nums_transposed = np.array(self.grid_nums).T
        for row in range(len(grid_nums_transposed)):
            for col in range(len(grid_nums_transposed[0])):
                num = grid_nums_transposed[row][col]
                pyplot.text(row + .25, col - .25, num, fontweight = 850, fontsize = 11)
                # Everything in this method is the same from in the visualize method except for below block of code
                # The id of the agent that is stuck is a parameter
                # The stuck agent is outputted as a red circle instead of a white circle (ease of visibility)
                if (self.grid[col][row].agent != None):
                    if (self.grid[col][row].agent.get_id() == id):
                        circle = pyplot.Circle((row - .05, col + .05), radius = .3, color='red')
                        pyplot.text(row - .3, col + .05, "Agent " + str(self.grid[col][row].agent.get_id()), fontweight = 500, fontsize = 11)
                        ax.add_patch(circle)
                    else:
                        circle = pyplot.Circle((row - .05, col + .05), radius = .3, color='white')
                        pyplot.text(row - .3, col + .05, "Agent " + str(self.grid[col][row].agent.get_id()), fontweight = 500, fontsize = 11)
                        ax.add_patch(circle)
                if (self.grid[col][row].obstacle == True):
                    square = pyplot.Rectangle((row - .51, col - .51), height = 1.02, width = 1.02, color='black')
                    ax.add_patch(square)
        pyplot.figtext(.05, .95, "step = " + str(self.step), fontsize = 15)
        pyplot.figtext(.4, .95, "Failed: Agent " + str(id) + " stuck", fontsize = 17)
        pyplot.savefig("images/step" + str(self.step) + ".png")