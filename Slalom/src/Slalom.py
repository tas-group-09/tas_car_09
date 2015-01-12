#!/usr/bin/env python

#   ____________________________________________
#   |                                          |
#   |  Technik Autonomer Systeme -TUM          |
#   |  Gruppe 09                               |
#   |                                          |
#   |  erstellt: WS 2014/2015 - (c) Tim Stahl  |
#   |__________________________________________|


### INFO - Waypoints Slalom
###|           |########
###|     6     |========
###|
###|
###|
###|     P  5
###|           |========
###|     4     |########
###|           |##
###|  3  P     |##
###|           |##
###|     2     |##
###|           |##
###|     P  1  |##
###|           |##
###|     0     |##
###|           |##
###|  X  P     |##
###|           |##   1,2,3,...: Waypoint No. 1,2,3,...
###|   _____   |##   P: Pylon
###|   | S |   |##   S: Start
###|   |   |   |##   X: Scan Position

import rospy
import math
import numpy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from tf.transformations import quaternion_from_euler


global ranges
global increment 
global angle_min
global pose

# Read necessary scan data into variables
def scan_callback(msg):

	global ranges		# range data [m]
	global increment	# angular distance between measurements [rad]
	global angle_min        # start angle of the scan [rad]

	ranges = msg.ranges
	increment = msg.angle_increment
	angle_min = msg.amgle_min

# Read necessary pose data into variables
def pose_callback(msg):

	global pose

	pose = (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)

