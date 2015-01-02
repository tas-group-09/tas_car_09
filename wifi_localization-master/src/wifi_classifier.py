#!/usr/bin/env python

import roslib; roslib.load_manifest('wifi_lookup')
import rospy, pickle
from wifi_lookup.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance

dbLoc = "database.pk"

k = 3

def WifiCallback(data):
	global measurement_database
	global iteration_counter
	global k
	
	# Wait 10 Measurements
	if iteration_counter < 10:
		iteration_counter = iteration_counter + 1	
		for spot in data.HotSpots:
			#if spot.MAC not in measurement_database:
			measurement_database[spot.MAC] = spot.dB

		print iteration_counter,') The message contains',len(measurement_database.keys()),'hotspots'
	
	# Compute Location
	else:
		iteration_counter = 0
		
		print
		print 'The COMPLETE measurement database contains',len(measurement_database.keys()),'hotspots.'
		print		
		
		positions = database.keys()	
		database_entries = len(positions)
	
		minimalError = []
		minimalError_Position = []

		# initialize the minimal error for the k - nearest neighbour
		for i in range(0,k):
			minimalError.append(99999999)
			minimalError_Position.append((0,0))

		for position in positions:
			position_database = database[position]

			all_MAC_map = position_database.keys()
			all_MAC_measurements = measurement_database.keys()

			all_MAC = all_MAC_map
			
			# Merge all Mac addresses
			for measurement_MAC in all_MAC_measurements:
				if measurement_MAC not in all_MAC:
				PoseWithCovariance	all_MAC.append(measurement_MAC)
			
			# Reset the error
			error = 0		
			
			for MAC in all_MAC:
			
				# The Mac adress is within the position & measurement Database
				if MAC in measurement_database and MAC in position_database:
					
					# Euclidean Distance					
					# error = error + pow(position_database[MAC] - measurement_database[MAC],2)
					# Manhattan Distance
					error = error + abs(position_database[MAC]- measurement_database[MAC])

				# The Mac adress is ONLY in the position database
				elif MAC not in measurement_database and MAC in position_database :
					
					# Euclidean Distance					
					# error = error + pow(position_database[MAC] - 0,2)
					# Manhattan Distance
					error = error + abs(position_database[MAC]-0)
				

				# The Mac adress is ONLY in the measurement database
				elif MAC in measurement_database and MAC not in position_database:
					
					# Euclidean Distance					
					# error = error + pow(0 - measurement_database[MAC],2)
					# Manhattan Distance
					error = error + abs(0 - measurement_database[MAC])
				

				else:
					print 'SOMETHING BAD HAPPENED'	
	
			print '@ Position',position,'the error equals',error
		
			#Check wether the tested point is one of the k nearest Neighbours
			for i in range(0,k):

				if error < minimalError[i]:
					minimalError_Position[i] = position
					minimalError[i] = error
					break
 

			measurement_database = {}

		
		msg = PoseWithCovariance()
		
		x = 0
		y = 0
		
		for i in range(0,k):
			x = x + minimalError_Position[i][0]
			y = y + minimalError_Position[i][1]

		covariance = []
		for i in range(0,36):
			covariance.append(0)
		

		msg.pose.position.x = x/k
		msg.pose.position.y = y/k
		msg.pose.position.z = 0

		msg.pose.orientation.x = 0
		msg.pose.orientation.y = 0
		msg.pose.orientation.z = 0

		msg.covariance = covariance

		print '[',x,',',y,']'


#deserialize the object and do ROS things
def make():
	global database
	global pub = rospy.Publisher('initialLocation_TEST', PoseWithCovariance, queue_size=10)
	
	global measurement_database
	global iteration_counter


	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}
	
	measurement_database = {}
	iteration_counter = 0

	rospy.Subscriber('wifi_data', WifiData, WifiCallback)
	rospy.spin()

#Add publisher ROS things
if __name__=='__main__':
	rospy.init_node('wifi_classifier')
	try:
		make()
	except rospy.ROSInterruptException: pass
