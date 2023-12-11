import heapq

class DStarLite:
    def __init__(self, grid, start, goal):
        self.width = len(grid[0])
        self.height = len(grid)
        self.start = start
        self.goal = goal
        self.km = 0
        self.graph = {(x, y): float('inf') for x in range(self.width) for y in range(self.height)}
        self.graph[self.start] = 0
        self.open_list = [(self.calculate_key(self.start), self.start)]
        self.obstacles = {(x, y) for x in range(self.width) for y in range(self.height) if grid[y][x] == 1}

    def calculate_key(self, node):
        return (min(self.graph[node], self.graph[node] + self.heuristic(node, self.goal) + self.km), min(self.graph[node], self.graph[node] + self.km))

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_vertex(self, node):
        if node != self.goal:
            self.graph[node] = min(neigh + self.cost(node, neigh) for neigh in self.neighbors(node))
        self.remove_from_open_list(node)

    def compute_shortest_path(self):
        while self.open_list and (self.open_list[0][0] < self.calculate_key(self.goal) or self.graph[self.goal] != self.graph[self.start]):
            current_key, current_node = heapq.heappop(self.open_list)
            if current_key < self.calculate_key(current_node):
                heapq.heappush(self.open_list, (self.calculate_key(current_node), current_node))
            elif self.graph[current_node] > self.graph_neigh_min(current_node):
                self.graph[current_node] = self.graph_neigh_min(current_node)
                for neigh in self.neighbors(current_node):
                    if self.graph[current_node] + self.cost(current_node, neigh) < self.graph[neigh]:
                        self.update_vertex(neigh)

    def graph_neigh_min(self, node):
        return min((neigh, self.cost(node, neigh)) for neigh in self.neighbors(node), key=lambda x: x[1])

    def cost(self, a, b):
        return (1,) if b not in self.obstacles else (float('inf'),)

    def neighbors(self, node):
        x, y = node
        possible_neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [(nx, ny) for nx, ny in possible_neighbors if 0 <= nx < self.width and 0 <= ny < self.height]

    def remove_from_open_list(self, node):
        self.open_list = [(key, n) for key, n in self.open_list if n != node]

    def update_start(self, new_start):
        self.km += self.heuristic(self.start, new_start)
        self.start = new_start
        self.update_vertex(self.goal)
        heapq.heappush(self.open_list, (self.calculate_key(new_start), new_start))

    def find_shortest_path(self):
        self.compute_shortest_path()
        path = [self.start]
        current_node = self.start
        while current_node != self.goal:
            min_neigh = min(self.neighbors(current_node), key=lambda n: self.graph[n] + self.cost(current_node, n)[0])
            path.append(min_neigh)
            current_node = min_neigh
        return path


if __name__ == "__main__":
    # Example usage with a 2D array representing obstacles and user-defined start and goal cells
    obstacle_grid = [
        [0, 0, 1],
        [0, 1, 0],
        [0, 0, 0]
    ]

    start_cell = (0, 0)
    goal_cell = (2, 2)

    ds_lite = DStarLite(obstacle_grid, start_cell, goal_cell)
    shortest_path = ds_lite.find_shortest_path()
    print("Shortest Path:", shortest_path)
