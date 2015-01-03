#!/usr/bin/env python

import roslib; roslib.load_manifest('wifi_lookup')
import rospy, pickle, sys
from wifi_lookup.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance

# Daten sind in der Form: 
# database={injectLoc1: {'MAC_ADDR1': spot.dB, 'MAC_ADDR2': spot.dB}, 
#	    injectLoc2: {'MAC_ADDR1': spot.dB, 'MAC_ADDR2': spot.dB}}
#
# bzw.:                   
# database={(3, 0): {'MAC2': 48, 'MAC1': 60}, (0, 0): {'MAC2': 48, 'MAC1': 60}}


dbLoc = "database.pk"

injectLoc = (0,0)
oldLoc = (9,9)
counter = 0
tempDatabase = {}


def injectLocation(msg):
	
	oldLoc = injectLoc
	injectLoc = (msg.pose.x,msg.pose.y)
	print injectLoc
	


def injectWifi(data):

	if counter >= 1000 and counter < 1020:

		counter = counter + 1
	
		if(pow(oldLoc[0]-injectLoc[0],2) + pow(oldLoc[1]-injectLoc[1],2) > 0.09):
			counter = 0
		
		for spot in data.HotSpots:
		
			print spot.MAC, spot.dB

			tempDatabase[spot.MAC] = spot.dB
			

	elif counter == 1020:

		database[injectLoc] = tempDatabase
		tempDatabase = {}
		counter = 0
		print
		print	'Location added to Database'
		print
	

	else:
		counter = counter + 1

	

def clean():
	dbFile = open(dbLoc,"w")
	pickle.dump(database, dbFile)
	dbFile.close()



def make():
	global database
	global tempDatabase	
	global oldLoc
	global injectLoc
	global counter


	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}

	rospy.Subscriber('wifi_data', WifiData, injectWifi)
	rospy.Subscriber('amcl_pose',PoseWithCovariance,injectLocation)
	rospy.spin()

if __name__=='__main__':
	rospy.init_node('wifi_database')
	try:
		make()
	except rospy.ROSInterruptException: pass
	clean()
