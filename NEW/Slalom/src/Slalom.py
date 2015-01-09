#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import LaserScan

global ranges
global increment 


def Lidar_callback(msg):

	global ranges
	global increment

	ranges = msg.ranges
	increment = msg.angle_increment


def nextWaypoint():
	global ranges
	global increment
    
	rospy.init_node('SlalomWaypoints', anonymous=True)
    	rate = rospy.Rate(100) # 100hz

    	pub = rospy.Publisher('nextWaypoint', Pose, queue_size=10)
 	
	while not rospy.is_shutdown():
		
		print ranges[1]

		# INSERT YOUR CODE

		msg = Pose()

		msg.pose.position.x = 11.7
		msg.pose.position.y = 18.2
		msg.pose.position.z = 0

		msg.pose.orientation.x = 0
		msg.pose.orientation.y = 0
		msg.pose.orientation.z = -0.8
		msg.pose.orientation.w = 0.81011023189
		
		pub.publish(msg)

		#sleep
        	rate.sleep()


if __name__ == '__main__':
    	
	try:
		
		publishLocation = True

		#rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,injectLocation)
		rospy.Subscriber('scan',wiimote_callback)

        	publishInitialLocation()
    
	except rospy.ROSInterruptException:
        	pass

