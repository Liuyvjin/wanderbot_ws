#!/usr/bin/env python
#coding=utf-8
# 考虑加速度，让机器人平稳起步与减速
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

key_vels = [0,0]
# 按键对照表
key_mapping = {'w':[0,1], 's':[0,-1], 'a':[1,0], 'd':[-1,0], 'x':[0,0]}

def keys_cb(msg):
	global key_vels
	if len(msg.data) == 0 or not key_mapping.has_key(msg.data[0]):
		return 
	key_vels = key_mapping[msg.data[0]]

	
if __name__ == '__main__':
	rospy.init_node('keys_to_twist')
	# 分别保存按键值和速度
	t = Twist()
	acc = 0.1  #加速度 
	# 发布话题cmd_vel
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	# 订阅话题‘keys’，其中twist_pub是回调函数的参数
	rospy.Subscriber('keys', String, keys_cb)
	
	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		t.linear.x = max(min(key_vels[1]*acc+t.linear.x, 1),-1)
		t.angular.z = max(min(key_vels[0]*acc+t.angular.z, 1),-1)
		twist_pub.publish(t)
		rate.sleep()