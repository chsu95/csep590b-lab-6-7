#!/usr/bin/env python3

'''
Stater code for Lab 7.

'''

import cozmo
from cozmo.util import degrees, Angle, Pose, distance_mm, speed_mmps
import math

# Wrappers for existing Cozmo navigation functions

def cozmo_drive_straight(robot, dist, speed):
    """Drives the robot straight.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        dist -- Desired distance of the movement in millimeters
        speed -- Desired speed of the movement in millimeters per second
    """
    robot.drive_straight(distance_mm(dist), speed_mmps(speed)).wait_for_completed()

def cozmo_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle -- Desired distance of the movement in degrees
        speed -- Desired speed of the movement in degrees per second
    """
    robot.turn_in_place(degrees(angle), speed=degrees(speed)).wait_for_completed()

def cozmo_go_to_pose(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    robot.go_to_pose(Pose(x, y, 0, angle_z=degrees(angle_z)), relative_to_robot=True).wait_for_completed()

# Functions to be defined as part of the labs

def get_front_wheel_radius():
    """Returns the radius of the Cozmo robot's front wheel in millimeters."""
    # ####
    # Trial and error until found distance that makes front wheel do one full rotation.
    # radius = distance (circumference) / (2pi)
    # distance was 87mm
    # ####
    return 87 / 2 / math.pi

def get_distance_between_wheels():
    """Returns the distance between the wheels of the Cozmo robot in millimeters."""
    # ####
    # Set left tread to drive at 10 mm/s with high acceleration, right tread same speed
    # but backwards. Trial and error until found time limit necessary for robot to complete
    # one quarter turn.
    # radius (i.e. dist between wheels) = circumference / (2pi)
    # circumference = speed * time * 4
    # time was 7.2s
    # Note: Multiply by 4 in the last step we used quarter turn
    # ####
    return 10 * 7.2 * 4 / 2 / math.pi

def rotate_front_wheel(robot, angle_deg):
    """Rotates the front wheel of the robot by a desired angle.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle_deg -- Desired rotation of the wheel in degrees
    """
    circ = get_front_wheel_radius() * 2 * math.pi
    dist = angle_deg / 360 * circ
    cozmo_drive_straight(robot, dist, 10)
    pass

def my_drive_straight(robot, dist, speed):
    """Drives the robot straight.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        dist -- Desired distance of the movement in millimeters
        speed -- Desired speed of the movement in millimeters per second
    """
    time = dist / speed
    robot.drive_wheels(speed, speed, l_wheel_acc=1000, r_wheel_acc=1000, duration=time)
    pass

def my_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle -- Desired distance of the movement in degrees
        speed -- Desired speed of the movement in degrees per second
    """
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    if angle > 180:
        mult = -1
        angle = 360 - angle
    else:
        mult = 1
    circ = get_distance_between_wheels() * 2 * math.pi
    num_circs = angle / 360
    dist = circ * num_circs
    time = dist / speed
    speed = mult * speed
    robot.drive_wheels(-speed, speed, l_wheel_acc=1000, r_wheel_acc=1000, duration=time)
    pass

def get_angle(x, y):
    if x == 0:
        if y > 0:
            angle = 90
        else:
            angle = 270
    else:
        angle = math.degrees(math.atan(y / x))
        if x < 0 and y < 0:
            angle += 180
    return angle

def my_go_to_pose1(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    dist = math.sqrt(x**2 + y**2)
    angle = get_angle(x, y)
    my_turn_in_place(robot, angle, 30)
    my_drive_straight(robot, dist, 30)
    my_turn_in_place(robot, -angle + angle_z, 30)
    pass

def my_go_to_pose2(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    trav_dist = math.sqrt(x ** 2 + y ** 2)
    angle = get_angle(x, y)
    if x < 0:
        angle -= 180
        angle_z += 180
        my_turn_in_place(robot, 180, 30)

    circ = get_distance_between_wheels() * 2 * math.pi
    num_circs = angle / 360
    correction_factor = 1.4 # Estimated through empirical observation
    turn_dist = circ * num_circs * correction_factor

    d_left = trav_dist - turn_dist
    d_right = trav_dist + turn_dist

    time = 10
    speed_left = d_left / time
    speed_right = d_right / time

    robot.drive_wheels(speed_left, speed_right, l_wheel_acc=1000, r_wheel_acc=1000, duration=time)
    my_turn_in_place(robot, -angle + angle_z, 30)
    pass

def my_go_to_pose3(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    if (x < 0):
        my_go_to_pose1(robot, x, y, angle_z)
    else:
        my_go_to_pose2(robot, x, y, angle_z)
    pass

def run(robot: cozmo.robot.Robot):

    print("***** Front wheel radius: " + str(get_front_wheel_radius()))
    print("***** Distance between wheels: " + str(get_distance_between_wheels()))

    ## Example tests of the functions

    # cozmo_drive_straight(robot, 62, 50)
    # cozmo_turn_in_place(robot, 60, 30)
    # cozmo_go_to_pose(robot, 100, 100, 45)
    #
    # rotate_front_wheel(robot, 90)
    # my_drive_straight(robot, 62, 50)
    # my_turn_in_place(robot, 90, 30)
    #
    # my_go_to_pose1(robot, 100, 100, 45)
    # my_go_to_pose2(robot, 100, 100, 45)
    # my_go_to_pose3(robot, 100, 100, 45)
    return


if __name__ == '__main__':

    cozmo.run_program(run)



