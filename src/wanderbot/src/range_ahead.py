#!/usr/bin/env python
#coding=utf-8
# 订阅深度相机‘scan’话题，输出正前方的距离
import rospy
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
	range_ahead = msg.ranges[len(msg.ranges)/2]
	print("range ahead: %0.1f" % range_ahead)

rospy.init_node('range_ahead')
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
rospy.spin()
