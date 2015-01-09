#!/usr/bin/env python

import roslib;
import rospy, pickle
from wifi_localization.msg import WifiData, Wifi
from geometry_msgs.msg import PoseWithCovariance

dbLoc = "/home/michael/catkin/src/Wifi_Localization/wifiMap.pk"


# load the database
def make():
	global database
	

	print
	print
	print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
	print  '/////////                                       Wifi Map Analyzer 				             ///////// '
	print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
	print
	print


	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		database = {}
		print 'Database is empty!'
		

	
	positions = database.keys()
	position_counter = 1


	
	for position in positions:
		
		print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
		print  '/////////                                       Postion', position_counter,'                                               ///////// '
		print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
		print
		print 'Location = ', position
		print
		
		MAC_Adresses = database[position].keys()
		MAC_counter = 1

		for MAC in MAC_Adresses:

			print MAC_counter,') MAC Adress: ',MAC,'          Signal Strength: ',database[position][MAC]
			MAC_counter = MAC_counter + 1

		print
		print
		print

		position_counter = position_counter + 1



	rospy.spin()


# tbd
if __name__=='__main__':
	rospy.init_node('wifiMap_Analyzer')
	try:
		make()
	except rospy.ROSInterruptException: pass
