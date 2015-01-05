#!/usr/bin/env python

import roslib;
import rospy, pickle, sys
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovarianceStamped
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

recordWifi = False

tempDatabase = {}

def wiimote_callback(msg):

	global recordWifi

	if(msg.buttons[1] == 1):
		if(recordWifi == False):
			print 'Wifi Recording -> STARTED'
			
		recordWifi = True
	else:
		if(recordWifi == True):
			print 'Wifi Recording -> ENDED'
		
		recordWifi = False
	



def injectLocation(msg):
	
	global injectLoc 

	oldLoc = injectLoc
	injectLoc = (msg.pose.pose.position.x,msg.pose.pose.position.y)
	#print injectLoc
	


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
	
	global oldLoc
	global injectLoc

	global recordWifi

	tempDatabase = {}

	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}

	rospy.Subscriber('wifi_data', WifiData, injectWifi)
	rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,injectLocation)
	rospy.Subscriber('wiimote/state',State,wiimote_callback)
	rospy.spin()

if __name__=='__main__':
	rospy.init_node('wifi_database')
	try:
		make()
	except rospy.ROSInterruptException: pass
	clean()
