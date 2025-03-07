#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import math
import rospy
from sensor_msgs.msg import JointState

# from pymycobot.mycobot import MyCobot
from pymycobot.mypalletizer import MyPalletizer


mc = None


def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "%s", data)
    data_list = []
    for index, value in enumerate(data.position):
        radians_to_angles = round(math.degrees(value), 2)
        data_list.append(radians_to_angles)
    rospy.loginfo(rospy.get_caller_id() + "%s", data_list)
    mc.send_angles(data_list, 25)


def listener():
    global mc
    rospy.init_node("mypal_reciver", anonymous=True)

    port = rospy.get_param("~port", "/dev/ttyUSB0")
    baud = rospy.get_param("~baud", 115200)
    print(port, baud)
    mc = MyPalletizer(port, baud)
    time.sleep(0.05)
    mc.set_free_mode(1)
    time.sleep(0.05)
    rospy.Subscriber("joint_states", JointState, callback)

    # spin() simply keeps python from exiting until this node is stopped 
    # spin()只是阻止python退出，直到该节点停止
    rospy.spin()


if __name__ == "__main__":
    listener()
