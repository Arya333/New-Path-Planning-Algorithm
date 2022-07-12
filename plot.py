from matplotlib import pyplot
import numpy as np

class Plot:
    grid = []
    grid_nums = []
    step = 0

    def __init__(self, grid):
        self.grid = grid
        self.grid_nums = [[0 for i in range(len(grid[0]))] for j in range(len(grid))] 
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    def set_grid(self, grid):
        self.step += 1
        self.grid = grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    def visualize(self):
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
                if (self.grid[col][row].agent != None):
                    circle = pyplot.Circle((row - .05, col + .05), radius = .3, color='white')
                    pyplot.text(row - .2, col + .05, "Agent " + str(self.grid[col][row].agent.get_id()), fontweight = 500, fontsize = 11)
                    ax.add_patch(circle)
        pyplot.figtext(.05, .95, "step = " + str(self.step), fontsize = 15)
        pyplot.savefig("images/step" + str(self.step) + ".png")
        #pyplot.show()