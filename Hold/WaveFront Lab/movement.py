#!/usr/bin/env python3
import math
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C

# CONSTANTS
WHEEL_RADIUS_IN_CM = 5.5 / 2
ROBOT_BASELINE_IN_CM = 13.5

left_motor = OUTPUT_B
right_motor = OUTPUT_C

tank_pair = MoveTank(left_motor, right_motor)


def move_straight(speed, distance_in_metres):
  speed = speed / 10
  number_of_rotations_degrees = ((distance_in_metres * 100) / (2 * math.pi * WHEEL_RADIUS_IN_CM) * 360)
  tank_pair.on_for_degrees(speed, speed, number_of_rotations_degrees, brake=True, block=True)


def turn(direction, speed, turn_angle):
  speed = speed / 10
  number_of_rotations_degrees = (ROBOT_BASELINE_IN_CM/WHEEL_RADIUS_IN_CM) * turn_angle

  if direction == 'left': 
    right_speed, left_speed = 0, speed
  else:
    left_speed, right_speed = 0, speed
    
  tank_pair.on_for_degrees(left_speed, right_speed, number_of_rotations_degrees, brake=True, block=True )


def spin(direction, speed, turn_angle):
  speed = speed / 10
  number_of_rotations_degrees = (ROBOT_BASELINE_IN_CM / (2 * WHEEL_RADIUS_IN_CM)) * turn_angle

  if direction == 'left':  
    right_speed, left_speed = speed, -speed
  else:
    left_speed, right_speed = speed, -speed

  tank_pair.on_for_degrees(left_speed, right_speed,number_of_rotations_degrees, brake=True, block=True)
