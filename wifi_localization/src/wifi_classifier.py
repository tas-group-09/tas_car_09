#!/usr/bin/env python

import roslib;
import rospy, pickle
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance
from wiimote.msg import State


# The path needs to be changed to the according system.
dbLoc = "catkin/src/wifi_localization/wifiMap.pk"

publishWifi = False         # global variable which triggers the publishing of the initial pose.

k = 3                       # global variable which defines the used k Nearest Neighbours.

def WifiCallback(data):
    	global publishWifi
	global measurement_database
	global iteration_counter
	global k
    
    	if(publishWifi == True):
	
		# For classification the classifier uses the data from 10 measurements published by the Wifi Publisher
		if iteration_counter < 10:
		    iteration_counter = iteration_counter + 1	
		    for spot in data.HotSpots:
		        measurement_database[spot.MAC] = spot.dB

		    print iteration_counter,') The message contains',len(measurement_database.keys()),'hotspots'
		
		# Computation of the initial location
		else:
		    iteration_counter = 0
		    
		    print
		    print 'The COMPLETE measurement database contains',len(measurement_database.keys()),'hotspots.'
		    print		
		    
		    positions = database.keys()	
		    database_entries = len(positions)
		
		    minimalError = []
		    minimalError_Position = []

		    # Initialization of the minimal error for the k - nearest neighbour
		    for i in range(0,k):
		        minimalError.append(99999999)
		        minimalError_Position.append((0,0))

		    # Comparison of the measured database with every location within the database.
		    for position in positions:
		        position_database = database[position]

		        # Computation of all MAC adresses in the measurement database and the MAC adresses from the database at the corresponding location
		        all_MAC_map = position_database.keys()
		        all_MAC_measurements = measurement_database.keys()

		        all_MAC = all_MAC_map
		        
		        # Merge all Mac addresses
		        for measurement_MAC in all_MAC_measurements:
		            if measurement_MAC not in all_MAC:
		                all_MAC.append(measurement_MAC)
		        
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
		                print 'ERROR while comparing the fingerprints of the WiFI Signals'
		
		        #print '@ Position',position,'the error equals',error
		    
		        #Check wether the tested point is one of the k nearest Neighbours
		        for i in range(0,k):

		            if error < minimalError[i]:
		                minimalError_Position[i] = position
		                minimalError[i] = error
		                break
	     
		        # Reset of the measurement database.
		        measurement_database = {}
		    
		    x = 0
		    y = 0
		    
		    # Calculation of the expectation value of the current position from the k - Nearest Neighbours.
		    for i in range(0,k):
		        x = x + minimalError_Position[i][0]
		        y = y + minimalError_Position[i][1]

		    covariance = []
		    for i in range(0,36):
		        covariance.append(0)
		    

		    msg = PoseWithCovariance()
		
		    msg.pose.position.x = x/k
		    msg.pose.position.y = y/k
		    msg.pose.position.z = 0

		    msg.pose.orientation.x = 0
		    msg.pose.orientation.y = 0
		    msg.pose.orientation.z = 0

		    msg.covariance = covariance


		    print '[',x,',',y,']'
		    
		    # Publishing the estimated Location via WiFi Localization
		    pub.publish(msg)



# Function to trigger the location Estimation.
def wiimote_callback(msg):
    
   	global publishWifi
        
	if(msg.buttons[1] == 1):

            if(publishWifi == False):
                print 'Wifi Publishing -> STARTED'
                
                publishWifi = True
        else:
            if(publishWifi == True):
                print 'Wifi Publishing -> ENDED'
                
                publishWifi = False




# Reading of the previously generated database
def make():
	global database
	global pub
	global dbLoc
	global measurement_database
	global iteration_counter

	pub = rospy.Publisher('initialpose', PoseWithCovariance, queue_size=10)

	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
		print 'Database found'

	except: 
		print 'Map not found'
		database = {}
	
	measurement_database = {}
	iteration_counter = 0

	rospy.Subscriber('wifi_data', WifiData, WifiCallback)
    	rospy.Subscriber('wiimote/state',State,wiimote_callback)

	rospy.spin()


# tbd
if __name__=='__main__':
	rospy.init_node('wifi_classifier')
	try:
		make()
	except rospy.ROSInterruptException: pass
