#!/usr/bin/env python

import roslib;
import rospy, pickle


dbLoc = "wifiMap.pk"


# load the database
def make():
	global database


	try:
		dbFile = open(dbLoc)
		database = pickle.load(dbFile)
		dbFile.close()
	except: 
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
