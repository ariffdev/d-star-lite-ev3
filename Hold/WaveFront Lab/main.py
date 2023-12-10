#!/usr/bin/env python3

from wavefront_algorithm import wavefront_algorithm
from planning_map import *
from follow_path_test import followPath, north, east, south, west
from path_extraction import path_extractor

wavefront_plan = wavefront_algorithm(world_map, start, goal)
path = path_extractor(wavefront_plan, start, goal)

""" RUN ON ROBOT """
# startOrientation = east
# followPath(start, startOrientation, path)

print('Wavefront Plan:', wavefront_plan)
print('Path', path)

