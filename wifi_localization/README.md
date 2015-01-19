WiFi Localization
==================
This ROS package contains different nodes to enable an initial localization using the WiFi signal strengths of all surrounding WiFi Access Points. The WiFi localization uses a fingerprinting approach, where the WiFi Access Point fingerprint at the current location is compared to a database containing WiFi fingerprints of various locations.   


Overview
--------

This package includes four different nodes:

WiFi Publisher:     The WiFi Publisher node reads the measured signal strength and publishes a message which contains an list which contains the MAC adress and the signal strength of each measured WiFi access point.
WiFi Classifier:    The WiFi Classifier node classifies the measured WiFi data using a k Nearest Neighbour approach and publishes the estimated location.
WiFi Database:      The WiFi Database node is used to build up a database of the fingerprints of the WiFi Signals at different locations.
Initial Location:   The Initial Position Node publishes the intital Position for at the start of the Wifi Database generation.

Dependencies
--------
The WiFi Localization packages requires the UNIX command "iwlist" to read the signal strength of all available WiFi Acess Points. This command can be installed via "sudo apt-get" install wireless-tools. The Wii Mote package is required because many operations of this package are triggered using a Wii Mote. Furthermore this package requires the standard ROS messages geometry_msgs.


Location Estimation
--------

Instructions: 
For an initial Location Estimation the Wifi Publisher node and the WiFi classifier node need to be started. Furthermore an accurate database of the WiFi fingerprints is required by the WiFi classifier to allow an location estimation. The standard path for the database is "/catkin_ws/src/wifi_localization". The initial location is published if the (1) button on the Wii Mote is pressed.  

Functionality:
The WiFi classifier node reads the published message of the WiFi publisher node and saves them the measured WiFi signal strength. This measured Wifi Signal is compared to each point within the database using the Manhattan distance and the k Nearest Neighbours (kNN) are selected to allow classification of the unkownd location. The estimated Location is computed as the expectation value of the k Nearest Neighbours. This procedure was implemented because previous research by Li et al. [1] have shown that the kNN classifier with the Manhattan distance produced the most accurate location estimation.


Database Generation
--------

Instructions:
For the generation of a WiFi fingerprint database the Wifi Publisher node, the Wifi database node and the intitial location node need to be started. The car has to be set to the fixed starting position and the initial pose setting needs to be triggered via the (1) button on the Wii Mote. Afterwards the car can manually or autonomously drive to any location and record a WiFi fingerprint. The WiFi fingerprint is recorded by stopping the car and pressing the (2) button on the Wii Mote. The button should be pressed for at least 20 seconds.   


Functionality:
The WiFi Database node subscribes the messages published by the WiFi publisher node, the AMCL node and the Wii Mote node. When the WiFi recording is started via the Wii Mote the current WiFi signals with the corresponding position of the AMCL node are saved to the database. The AMCL pose is accurate due to the fixed starting position and the initialization via the location node. This database generation was designes to allow an autonomous database generation while driving. However the measurement frequency of the UNIX wireless tools to allow the database generation while driving. Therefore, the car needs to be stopped and the WiFi signals have to be measure for at least 20 seconds.    


References
--------

The WiFi publisher node as well as the structure of the database is designed by Robert Lynch and Josh Eversmann at the University of Texas in Spring 2013 (https://github.com/utexas-air-fri/wifi_localization). The architecture to allow an automated WiFi database generation using the LSR cars as well as the structure of the WiFi database was redesigned by TAS Group 09. The classifier node as well as the initial Location node were solely written by TAS Group 09.

[1] Binghao Li, James Salter, Andrew G. Dempster, Chris Rizos; "Indoor positioning techniques based on wireless LAN" in First IEEE International Conference on Wireless Broadband and Ultra Wideband Communications, pp. 13 - 16, 2006




