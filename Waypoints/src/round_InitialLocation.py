#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseWithCovarianceStamped
from wiimote.msg import State
from tf.transformations import euler_from_quaternion
from tf.transformations import quaternion_from_euler

global publishLocation 

def injectLocation(msg):
	
	global publishLocation
	
	injectLoc = (msg.pose.pose.position.x,msg.pose.pose.position.y)
	print publishLocation, injectLoc
	
	if(abs(injectLoc[0]-11.7) < 0.05 and abs(injectLoc[1]-18.2)):
		publishLocation = False


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

    		quaternion = quaternion_from_euler(0, 0, (-90.0 /180.0) * math.pi)

		msg.pose.pose.orientation.x = quaternion[0]
		msg.pose.pose.orientation.y = quaternion[1]
		msg.pose.pose.orientation.z = quaternion[2]
		msg.pose.pose.orientation.w = quaternion[3]

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

		#rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,injectLocation)
		rospy.Subscriber('wiimote/state',State,wiimote_callback)

        	publishInitialLocation()
    
	except rospy.ROSInterruptException:
        	pass

