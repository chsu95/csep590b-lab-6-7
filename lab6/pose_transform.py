#!/usr/bin/env python3

'''
This is starter code for Lab 6 on Coordinate Frame transforms.

'''

import asyncio
import cozmo
import numpy as np
import math
from cozmo.util import degrees

def get_relative_pose(object_pose, reference_frame_pose):
    ox, oy, oz = object_pose.position.x_y_z
    oang = object_pose.rotation.angle_z.radians
    cx, cy, cz = reference_frame_pose.position.x_y_z
    cang = reference_frame_pose.rotation.angle_z.radians

    o1 = [math.cos(oang), -math.sin(oang), 0, ox]
    o2 = [math.sin(oang), math.cos(oang), 0, oy]
    o3 = [0, 0, 1, oz]
    o4 = [0, 0, 0, 1]
    o = np.matrix([o1, o2, o3, o4])

    c = np.matrix([[cx, cy, cz, 1]]).T

    newXyz = o * c
    newAng = oang + cang

    return cozmo.util.pose_z_angle(newXyz[0,0], newXyz[1,0], newXyz[2,0], cozmo.util.Angle(radians = newAng))

def find_relative_cube_pose(robot: cozmo.robot.Robot):
    '''Looks for a cube while sitting still, prints the pose of the detected cube
    in world coordinate frame and relative to the robot coordinate frame.'''

    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()
    cube = None

    while True:
        try:
            cube = robot.world.wait_for_observed_light_cube(timeout=30)
            if cube:
                print("Robot pose: %s" % robot.pose)
                print("Cube pose: %s" % cube.pose)
                print("Cube pose in the robot coordinate frame: %s" % get_relative_pose(cube.pose, robot.pose))
        except asyncio.TimeoutError:
            print("Didn't find a cube")


if __name__ == '__main__':

    cozmo.run_program(find_relative_cube_pose)
