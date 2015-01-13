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

#new comment
import re
def replace(re1,re2):
    doc = window.get_active_document()
    start, end = doc.get_bounds()
    txt = start.get_slice(end)      
    newtxt = re.sub(re1,re2,txt)    
    doc.set_text(newtxt)

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
    



if __name__ == '__main__':

	global ranges
	global increment
	global angle_min
	global pose

	# DEFINE TEST PARAMETERS
	print "Defining parameters..."
	pose = (0, 0, 0, 0)
	ranges =(0.558000,0.557000,0.557000,0.556000,0.556000,0.554000,0.556000,0.554000,0.554000,0.548000,0.548000,0.548000,0.555000,0.555000,0.555000,0.556000,0.556000,0.553000,0.553000,0.553000,0.552000,0.552000,0.550000,0.550000,0.550000,0.551000,0.552000,0.552000,0.552000,0.552000,0.551000,0.547000,0.546000,0.546000,0.543000,0.546000,0.546000,0.547000,0.550000,0.554000,0.550000,0.550000,0.546000,0.546000,0.546000,0.546000,0.546000,0.553000,0.553000,0.547000,0.545000,0.547000,0.545000,0.547000,0.547000,0.547000,0.547000,0.547000,0.547000,0.555000,0.555000,0.555000,0.553000,0.553000,0.553000,0.559000,0.562000,0.562000,0.559000,0.559000,0.555000,0.555000,0.559000,0.566000,0.566000,0.566000,0.559000,0.558000,0.558000,0.559000,0.563000,0.563000,0.563000,0.563000,0.560000,0.560000,0.560000,0.572000,0.572000,0.572000,0.570000,0.570000,0.559000,0.568000,0.568000,0.568000,0.562000,0.568000,0.568000,0.568000,0.565000,0.565000,0.563000,0.563000,0.563000,0.569000,0.573000,0.573000,0.573000,0.574000,0.577000,0.581000,0.581000,0.580000,0.577000,0.580000,0.580000,0.577000,0.582000,0.582000,0.579000,0.579000,0.584000,0.584000,0.584000,0.586000,0.588000,0.588000,0.589000,0.590000,0.596000,0.596000,0.596000,0.596000,0.598000,0.592000,0.600000,0.600000,0.592000,0.592000,0.603000,0.605000,0.606000,0.610000,0.610000,0.610000,0.612000,0.612000,0.615000,0.615000,0.612000,0.610000,0.610000,0.610000,0.619000,0.619000,0.619000,0.620000,0.619000,0.620000,0.620000,0.632000,0.633000,0.634000,0.633000,0.632000,0.634000,0.634000,0.646000,0.651000,0.653000,0.653000,0.653000,0.654000,0.654000,0.654000,0.661000,0.662000,0.664000,0.665000,0.666000,0.666000,0.666000,0.666000,0.667000,0.674000,0.676000,0.684000,0.684000,0.685000,0.685000,0.685000,0.685000,0.686000,0.690000,0.697000,0.697000,0.704000,0.707000,0.707000,0.707000,0.707000,0.704000,0.704000,0.704000,0.712000,0.718000,0.730000,0.730000,0.730000,0.731000,0.733000,0.733000,0.745000,0.745000,0.746000,0.746000,0.741000,0.735000,0.732000,0.732000,0.728000,0.728000,0.728000,0.729000,0.727000,0.729000,0.727000,0.730000,0.726000,0.723000,0.723000,0.723000,0.723000,0.723000,0.730000,0.801000,2.513000,2.513000,2.513000,2.502000,2.486000,2.474000,2.465000,2.458000,2.437000,2.430000,2.429000,2.427000,2.424000,2.413000,2.395000,2.395000,2.392000,2.390000,2.387000,2.387000,2.373000,2.370000,2.370000,2.369000,2.363000,2.361000,2.361000,2.361000,2.360000,2.360000,2.361000,2.364000,2.365000,2.366000,2.366000,2.366000,2.366000,2.366000,2.301000,2.181000,2.161000,2.152000,2.148000,2.136000,2.132000,2.126000,2.126000,2.118000,2.118000,2.105000,2.105000,2.104000,2.102000,2.101000,2.085000,2.078000,2.075000,2.072000,2.066000,2.063000,2.054000,2.053000,2.050000,2.045000,2.030000,2.024000,1.869000,1.752000,1.714000,1.690000,1.683000,1.660000,1.657000,1.657000,1.656000,1.651000,1.648000,1.637000,1.635000,1.634000,1.634000,1.633000,1.633000,1.623000,1.621000,1.618000,1.618000,1.615000,1.615000,1.610000,1.609000,1.609000,1.610000,1.630000,1.712000,1.791000,1.811000,1.827000,1.861000,1.897000,1.926000,1.967000,1.984000,2.010000,2.049000,2.076000,2.118000,2.150000,2.192000,2.223000,2.275000,2.310000,2.348000,2.392000,2.441000,2.486000,2.537000,2.589000,2.643000,2.705000,2.754000,2.808000,2.881000,2.938000,3.016000,3.090000,3.181000,3.278000,3.355000,3.420000,3.527000,3.638000,3.767000,3.879000,3.899000,3.902000,3.904000,3.904000,3.904000,3.905000,3.906000,3.905000,3.906000,3.906000,3.919000,3.948000,4.038000,4.175000,4.265000,7.652000,7.828000,8.833000,8.833000,8.845000,11.366000,11.408000,11.427000,11.438000,11.444000,11.504000,14.151000,14.151000,float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),17.959000,17.981001,17.981001,17.9336000,17.9336000,17.9336000,14.170000,14.170000,14.170000,14.053000,13.392000,13.372000,13.372000,13.393000,13.393000,13.406000,13.406000,13.406000,13.406000,12.028000,12.010000,12.010000,12.014000,12.019000,12.036000,12.036000,float("inf"),float("inf"),float("inf"),float("inf"),8.046000,8.046000,7.849000,7.617000,7.465000,7.217000,7.003000,6.892000,6.781000,6.636000,6.495000,6.353000,6.282000,4.496000,4.496000,4.496000,5.673000,5.673000,5.570000,5.464000,5.357000,5.262000,5.183000,5.121000,5.018000,4.933000,4.862000,4.776000,4.704000,4.633000,4.600000,4.599000,4.599000,4.599000,4.614000,4.626000,4.632000,4.632000,4.632000,2.932000,2.924000,2.924000,2.924000,2.952000,4.688000,4.690000,4.698000,4.698000,4.698000,4.698000,4.696000,4.687000,4.672000,4.632000,4.577000,4.533000,4.472000,4.437000,4.407000,4.347000,4.305000,4.265000,4.218000,4.193000,4.148000,4.097000,4.072000,4.017000,3.990000,3.959000,3.931000,3.898000,3.861000,3.829000,3.795000,3.762000,3.745000,3.721000,3.688000,3.640000,3.621000,3.581000,3.561000,3.529000,3.511000,3.476000,3.450000,3.437000,3.410000,3.379000,3.370000,3.261000,3.260000,3.248000,3.248000,3.242000,3.231000,3.202000,3.181000,3.144000,3.134000,3.117000,3.093000,3.084000,3.062000,3.047000,3.028000,2.992000,2.988000,2.965000,2.946000,2.935000,2.930000,2.906000,2.884000,2.873000,1.547000,1.517000,1.516000,1.516000,1.526000,1.516000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.620000,2.620000,2.614000,2.606000,2.594000,2.582000,2.556000,2.546000,2.536000,2.528000,2.523000,2.522000,2.506000,2.492000,2.472000,2.456000,2.451000,2.447000,2.435000,2.422000,2.422000,2.419000,2.405000,2.391000,2.382000,2.367000,2.366000,2.349000,2.341000,2.334000,2.318000,2.315000,2.307000,2.301000,2.292000,2.282000,2.276000,2.274000,2.260000,2.254000,2.237000,2.232000,2.224000,2.218000,2.204000,2.202000,2.185000,2.185000,2.183000,2.182000,2.178000,2.172000,2.162000,2.138000,2.106000,2.106000,2.106000,2.106000,2.088000,2.091000,2.091000,2.091000,2.091000,2.091000,2.088000,2.081000,2.079000,2.076000,2.070000,2.066000,2.043000,2.043000,2.043000,2.042000,2.042000,2.026000,2.022000,2.022000,2.020000,2.016000,2.011000,2.007000,1.990000,1.990000,1.988000,1.985000,1.985000,1.980000,1.972000,1.966000,1.962000,1.962000,1.954000,1.952000,1.950000,1.944000,1.939000,1.939000,1.935000,1.935000,1.924000,1.920000,1.920000,1.919000,1.919000,1.914000,1.914000,1.906000,1.895000,1.895000,1.894000,1.893000,1.891000,1.883000,1.875000,1.874000,1.872000,1.871000,1.866000,1.865000,1.859000,1.856000,1.853000,1.852000,1.850000,1.845000,1.842000,1.837000,1.842000,1.836000,1.830000,1.833000,1.833000,1.830000,1.828000,1.820000,1.819000,1.819000,1.819000,1.819000,1.819000,1.819000,1.818000,1.812000,1.806000,1.803000,1.800000,1.795000,1.793000,1.793000)
	increment = 0.004363
	angle_min = -1.570796

	# PARAMETERS FOR OBJECT DETECTION
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
	
	print "Processing data..."
	while i < (len(ranges) - 1):
		
		# Check if next range is closer than defined value and not compared to infinity (often faulty data)
		if (ranges[i+1] < (ranges[i] - detection_offset)) and (ranges[i] < 999):
			temp_i = i + 1
	
			while (ranges[temp_i] < (ranges [i+1] + object_tolerance)) and (ranges[temp_i] > (ranges [i+1] - object_tolerance)) and (i <= (temp_i + max_width_object)) and (i < len(ranges)-1):
				i += 1
			
			# Check if object is small enough and detection_offset is also fulfilled
			if ((i <= temp_i + max_width_object) and (ranges[i+1] > (ranges[temp_i] + detection_offset))):
				detected_objects_distance.append(ranges[temp_i + (i-temp_i)//2])
				detected_objects_increment.append(increment * (temp_i* 180 / math.pi + (i-temp_i)//2))
				nmb_detected_objects += 1
				#print "Object detected (Distance: ", ranges[temp_i], ", Value-No.: ", temp_i
			i += 1	
		else:
			i += 1
	
	print "Analyze complete..."

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
		
		# Print detected objects
		i = 0		
		while i < nmb_detected_objects:
			print "Object ", i, ": ", detected_objects_points[i]
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

			
			# Print evaluated waypoints
			i = 0		
			while i <= 6:
				print "waypoint ", i, ": ", waypoints[i]
				i += 1
