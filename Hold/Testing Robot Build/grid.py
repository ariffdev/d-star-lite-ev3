#!/usr/bin/env python3
from movement import *
f = open("path.txt")
path = f.read().split("\n")
f.close()


DRIVE_SPEED = 250
TILE_DISTANCE_IN_METRES = 44.5 / 100


for step in path:
  if step == 'forward':
    move_straight(DRIVE_SPEED,TILE_DISTANCE_IN_METRES )
  elif step == 'backward':
    move_straight(-DRIVE_SPEED, TILE_DISTANCE_IN_METRES)
  elif step == 'left':
    spin('left', DRIVE_SPEED, 90)
  elif step == 'right':
    spin('right', DRIVE_SPEED, 90)
  else:
    continue







