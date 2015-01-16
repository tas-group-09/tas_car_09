#!/usr/bin/env python

#   ____________________________________________
#   |                                          |
#   |  Technik Autonomer Systeme -TUM          |
#   |  Gruppe 09                               |
#   |                                          |
#   |  erstellt: WS 2014/2015 - (c) Tim Stahl  |
#   |__________________________________________|

#  Inflation Radius von 0.25
#  scaling_offset = (std::abs((autonomous_control.cmd_steeringAngle)-1500))/25;


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
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from tf.transformations import quaternion_from_euler


global ranges
global increment 
global angle_min
global pose
global published
global pose_received		

# Read necessary scan data into variables
def scan_callback(msg):

	global ranges		# range data [m]
	global increment	# angular distance between measurements [rad]
	global angle_min        # start angle of the scan [rad]

	#print "SCAN CALLBACK"

	ranges = msg.ranges
	increment = msg.angle_increment
	angle_min = msg.angle_min


# Read necessary pose data into variables
def pose_callback(msg):

	global pose
	global pose_received

	pose = (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
	pose_received = True

# Send Scan Position to Path Planner
def sendScanPosition():
	rate = rospy.Rate(100) # 100hz

    	pub = rospy.Publisher('goals', Path, queue_size=10, latch=True)
	
	msg = Path()
	targetPose = PoseStamped()

	targetPose.header.frame_id = 'map'
	targetPose.header.stamp = rospy.get_rostime()

	targetPose.pose.position.x = 24.3
	targetPose.pose.position.y = 16.8
	targetPose.pose.position.z = 0

	quaternion = quaternion_from_euler(0,0,-90 *math.pi/180)

	targetPose.pose.orientation.x = quaternion[0]
	targetPose.pose.orientation.y = quaternion[1]
	targetPose.pose.orientation.z = quaternion[2]
	targetPose.pose.orientation.w = quaternion[3]

	msg.poses.append(targetPose)

	pub.publish(msg)

	

# Calculate waypoints
def calculateWaypoints():
	global ranges
	global increment
	global angle_min
	global pose
	global pose_received
	global published
    
    	rate = rospy.Rate(100) # 100hz

    	pub = rospy.Publisher('goals', Path, queue_size=10, latch=True)
 	
	while not (rospy.is_shutdown()):
		
		# If pose and ranges received         and not published      and near scan position
		if (pose_received and len(ranges) > 0 and published == False and pose[1] < 17.7):

			# PARAMETERS FOR OBJECT DETECTION AND WAYPOINT GENERATION
			detection_offset = 0.4		# Distance which pylons are (min.) closer than the wall; half hall width recomended
			object_tolerance = 0.15		# Max. variance (+/-) of distances for same object
			max_width_object = 0.15		# Max. witdh of detected objects (in m)	
			max_nmb_objects  = 4		# Max. number of detected objects	
			waypoint_offset = 0.4		# Distance how far waypoint is set away from pylon (affects WP1, WP3 and WP5)	
			radius_pylon = 0.03		# Radius of Pylon (on scanner height)


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
					print "Object-Candidate found (Distance: ", ranges[i+1], ")"
					max_width_object_frames = (math.atan(max_width_object/(2*ranges[temp_i])*2)//increment)
					
					while (ranges[temp_i] < (ranges[i+1] + object_tolerance)) and (ranges[temp_i] > (ranges[i+1] - object_tolerance)) and (i <= (temp_i + max_width_object_frames)) and (i < len(ranges)-1):
						i += 1

					# Check if object is small enough and detection_offset is also fulfilled
					if ((i <= temp_i + max_width_object_frames) and ((ranges[i+1]+ranges[i+2]+ranges[i+3]+ranges[i+4])/4 > (ranges[temp_i] + detection_offset))):
						detected_objects_distance.append(ranges[temp_i + (i-temp_i)//2])
						detected_objects_increment.append(increment * 180 / math.pi * (temp_i + (i-temp_i)//2))
						nmb_detected_objects += 1
						print "-> Candidate selected"
						print

					if not (i <= temp_i + max_width_object_frames):				
						print "Error: Objectwidth to large = ", 2*ranges[temp_i]*math.tan(((i - temp_i)*increment)/2)
						print
					if not ((ranges[i+1]+ranges[i+2]+ranges[i+3]+ranges[i+4])/4 > (ranges[temp_i] + detection_offset)):
						print "Error: Distance to wall too small"
						print "Distance to object: ", ranges[temp_i]
						print "Distance to wall (Avrg. nxt 4 Values): ", (ranges[i+1]+ranges[i+2]+ranges[i+3]+ranges[i+4])/4
						print 

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
					
					# Correction factor to get pylon point into center of object
					correction_factor = (1 + radius_pylon/detected_objects_distance[i])					

					detected_objects_points.append((pose[0] + detected_objects_distance[i] * correction_factor * math.cos(alpha * math.pi / 180), pose[1] + detected_objects_distance[i] * correction_factor * math.sin(alpha * math.pi/180)))

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
					
					# If second Pylon was recognized as first one (due to hardware issues / faulty scan data)
					if (detected_objects_distance[i] > 1.2):
						reference_point = (detected_objects_points[i][0] - target_vector[0], detected_objects_points[i][1] - target_vector[1])			
					else:
						reference_point = detected_objects_points[i]   # Reference point is first pylon


					# Calculate waypoints between each pylon
					
					waypoints[0] = (reference_point[0] + target_vector[0]/2, reference_point[1] + target_vector[1]/2)
					waypoints[2] = (reference_point[0] + 3*target_vector[0]/2, reference_point[1] + 3*target_vector[1]/2)
					waypoints[4] = (reference_point[0] + 5*target_vector[0]/2, reference_point[1] + 5*target_vector[1]/2)
					waypoints[6] = (reference_point[0] + 9*target_vector[0]/2, reference_point[1] + 9*target_vector[1]/2)

					# Calculate orthogonal vector in relation to target vector (applying cross product)
					norm_factor = waypoint_offset / numpy.sqrt(target_vector[0]**2 + target_vector[1]**2)
					orthogonal_target_vector =  (norm_factor * target_vector[1], norm_factor * (-target_vector[0]))

					# Calculate waypoints besides each pylon
					waypoints[1] = (reference_point[0] + target_vector[0] + orthogonal_target_vector[0], reference_point[1] + target_vector[1] + orthogonal_target_vector[1])
					waypoints[3] = (reference_point[0] + 2*target_vector[0] - orthogonal_target_vector[0], reference_point[1] + 2*target_vector[1] - orthogonal_target_vector[1])
					waypoints[5] = (reference_point[0] + 3*target_vector[0] + orthogonal_target_vector[0] +0.05, reference_point[1] + 3*target_vector[1] + orthogonal_target_vector[1])
					
					print
					print "Calculated Waypoints: ", waypoints
					print
					
					# For debuging reasons
					#print "Pose: ", pose
					#print "Ranges: ", ranges
					#print

					# Publish all waypoints
					msg = Path()

					for i in range(7):

						wpts = PoseStamped()

						wpts.header.frame_id = 'map'
						wpts.header.stamp = rospy.get_rostime()

	
						wpts.pose.position.x = waypoints[i][0]
						wpts.pose.position.y = waypoints[i][1]
						wpts.pose.position.z = 0
					

						wpts_quaternion = quaternion_from_euler(0,0,-94 *math.pi/180)


						wpts.pose.orientation.x = wpts_quaternion[0]
						wpts.pose.orientation.y = wpts_quaternion[1]
						wpts.pose.orientation.z = wpts_quaternion[1]
						wpts.pose.orientation.w = wpts_quaternion[2]
			
						msg.poses.append(wpts)

					if(published == False):
						#print msg
						pub.publish(msg)
						published = True

		#sleep
        	#rate.sleep()
	rospy.spin()


if __name__ == '__main__':
    	
	try:
		global pose_received
		global published
		pose_received = False
		published = False

		print 'Slalom went Active'

		ranges = []
		pose = (99,99,99,99)

    		rospy.init_node('slalomPlanner', anonymous=True)

    
		rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,pose_callback)
		rospy.Subscriber('scan',LaserScan,scan_callback)

		sendScanPosition()		

        	calculateWaypoints()
    
	except rospy.ROSInterruptException:
        	pass

