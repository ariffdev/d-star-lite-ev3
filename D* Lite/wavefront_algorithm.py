
from planning_map import world_map, start, goal

x, y = 0, 1  # for indexing position tuples

world_map_x_len = len(world_map)
world_map_y_len = len(world_map[0])

def wavefront_algorithm(world_map, start, goal):
  # Initializing queue
  queue = []

  #Creating wavefront_plan from world map
  wavefront_plan = world_map.copy()

  #Initializing goal cell to 2
  wavefront_plan[goal[x]][goal[y]] = 2

  #Adding goal cell to the queue
  queue.append(goal)

  while queue: #run till queue is empty
    #Take next cell from front of queue
    working_cell = queue.pop(0)

    #Determining non-obstacle neighbours who have not been processed
    # working_cell -> tuple (x,y) of current position
    def compute_non_processed_non_obstacle_neighbours(working_cell):
          # Generating all possible neigbours in 4-point connectivity
      neighbour_dict = {
          'up': (working_cell[x]-1, working_cell[y]),
          'down': (working_cell[x]+1, working_cell[y]),
          'left': (working_cell[x], working_cell[y] - 1),
          'right': (working_cell[x], working_cell[y] + 1)
      }

      # Removing neighbours that may be out of the wavefront plan
      # created copy of dictionary for searching to avoid size change in iteration error
      for key, value in neighbour_dict.copy().items():
        # neighbour does not fall in the world_map
        if ((value[x] < 0) or (value[x] >= world_map_x_len)) or ((value[y] < 0) or (value[y] >= world_map_y_len)):
          del neighbour_dict[key]
      neighbours = list(neighbour_dict.values())
      # Extracting non-obstacle neighbours
      non_obstacle_neighbours =  [neighbour for neighbour in neighbours if wavefront_plan[neighbour[x]][neighbour[y]] != 1]

      # Extracting non-processed non-obstacle neighbours
      non_processed_non_obstacle_neighbours = [non_processed_non_obstacle_neighbour for non_processed_non_obstacle_neighbour in non_obstacle_neighbours if wavefront_plan[non_processed_non_obstacle_neighbour[x]][non_processed_non_obstacle_neighbour[y]] == 0]
      return non_processed_non_obstacle_neighbours  # tuple of non_obstacle neighbour cells

    non_processed_non_obstacle_neighbours = compute_non_processed_non_obstacle_neighbours(working_cell)
    working_cell_value = lambda : wavefront_plan[working_cell[x]][working_cell[y]]

    #Setting values for non_processed_non_obstacle_neighbours and adding them to the queue
    for neighbour in non_processed_non_obstacle_neighbours:
        wavefront_plan[neighbour[x]][neighbour[y]] = working_cell_value() + 1
        queue.append(neighbour)
    
  return wavefront_plan

""" TEST """
# wavefront_algorithm(world_map, start, goal)