# Calculate waypoints
def calculateWaypoints():
	global ranges
	global increment
	global angle_min
	global pose
    
	rospy.init_node('SlalomWaypoints', anonymous=True)
    	#rate = rospy.Rate(100) # 100hz

    	pub = rospy.Publisher('SlalomWaypointData', Pose, queue_size=10)
 	
	while not rospy.is_shutdown():

		# PARAMETERS FOR OBJECT DETECTION AND WAYPOINT GENERATION
		detection_offset = 0.8		# Distance which pylons are (min.) closer than the wall; half hall width recomended
		object_tolerance = 0.15		# Max. variance (+/-) of distances for same object
		max_width_object = 5		# Max. witdh of detected objects, expressed by number of scanned frames (approximation)	
		max_nmb_objects  = 4		# Max. number of detected objects	
		waypoint_offset = 0.4		# Distance how far waypoint is set away from pylon (affects WP1, WP3 and WP5)	


		# DETERMINE OBJECTS IN RANGE

		# Variables
		i = 1
		nmb_detected_objects = 0
		detected_objects_distance = []	# All detected objects with distance to car
		detected_objects_increment = []	# All detected objects with increment (referenced to angle_min)
		detected_objects_points = []	# Coordniates of all detected points (in local map)
		target_vector = []		# Vector pointing from one pylon to the next one
		waypoints = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]		# Waypoints with each [x, y]

		while i < (len(ranges) - 1):
			# Check if next range is closer than defined value and not compared to infinity (often faulty data)
			if (ranges[i+1] < (ranges [i] - detection_offset)) and (ranges[i] < 999):
				temp_i = i+1
				while (ranges[temp_i] < (ranges[i+1] + object_tolerance)) and (ranges[temp_i] > (ranges[i+1] - object_tolerance)) and (i <= (temp_i + max_width_object)) and (i < len(ranges)-1):
					i += 1

				# Check if object is small enough and detection_offset is also fulfilled
				if ((i <= temp_i + max_width_object) and (ranges[i+1] > (ranges[temp_i] + detection_offset))):
					detected_objects_distance.append(ranges[temp_i + (i-temp_i)//2])
					detected_objects_increment.append(increment * 180 / math.pi * (temp_i + (i-temp_i)//2))
					nmb_detected_objects += 1
				i += 1
			else:
				i += 1

		if (nmb_detected_objects < 2) or (nmb_detected_objects > max_nmb_objects):
			print "Error: number of objects not in the permitted range (Detected objects: ", nmb_detected_objects, ")"

		else:
			print "Success: ", nmb_detected_objects, " objects detected"

			# Transform points of detected objects into map
			i = 0			
			while i < nmb_detected_objects:
				
				(unused1, unused2, alpha) = euler_from_quaternion((0,0,pose[2],pose[3]))
				alpha = alpha * 180 / math.pi + (detected_objects_increment[i] + angle_min * 180 / math.pi)

				detected_objects_points.append((pose[0] + detected_objects_distance[i] * math.cos(alpha * math.pi / 180), pose[1] + detected_objects_distance[i] * math.sin(alpha * math.pi/180)))

				i += 1

			# Calculate and evaluate frequency / distance of detected points
			i = 0	
			mean_distance = 0		
			while i < (nmb_detected_objects - 1):
				# Calculate eucledian distance between current and next point
				distance = numpy.sqrt((detected_objects_points[i][0]-detected_objects_points[i+1][0])**2 + (detected_objects_points[i][1]-detected_objects_points[i+1][1])**2)
				
				# Calculate floating mean value
				mean_distance = mean_distance - (mean_distance - distance)/(i+1)

				i += 1
			
			if (mean_distance < 1) or (mean_distance > 2):
				print "Error: calculated mean_distance between objects out of range [1m, 2m]"
			
			else:
				print "Calculated mean distance between objects: ", mean_distance, "m"
				
				# Select reference point with shortest distance to car
				i = detected_objects_distance.index(min(detected_objects_distance))
				
				# Determine target vector (from first pylon to second)
				if i > 0:
					target_vector = (detected_objects_points[i-1][0] - detected_objects_points[i][0], detected_objects_points[i-1][1] - detected_objects_points[i][1])
				else:
					target_vector = (detected_objects_points[i+1][0] - detected_objects_points[i][0], detected_objects_points[i+1][1] - detected_objects_points[i][1])

				# Calculate waypoints between each pylon
				reference_point = detected_objects_points[i]   # Reference point is first pylon
				waypoints[0] = (reference_point[0] + target_vector[0]/2, reference_point[1] + target_vector[1]/2)
				waypoints[2] = (reference_point[0] + 3*target_vector[0]/2, reference_point[1] + 3*target_vector[1]/2)
				waypoints[4] = (reference_point[0] + 5*target_vector[0]/2, reference_point[1] + 5*target_vector[1]/2)
				waypoints[6] = (reference_point[0] + 7*target_vector[0]/2, reference_point[1] + 7*target_vector[1]/2)

				# Calculate orthogonal vector in relation to target vector (applying cross product)
				norm_factor = waypoint_offset / numpy.sqrt(target_vector[0]**2 + target_vector[1]**2)
				orthogonal_target_vector =  (norm_factor * target_vector[1], norm_factor * (-target_vector[0]))

				# Calculate waypoints besides each pylon
				waypoints[1] = (reference_point[0] + target_vector[0] + orthogonal_target_vector[0], reference_point[1] + target_vector[1] + orthogonal_target_vector[1])
				waypoints[3] = (reference_point[0] + 2*target_vector[0] - orthogonal_target_vector[0], reference_point[1] + 2*target_vector[1] - orthogonal_target_vector[1])
				waypoints[5] = (reference_point[0] + 3*target_vector[0] + orthogonal_target_vector[0], reference_point[1] + 3*target_vector[1] + orthogonal_target_vector[1])


			# Publish all waypoints
			i = 0
			while i <= 6:
				msg = Pose()

				msg.pose.position.x = waypoints[i][0]
				msg.pose.position.y = waypoints[i][1]
				msg.pose.position.z = 0

				msg.pose.orientation.x = 0
				msg.pose.orientation.y = 0
				msg.pose.orientation.z = -0.586
				msg.pose.orientation.w = 0.81011023189
		
				pub.publish(msg)

		#sleep
        	rate.sleep()


if __name__ == '__main__':
    	
	try:
		
		rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,pose_callback)
		rospy.Subscriber('scan',scan_callback)

        	calculateWaypoints()
    
	except rospy.ROSInterruptException:
        	pass

