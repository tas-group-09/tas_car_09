#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovariance

def publishInitialLocation():
    
	rospy.init_node('initialLocalization', anonymous=True)
    	rate = rospy.Rate(10) # 10hz

    	pub = rospy.Publisher('amcl_pose', PoseWithCovariance, queue_size=10)
 	
	while not rospy.is_shutdown():
		
		covariance = []
		for i in range(0,36):
			covariance.append(0)
		

		msg = PoseWithCovariance()

		msg.pose.position.x = 0
		msg.pose.position.y = 0
		msg.pose.position.z = 0

		msg.pose.orientation.x = 0
		msg.pose.orientation.y = 0
		msg.pose.orientation.z = 0

		msg.covariance = covariance
		
		# publish message
		pub.publish(msg)

		#sleep
        	rate.sleep()


if __name__ == '__main__':
    	
	try:
        	publishInitialLocation()
    
	except rospy.ROSInterruptException:
        	pass

