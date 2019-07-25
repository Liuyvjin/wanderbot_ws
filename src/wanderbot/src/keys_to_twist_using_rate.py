#!/usr/bin/env python
#coding=utf-8
# 稳定命令流的键盘控制，收到按键则发送一条速度命令，否则发送0,0
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

key_mapping = {'w':[0,1], 's':[0,-1], 'a':[1,0], 'd':[-1,0], 'x':[0,0]}
def keys_cb(msg, t):
	if len(msg.data) == 0 or not key_mapping.has_key(msg.data[0]):
		return 
	vels = key_mapping[msg.data[0]]
	t.angular.z = vels[0]
	t.linear.x = vels[1]

if __name__ == '__main__':
	rospy.init_node('keys_to_twist')
	# 发布话题cmd_vel
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	# 订阅话题‘keys’，其中twist_pub是回调函数的参数
	t = Twist() 
	rospy.Subscriber('keys', String, keys_cb, t)

	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		if t.angular.z or t.linear.x:
			twist_pub.publish(t)
			is_rec_cmd = False
			t.angular.z = 0
			t.linear.x = 0
		else:
			twist_pub.publish(t)
		rate.sleep()