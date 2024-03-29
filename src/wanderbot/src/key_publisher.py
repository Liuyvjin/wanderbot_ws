#!/usr/bin/env python
#coding=utf-8
# 检测按键，并发送到话题'keys'
import sys, select, tty, termios
import rospy
from std_msgs.msg import String

if __name__ == '__main__':
	key_pub = rospy.Publisher('keys',String, queue_size=1)
	rospy.init_node("keyboard_driver")
	rate = rospy.Rate(50)
	old_attr = termios.tcgetattr(sys.stdin) 
	tty.setcbreak(sys.stdin.fileno())
	print("Publishing keystrokes. Press Ctrl-C to exit...")

	while not rospy.is_shutdown():
		if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
			c = sys.stdin.read(1)
			key_pub.publish(c)
		rate.sleep()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)