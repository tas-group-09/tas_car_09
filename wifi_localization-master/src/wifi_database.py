#!/usr/bin/env python

import roslib;
import rospy, pickle, sys
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance
from wiimote.msg import State

# Daten sind in der Form: 
# database={injectLoc1: {'MAC_ADDR1': spot.dB, 'MAC_ADDR2': spot.dB}, 
#	    injectLoc2: {'MAC_ADDR1': spot.dB, 'MAC_ADDR2': spot.dB}}
#
# bzw.:                   
# database={(3, 0): {'MAC2': 48, 'MAC1': 60}, (0, 0): {'MAC2': 48, 'MAC1': 60}}


dbLoc = "database.pk"

injectLoc = (0,0)
oldLoc = (9,9)

recordWifi = false

tempDatabase = {}

def wiimote_callback(msg):
	if(msg.buttons[1] == 1):
		if(recordWifi == false):
			print 'Wifi Recording -> STARTED'
			
		recordWifi = true
	else:
		if(recordWifi == true):
			print 'Wifi Recording -> ENDED'
		
		recordWifi = false
	



def injectLocation(msg):
	
	oldLoc = injectLoc
	injectLoc = (msg.pose.position.x,msg.pose.position.y)
	print injectLoc
	


def injectWifi(data):

	if recordWifi == true:
		
		for spot in data.HotSpots:
		
			print spot.MAC, spot.dB
			tempDatabase[spot.MAC] = spot.dB
			

	elif recordWifi == false and len(tempDatabase) > 0:

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
	
	global oldLoc
	global injectLoc

	global recordWifi


	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}

	rospy.Subscriber('wifi_data', WifiData, injectWifi)
	rospy.Subscriber('amcl_pose',PoseWithCovariance,injectLocation)
	rospy.Subscriber('wiimote/state',State,wiimote_callback)
	rospy.spin()

if __name__=='__main__':
	rospy.init_node('wifi_database')
	try:
		make()
	except rospy.ROSInterruptException: pass
	clean()
