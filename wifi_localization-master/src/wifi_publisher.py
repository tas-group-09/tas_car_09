#!/usr/bin/env python

import roslib;
import rospy, os, re
from wifi_localization.msg import WifiData, Wifi


class DataNode():
	def __init__(self):
		pub = rospy.Publisher('wifi_data', WifiData, queue_size=2)

		r = rospy.Rate(rospy.get_param('~rate', 1))
		while not rospy.is_shutdown():
			os.system("iwlist wlan0 scan >> datatemp.txt")

			wifiraw = open("datatemp.txt").read()
			os.remove("datatemp.txt")

			essids = re.findall("ESSID:\"(.*)\"", wifiraw)
			addresses = re.findall("Address: ([0-9A-F:]{17})", wifiraw)
			signals = re.findall("Signal level=.*?([0-9]+)", wifiraw)

			msg = WifiData()

			for i in range(len(essids)):
				temp = Wifi()			    
				temp.MAC = addresses[i] 
				temp.dB = int(signals[i])
				msg.HotSpots.append(temp)

			msg.length = len(msg.HotSpots)
			pub.publish(msg)
			r.sleep()

if __name__ == '__main__':
	rospy.init_node('wifi_publisher')
	try:
		node = DataNode()
	except rospy.ROSInterruptException: pass
	
