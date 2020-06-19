class Grid:
    def __init__(self, width, height, p_width, p_height):
        self.width = width
        self.height = height
        self.p_width = p_width
        self.p_height = p_height
        self.pixels = []
        self.init_grid_array()

    def init_grid_array(self):
        self.pixels = []
        num_cols = self.width // self.p_width
        num_rows = self.height // self.p_height
        for i in range(num_rows):
            self.pixels.append([])
            for j in range(num_cols):
                self.pixels[i].append(0)

    def clicked(self, x, y):
        row = y // self.p_height
        col = x // self.p_width
        neighbors = self.get_neighbors(row, col)
        for r, c in neighbors:
            self.pixels[r][c] = 1

    def get_neighbors(self, row, col):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                neighbor_row = row + i
                neighbor_col = col + j
                if 0 <= neighbor_row < len(self.pixels) and 0 <= neighbor_col < len(self.pixels[row]):
                    neighbors.append((neighbor_row, neighbor_col))

        return neighbors