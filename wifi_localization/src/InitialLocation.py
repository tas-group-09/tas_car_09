#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from wiimote.msg import State

global publishLocation


def wiimote_callback(msg):

	global publishLocation

	if(msg.buttons[0] == 1):
		if(publishLocation == False):
			print 'Initial Location -> Published'
			
		publishLocation = True
	else:
		if(publishLocation == True):
			print 'Initial Location -> STOPPED Publishing'
		
		publishLocation = False



def publishInitialLocation():
	global publishLocation
    
	rospy.init_node('initialLocalization', anonymous=True)
    	rate = rospy.Rate(100) # 100hz

    	pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
 	
	while not rospy.is_shutdown():
		
		covariance = []
		for i in range(0,36):
			covariance.append(0)
		
		covariance[0] = 1
		covariance[7] = 1
		covariance[35] = 3

		msg = PoseWithCovarianceStamped()

		msg.header.stamp = rospy.get_rostime()

		msg.pose.pose.position.x = 11.7
		msg.pose.pose.position.y = 18.2
		msg.pose.pose.position.z = 0

		msg.pose.pose.orientation.x = 0
		msg.pose.pose.orientation.y = 0
		msg.pose.pose.orientation.z = -0.8
		msg.pose.pose.orientation.w = 0.81011023189

		msg.pose.covariance = covariance
		
		if(publishLocation == True):
			# publish message
			pub.publish(msg)

		#sleep
        	rate.sleep()


if __name__ == '__main__':
    	
	try:
		global publishLocation
		
		publishLocation = True

		rospy.Subscriber('wiimote/state',State,wiimote_callback)

        	publishInitialLocation()
    
	except rospy.ROSInterruptException:
        	pass

