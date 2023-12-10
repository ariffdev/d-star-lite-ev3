#!/usr/bin/env python3
from wavefront_algorithm import wavefront_algorithm
from movement import *
from path_extraction import path_extractor
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_4
import planning_map
import copy


left_sonar = UltrasonicSensor(INPUT_4)
right_sonar = UltrasonicSensor(INPUT_1)
sound = Sound()




# Names of cardinal directions corresponding to the integers 0, 1, 2, and 3
directions = ['east','south','west','north']
east, south, west , north = 0, 1, 2, 3

DRIVE_SPEED = 250
TURN_SPEED = 250
CELL_DISTANCE_M = 45 / 100

# Computes the direction of pos2 relative to pos1, if pos2 is adjacent to pos1
# pos1 and pos2 are assumed to be tuples in the form (x,y)
# Direction is represented as an integer between 0 (corresponding to east) and
# 3 (corresponding to north)
# Throws an exception if pos2 is not adjacent to pos1
def relDirection(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    if x2==x1 and y2==y1+1:
        dir = 0
    elif x2==x1+1 and y2==y1:
        dir = 1
    elif x2==x1 and y2==y1-1:
        dir = 2
    elif x2==x1-1 and y2==y1:
        dir = 3
    else:
        raise ValueError(str(pos1)+" and " + str(pos2) + " are not neighbors,"\
                         +"so cannot compute relative direction between them.")
    return dir




def scan_for_change(currPos):
    new_world_map = copy.deepcopy(planning_map.world_map)
    print("dcopy", new_world_map)
    left = 1 if left_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm
    right = 1 if right_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm

    sound.speak('Left {}'.format(left))
    sound.speak('Right {}'.format(right))

    #Spin left to check forward(down) and backward(up)
    spin('left', TURN_SPEED, 90)
    back = 1 if left_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm
    forward = 1 if right_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm

    sound.speak('Back {}'.format(back))
    sound.speak('Forward {}'.format(forward))

    #Spin back to original position
    spin('right', TURN_SPEED, 90)

    new_world_map[currPos[0]][currPos[1]- 1] = left
    new_world_map[currPos[0]][currPos[1]+ 1] = right
    new_world_map[currPos[0] - 1][currPos[1]] = back
    new_world_map[currPos[0] + 1][currPos[1]] = forward

    print('nwmap', new_world_map)

    # if world_map == new_world_map:
    #     change = False
    #     sound.speak('No change')
    # else:
    #     change = True
    #     sound.speak('Lots of change')

    change = False
    for i in range(len(new_world_map)):
        for j in range(len(new_world_map[0])):
            if new_world_map[i][j] != planning_map.world_map[i][j]:
                change =  True
                sound.speak('Lots of change')
                break

    
    return [change, new_world_map]

def execute_next_step(path):
    sound.speak('Executing next step')
    pass

def recompute_algorithm(working_world_map):
    pass


# Assuming the robot starts at startPosition, facing the direction startOrientation,
# This function enables the robot to follow the path (a list of tuples representing
# positions) stored in the parameter path.
def run_dstar_lite(world_map, start, goal):
    #Initial steps

    startOrientation = south
    currPos = start
    currDir = startOrientation

    wavefront_plan = wavefront_algorithm(world_map, start, goal)
    path = path_extractor(wavefront_plan, start, goal)

    #Repeated Incremental Part
    while currPos != goal:
        [change, new_world_map] = scan_for_change(currPos)
        if change == False: #No change
            execute_next_step(path)
        else:
            working_world_map = new_world_map
            recompute_algorithm(working_world_map)
            continue
    if currPos == goal:
        sound.speak('Done')


world_map = [
    [0,1,0],
    [0,0,0],
    [1,1,0]
]

start = (1,1) #(0,0)
goal = (2,2)
run_dstar_lite(world_map, start, goal)
