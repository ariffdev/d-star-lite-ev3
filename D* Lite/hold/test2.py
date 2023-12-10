import heapq
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = math.inf
        self.rhs = math.inf

    def __lt__(self, other):
        return (self.g + self.heuristic) < (other.g + other.heuristic)

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def calculate_key(node, start, k_m):
    g_rhs = min(node.g, node.rhs)
    return (g_rhs + heuristic(start, node) + k_m, g_rhs)

def initialize(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    nodes = [[Node(x, y) for y in range(cols)] for x in range(rows)]

    goal.g = math.inf
    goal.rhs = 0

    open_list = []
    heapq.heappush(open_list, (calculate_key(start, start, 0), start))

    return nodes, open_list

def update_vertex(node, nodes, goal, open_list, k_m):
    if node != goal:
        node.rhs = min([nodes[succ.x][succ.y].g + 1 for succ in get_neighbors(node, nodes)])

    if node.g != node.rhs:
        heapq.heappush(open_list, (calculate_key(node, goal, k_m), node))

def get_neighbors(node, nodes):
    neighbors = []
    rows, cols = len(nodes), len(nodes[0])

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 neighbors

    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append(nodes[nx][ny])

    return neighbors

def replan(grid, start, goal):
    nodes, open_list = initialize(grid, start, goal)

    while open_list and (open_list[0][0] < calculate_key(goal, goal, 0) or goal.rhs != goal.g):
        k_old, current = heapq.heappop(open_list)

        if k_old < calculate_key(current, goal, 0):
            heapq.heappush(open_list, (calculate_key(current, goal, 0), current))
        elif current.g > current.rhs:
            current.g = current.rhs
            for pred in get_neighbors(current, nodes):
                update_vertex(pred, nodes, goal, open_list, 0)
        else:
            current.g = math.inf
            for pred in get_neighbors(current, nodes):
                update_vertex(pred, nodes, goal, open_list, 0)
            update_vertex(current, nodes, goal, open_list, 0)

    return nodes

def print_grid(grid, path=None):
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if (i, j) == path[0]:
                print("S", end=" ")
            elif (i, j) == path[-1]:
                print("G", end=" ")
            elif (i, j) in path:
                print("*", end=" ")
            elif grid[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()

# Example usage:
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = Node(0, 0)
goal = Node(4, 4)

nodes = replan(grid, start, goal)

# Extract the path from the nodes
path = [(goal.x, goal.y)]
current = goal
while current != start:
    neighbors = get_neighbors(current, nodes)
    next_node = min(neighbors, key=lambda x: nodes[x.x][x.y].g)
    path.append((next_node.x, next_node.y))
    current = next_node

path.reverse()

# Print the grid with the path
print_grid(grid, path)
