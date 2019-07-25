#!/usr/bin/env python
#coding=utf-8
# 稳定命令流的键盘控制，收到按键则发送一条速度命令，否则发送上条命令
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

g_last_Twist = None
key_mapping = {'w':[0,1], 's':[0,-1], 'a':[1,0], 'd':[-1,0], 'x':[0,0]}
# 回调函数
def keys_cb(msg, twist_pub):
	global g_last_Twist
	if len(msg.data) == 0 or not key_mapping.has_key(msg.data[0]):
		return 
	vels = key_mapping[msg.data[0]]
	g_last_Twist.angular.z = vels[0]
	g_last_Twist.linear.x = vels[1]
	#twist_pub.publish(g_last_Twist)

if __name__ == '__main__':
	rospy.init_node('keys_to_twist')
	# 发布话题cmd_vel
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	# 订阅话题‘keys’，其中twist_pub是回调函数的参数
	rospy.Subscriber('keys', String, keys_cb, twist_pub)

	rate = rospy.Rate(10)
	g_last_Twist = Twist()
	while not rospy.is_shutdown():
		twist_pub.publish(g_last_Twist)
		rate.sleep()