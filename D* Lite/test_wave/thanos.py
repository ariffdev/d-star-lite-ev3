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

global currPos
global currDir


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




def scan_for_change(currPos, currDir):
    sound.speak('Current position is row {} column {} '.format(currPos[0], currPos[1]))
    #Ensuring always facing south before scan
    if currDir == north:
        spin('right', TURN_SPEED, 180)
    elif currDir == east:
        spin('right', TURN_SPEED, 90)
    elif currDir == west:
        spin('left', TURN_SPEED, 90)
    else: #south
        pass
    currDir = south

    new_world_map = copy.deepcopy(planning_map.world_map)
    print("dcopy", new_world_map)
    left = 1 if left_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm
    right = 1 if right_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm

    sound.speak('Left {}'.format(left))
    sound.speak('Right {}'.format(right))

    ##spin left to check forward(down) and backward(up)
    spin('left', TURN_SPEED, 90)
    # back = 1 if left_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm
    forward = 1 if right_sonar.distance_centimeters < 50 else 0 #obstacle if distance less than 50cm

    # sound.speak('Back {}'.format(back))
    sound.speak('Forward {}'.format(forward))

    ##spin back to original position
    spin('right', TURN_SPEED, 90)

    # new_world_map[currPos[0]][currPos[1]- 1] = left
    # new_world_map[currPos[0]][currPos[1]+ 1] = right
    # # new_world_map[currPos[0] - 1][currPos[1]] = back #not checking back
    # new_world_map[currPos[0] + 1][currPos[1]] = forward

    if currPos == (0,0):
        new_world_map[0][1] = left   
        new_world_map[1][0] = forward    
    elif currPos == (1,0):
        new_world_map[1][1] = left   
        new_world_map[2][0] = forward  
    elif currPos == (2,0):
        new_world_map[2][1] = left 
    
    elif currPos == (0,1):
        new_world_map[0][2] = left   
        new_world_map[1][1] = forward    
        new_world_map[0][0] = right
    elif currPos == (1,1):
        new_world_map[1][2] = left   
        new_world_map[2][1] = forward    
        new_world_map[1][0] = right
    elif currPos == (2,1):
        new_world_map[2][2] = left  
        new_world_map[2][0] = right

    elif currPos == (0,2):
        new_world_map[1][2] = forward    
        new_world_map[0][1] = right
    elif currPos == (1,2):
        new_world_map[2][2] = forward    
        new_world_map[1][1] = right
    elif currPos == (2,2):
        new_world_map[2][1] = right


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

    
    return [currDir, change, new_world_map]

def execute_next_step(path, currPos, currDir):
    sound.speak('Executing next step')
    nextPos = path.pop(0)
    relDir = relDirection(currPos, nextPos)

    print("At pos " + str(currPos) + " facing direction " + str(currDir)
            + " (" + directions[currDir] + ")")
    print("Next pos is " + str(nextPos)
            + ", whose direction relative to the current pos is "
            + str(relDir) + " (" + directions[relDir] + ")")
    print()

        # TO DO: IF NECESSARY, TURN TO FACE IN THE CORRECT DIRECTION

    if (currDir == north and relDir == east) or (currDir == east and relDir == south) or (currDir == south and relDir == west) or (currDir == west and relDir == north):
        sound.speak('Spinning')
        spin('right', TURN_SPEED, 90)

    elif (currDir == north and relDir == south) or (currDir == east and relDir == west) or (currDir == south and relDir == north) or (currDir == west and relDir == east):
        sound.speak('Spinning')
        spin('right', TURN_SPEED, 180)

    elif (currDir == north and relDir == west) or (currDir == west and relDir == south) or (currDir == south and relDir == east) or (currDir == east and relDir == north):
        sound.speak('Spinning')
        spin('left', TURN_SPEED, 90)

    else: #currDir == relDir
        pass

    
    # TO DO: MOVE ONE CELL FORWARD INTO THE NEXT POSITION
    sound.speak('Moving forward')
    move_straight(DRIVE_SPEED, CELL_DISTANCE_M)

    # Update the current position and orientation
    currPos = nextPos
    currDir = relDir
    return [currPos, currDir]



def recompute_algorithm(working_world_map, currPos):
    print("Working World Map: ", working_world_map)
    new_wavefront_plan = wavefront_algorithm(working_world_map, currPos, goal)
    print('New Plan:', new_wavefront_plan)
    path = path_extractor(new_wavefront_plan, currPos, goal)
    print('New Path:', path)
    return path


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
        [currDir, change, new_world_map] = scan_for_change(currPos, currDir)
        if change == False: #No change
            [currPos, currDir] = execute_next_step(path, currPos, currDir)
        else:
            working_world_map = copy.deepcopy(new_world_map)
            sound.speak('Recomputing path')
            path = recompute_algorithm(working_world_map, currPos)
            [currPos, currDir] = execute_next_step(path, currPos, currDir)
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
