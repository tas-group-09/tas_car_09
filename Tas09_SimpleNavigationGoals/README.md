Tas09 Simple Navigation Goals 
==================

Overview
--------
This ROS package listens to the topic goals and executes the received waypoints using the Move Base node. 

Dependencies
--------
This package depends on the nav_msgs and the Move base node to execute the waypoints. 


Tas09 Simple Naviation Goals
--------

Instructions: 
This node subscribes to ROS topic "goals" and buffers the received waypoints in an array. The waypoints in the array are subsequently executed by Move Base node using the Action API. The target path has to be published only once otherwise this path is executed repeatedly.  


References
--------

This package was originally designed by LSR (https://github.com/LSR-TAS/tas_car) and was redesigned by TAS Group 09 for the TAS Car Project at the Technical University Munich in 2015 to buffer and execute any goals published to the topic goals..





