#!/usr/bin/env python

import roslib; roslib.load_manifest('wifi_lookup')
import rospy, pickle
from wifi_lookup.msg import WifiData, Wifi
from std_msgs.msg import String

#1st goal, Completed, load database from other node
#2nd goal, Create publisher framework for pose messages
#3rd goal, perform 2-D lookup and set comprehension to create location
dbLoc = "database.pk"

#create proper handler function to append new hotspots to data object
def repeat(data):
	global measurement_database
	global iteration_counter
	
	if iteration_counter < 10:
		iteration_counter = iteration_counter + 1	
		for spot in data.HotSpots:
			#if spot.MAC not in measurement_database:
			measurement_database[spot.MAC] = spot.dB

		print iteration_counter,') The message contains',len(measurement_database.keys()),'hotspots'

	else:
		iteration_counter = 0
		print
		print 'The COMPLETE measurement database contains',len(measurement_database.keys()),'hotspots.'
		print		
		
		positions = database.keys()	
		database_entries = len(positions)
	
		#print 'Position list[',database_entries,'] =',positions
		minimal_error = 999999
		minimal_error_position = [99,99]
		
		for position in positions:
			position_database = database[position]

			all_MAC_map = position_database.keys()
			all_MAC_measurements = measurement_database.keys()

			all_MAC = all_MAC_map

			for measurement_MAC in all_MAC_measurements:
				if measurement_MAC not in all_MAC:
					all_MAC.append(measurement_MAC)
			
			error = 0		
			
			for MAC in all_MAC:
			
				if MAC in measurement_database and MAC in position_database:
					error = error + pow(position_database[MAC] - measurement_database[MAC],2)
				elif MAC not in measurement_database and MAC in position_database :
					error = error + pow(position_database[MAC] - 0,2)
				elif MAC in measurement_database and MAC not in position_database:
					error = error + pow(0 - measurement_database[MAC],2)
				else:
					print 'SOMETHING BAD HAPPENED'	
	
			print '@ Position',position,'the error equals',error
		
			if error < minimal_error:
				minimal_error_position = position
				minimal_error = error 

			measurement_database = {}

		print			
		print minimal_error_position
		print

	#pub.publish(String("Message"))


#deserialize the object and do ROS things
def make():
	global database
	global pub
	
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

	#print database
	pub = rospy.Publisher('wifi_test', String)
	rospy.Subscriber('wifi_data', WifiData, repeat)
	rospy.spin()

#Add publisher ROS things
if __name__=='__main__':
	rospy.init_node('wifi_publisher')
	try:
		make()
	except rospy.ROSInterruptException: pass
