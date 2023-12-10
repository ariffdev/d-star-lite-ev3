#!/usr/bin/env python3
import movement

print('Moving forward')
# movement.move_straight(250, 0.45)
print('Turning')
movement.spin('right',250,90)
movement.stop()
movement.spin('left',250,90)


