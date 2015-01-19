#!/usr/bin/env python

import roslib;
import rospy, pickle, sys
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovarianceStamped
from wiimote.msg import State

# General Database Architecture:

# The database is a dictionary, which uses the locations of the WiFi fingerprints as keys.
# The corresponding values for the keys is a secondary dictionary, which contains the MAC
# adresses and the signal strengt of the WiFi signal at the corresponding location. This
# secondary dictionary uses the MAC adresses as keys and the signal strength as value. An
# example of the database structure is shown below.
#
# database      = {Location1: {'MAC_ADDR1': spot.dB, 'MAC_ADDR2': spot.dB},
#                  Location2: {'MAC_ADDR4': spot.dB, 'MAC_ADDR1': spot.dB}}
#
# database      ={(3, 0)    : {'MAC2': 48,           'MAC1': 60},
#                 (0, 0)    : {'MAC9': 21,           'MAC5': 67}}

# The path needs to be changed to the according system.
dbLoc = "catkin/src/wifi_localization/wifiMap.pk"

injectLoc = (0,0)       # global tuple variable containing the current location (X,Y)

recordWifi = False      # global boolean variable triggering the measuring of the WiFi Fingerprint.

tempDatabase = {}       # Temporary database to buffer the measured signals.


# The Wiimote_callback triggers the the recording of the WiFi Signals
def wiimote_callback(msg):

	global recordWifi

	if(msg.buttons[1] == 1):
		if(recordWifi == False):
			print 'WiFi Recording -> STARTED'
			
		recordWifi = True
	else:
		if(recordWifi == True):
			print 'WiFi Recording -> ENDED'
		
		recordWifi = False
	



# The inject Location function reads the message with the current pose and buffers it.
def injectLocation(msg):
	
	global injectLoc 

	injectLoc = (msg.pose.pose.position.x,msg.pose.pose.position.y)


# The injectWifi function buffers the measured WiFi signals and appends them into the current database after the measuring trigger has stopped.
def injectWifi(data):

	global tempDatabase
	global recordWifi
	global database
	global injectLoc

	if recordWifi == True:
		
		for spot in data.HotSpots:
		
			print spot.MAC, spot.dB
			tempDatabase[spot.MAC] = spot.dB
			

	elif recordWifi == False and len(tempDatabase) > 0:

		database[injectLoc] = tempDatabase
		tempDatabase = {}

		print
		print	'Location added to Database'
		print
	

	else:
		tempDatabase = {}

	

def clean():
	dbFile = open(dbLoc,"w")
	pickle.dump(database, dbFile)
	dbFile.close()



def make():
	global database
	global tempDatabase
    	global injectLoc
	global recordWifi

	tempDatabase = {}

	try:
        
        # Loading of the current database
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
		print 'Map found'

    	except:
        	# No previous database is existent
		database = {}
		print 'No previously map found'

    	# Subscribing the Wifi Publisher node for the MAC adresses and the signal strength
	rospy.Subscriber('wifi_data', WifiData, injectWifi)
    
    	# Subsribing the amcl node for the current pose used for the database generation.
	rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,injectLocation)

    	# Subscribing the wii mote state to enable triggering of the WiFi recording.   
    	rospy.Subscriber('wiimote/state',State,wiimote_callback)
	rospy.spin()

if __name__=='__main__':
	rospy.init_node('wifi_database')
	try:
		make()
	except rospy.ROSInterruptException: pass
	clean()
