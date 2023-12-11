from planning_map import world_map

working_world_map = [
                    [1,1,0],
                    [1,1,0],
                    [0,0,0]
                    ]

x, y = 0, 1  # for indexing position tuples
world_map_x_len = len(working_world_map)
world_map_y_len = len(working_world_map[0])


def compute_neighbour_cells(currPos): #currPos -> tuple (x,y) of current position


  # Generating all possible neigbours in 4-point connectivity
  neighbour_dict = {
        'up': (currPos[x]-1, currPos[y]),
        'down': (currPos[x]+1, currPos[y]),
        'left': (currPos[x], currPos[y]- 1),
        'right': (currPos[x], currPos[y] + 1)
    }

  # Removing neighbours that may be out of the world map
  for key, value in neighbour_dict.copy().items(): #created copy of dictionary for searching to avoid size change in iteration error
    # neighbour does not fall in the world_map
    if ((value[x] < 0) or (value[x] >= world_map_x_len)) or ((value[y] < 0) or (value[y] >= world_map_y_len)):
      del neighbour_dict[key]
  neighbour_cells = list(neighbour_dict.values())

  return neighbour_cells #tuple of neighbour cells


print('Neighbours: ', compute_neighbour_cells((1,0)))

def path_extractor(working_world_map, wavefront_plan, start, goal):
  path = []
  currPos = start

  while goal not in path:  # determine path up till goal cell
    neighbours = compute_neighbour_cells(currPos)
    available_neighbours = [
        neighbour for neighbour in neighbours if wavefront_plan[neighbour[x]][neighbour[y]] != 1]
    print('Available Neighbours:', available_neighbours)

  # check the value in wavefront_plan that corresponds with the available_neighbours and find the one with the least value
    # initializing a number (infinity) that all options are guaranteed to be lower than
    lowest_move_option = float('inf')
    for neighbour in available_neighbours:
      if wavefront_plan[neighbour[x]][neighbour[y]] < lowest_move_option:
        lowest_move_option = wavefront_plan[neighbour[x]][neighbour[y]]
        most_available_neighbour = neighbour
    # set the most available neighbour as current position to keep path going
    currPos = most_available_neighbour
    path.append(most_available_neighbour)
    print('Most Available Neigbour: ', most_available_neighbour)  # printing to the EV3 screen
    print()
  return path  # return the constructed path


wavefront_plan = [
  [10000, 10000, 6],
    [10000, 10000, 5], 
    [2, 3, 4]]
path  = path_extractor(working_world_map, wavefront_plan, (0,2), (2,0))
print('Path: ', path)