import heapq

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # Distance from the start
        self.rhs = float('inf')  # Right-hand side value
        self.h = 0  # Heuristic value
        self.key = (float('inf'), float('inf'))  # Key for priority queue

    def __lt__(self, other):
        return self.key < other.key


class DStarLite:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.start = self.grid[0][0]
        self.goal = self.grid[width - 1][height - 1]
        self.robot = self.start
        self.open_list = []

    def initialize(self):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].g = float('inf')
                self.grid[x][y].rhs = float('inf')

        self.goal.g = float('inf')
        self.goal.rhs = 0
        self.open_list = []
        heapq.heappush(self.open_list, self.goal)

    def update_vertex(self, cell):
        if cell != self.goal:
            cell.rhs = min([self.get_cost(cell, succ) + succ.g for succ in self.get_neighbors(cell)])
        if cell in self.open_list:
            self.open_list.remove(cell)
        if cell.g != cell.rhs:
            cell.key = (min(cell.g, cell.rhs) + cell.h, min(cell.g, cell.rhs))
            heapq.heappush(self.open_list, cell)

    def compute_shortest_path(self):
        while self.open_list and (self.open_list[0].key < (self.robot.g, self.robot.rhs) or self.robot.rhs != self.robot.g):
            current = heapq.heappop(self.open_list)
            if current.g > current.rhs:
                current.g = current.rhs
                for pred in self.get_neighbors(current):
                    self.update_vertex(pred)
            else:
                current.g = float('inf')
                self.update_vertex(current)
                for pred in self.get_neighbors(current):
                    self.update_vertex(pred)
            print(f"Current: ({current.x}, {current.y})")

    def move_to_goal(self):
        while self.robot != self.goal:
            min_succ = min(self.get_neighbors(self.robot), key=lambda succ: self.get_cost(self.robot, succ) + succ.g)
            self.robot = min_succ
            print(f"Move to: ({self.robot.x}, {self.robot.y})")

    def get_neighbors(self, cell):
        neighbors = []
        if cell.x > 0:
            neighbors.append(self.grid[cell.x - 1][cell.y])
        if cell.x < self.width - 1:
            neighbors.append(self.grid[cell.x + 1][cell.y])
        if cell.y > 0:
            neighbors.append(self.grid[cell.x][cell.y - 1])
        if cell.y < self.height - 1:
            neighbors.append(self.grid[cell.x][cell.y + 1])
        return neighbors

    def get_cost(self, from_cell, to_cell):
        return 1  # Assuming uniform cost for simplicity


# Example usage
width = 5
height = 5
dstar = DStarLite(width, height)
dstar.initialize()
dstar.compute_shortest_path()
dstar.move_to_goal()
