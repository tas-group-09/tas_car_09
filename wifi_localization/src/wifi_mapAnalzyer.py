#!/usr/bin/env python

import roslib;
import rospy, pickle
import os


dbLoc = "wifiMap.pk"


# load the database
def make():
	global database
	global dbLoc
	
	dbLoc = 'wifiMap.pk'

	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
		print "No map file found"
		database = {}

	
	positions = database.keys()
	counter = 1

	print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
	print  '/////////                                       Wifi Map Analyzer                                            /////////'
	print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
	

	for position in positions:
		
		print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
		print  '/////////                                       Postion', counter,                                             '///////// '
		print  '//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
		print
		print 'Location = ', position
		print
		
		MAC_Adresses = database[position].keys()

		for MAC in MAC_Adresses:
			print 'MAC Adress: ',MAC,'          Signal Strength: ',database[position][MAC]

		print
		print
		print

		counter = counter + 1


	rospy.spin()


# tbd
if __name__=='__main__':
	rospy.init_node('wifiMap_Analyzer')
	try:
		make()
	except rospy.ROSInterruptException: pass
