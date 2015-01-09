#!/usr/bin/env python

import roslib;
import rospy, pickle
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance

dbLoc = "/home/michael/catkin/src/Wifi_Localization/wifiMap.pk"

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
		
		#print
		#print 'The COMPLETE measurement database contains',len(measurement_database.keys()),'hotspots.'
		#print

		#measurement_database = {'d':7,'b':7,'c':7}	

		#print database
		#print
		#print
		#print measurement_database
		#print
		#print	
		
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
					all_MAC.append(measurement_MAC)
			

			# Reset the error
			error = 0

			#print
			#print
			#print 'Calculate Error for Position ', position
			#print 'Position Database is', position_database
			#print 'Measured Database is', measurement_database
			#print 'All known Mac Adresses for the known Position are ', all_MAC
			
			for MAC in all_MAC:
			
				# The Mac adress is within the position & measurement Database
				if MAC in measurement_database and MAC in position_database:
					
					# Euclidean Distance					
					# error = error + pow(position_database[MAC] - measurement_database[MAC],2)
					# Manhattan Distance
					error = error + abs(position_database[MAC]- measurement_database[MAC])
					#print 'both databases', error


				# The Mac adress is ONLY in the position database
				elif MAC not in measurement_database and MAC in position_database :
					
					# Euclidean Distance					
					# error = error + pow(position_database[MAC] - 0,2)
					# Manhattan Distance
					error = error + abs(position_database[MAC]-0)
					#print 'only position database ',error
				

				# The Mac adress is ONLY in the measurement database
				elif MAC in measurement_database and MAC not in position_database:
					
					# Euclidean Distance					
					# error = error + pow(0 - measurement_database[MAC],2)
					# Manhattan Distance
					error = error + abs(0 - measurement_database[MAC])
					#print 'only measurement', error
				

				else:
					print 'SOMETHING BAD HAPPENED'	
	
			#print
			#print			
			#print '@ Position',position,'the error equals',error
			#print 'The k NN are =',minimalError_Position
			#print 'The k NN Error is =',minimalError
		
			#Check wether the tested point is one of the k nearest Neighbours
			for i in range(0,k):

				if error < minimalError[i]:
					#print 
					#print 'insert @',i
		
					minimalError_Position.insert(i, position)
					removedElement = minimalError_Position.pop()

					minimalError.insert(i, error)
					removedElement = minimalError.pop()
					break
			#print
			#print
 

		measurement_database = {}
		
		#print 'Final',k, 'Nearest Neighbours:'
		#print 'The k NN are =',minimalError_Position
		#print 'The k NN Error is =',minimalError
		#print

		x = 0
		y = 0

		for i in range(0,k):
			x = x + minimalError_Position[i][0]
			y = y + minimalError_Position[i][1]

		#print 'Sum x = ', x, 'Sum y = ', y

		x = 1.0*x/k
		y = 1.0*y/k

		print
		print
		print 'Best Location = [',x,',',y,']'
		print
		#print
		#print
		#print

		covariance = []
		for i in range(0,36):
			covariance.append(0)
		

		msg = PoseWithCovariance()
	
		msg.pose.position.x = x
		msg.pose.position.y = y
		msg.pose.position.z = 0

		msg.pose.orientation.x = 0
		msg.pose.orientation.y = 0
		msg.pose.orientation.z = 0

		msg.covariance = covariance
		


		pub.publish(msg)


# load the database
def make():
	global database
	global pub
	
	global measurement_database
	global iteration_counter

	pub = rospy.Publisher('initialLocation_TEST', PoseWithCovariance, queue_size=10)

	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}

	#database = {}
	#database[(0,0)] = {'a':1,'b':1, 'c':1}
	#database[(1,1)] = {'a':2,'b':2, 'c':2}
	#database[(2,2)] = {'a':3,'b':3, 'c':3}
	#database[(3,3)] = {'a':4,'b':4, 'c':4}
	#database[(4,4)] = {'a':5,'b':5, 'c':5}
	#database[(5,5)] = {'a':6,'b':6, 'c':6}
	#database[(6,6)] = {'a':7,'b':7, 'c':7}
	#database[(7,7)] = {'a':8,'b':8, 'c':8}
	
	measurement_database = {}
	iteration_counter = 0

	rospy.Subscriber('wifi_data', WifiData, WifiCallback)
	rospy.spin()


# tbd
if __name__=='__main__':
	rospy.init_node('wifi_classifier')
	try:
		make()
	except rospy.ROSInterruptException: pass
