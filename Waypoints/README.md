Pathfinder
==================

Overview
--------
This ROS package contains the pathfinder node. The pathfinder node adapts the path around the 3rd Floor of the LSR to a given starting position.


Dependencies
--------
This package depends on the navigations messages and uses the MoveBase node of the navigation stack because it uses the MakePlan ROS service provided by the MoveBase node. To execute these waypoints the redesigned simple navigation goals node provided by TAS Group 09 is needed.


Pathfinder
--------

Instructions: 
The Pathfinder node takes any initial pose as starting point and computes the path to complete a whole lap around the 3rd floor of the LSR.


Functionality:
The Pathfinder has a total of 8 waypoints with 2 waypoints at each corner and adapts the ordering of the waypoints according to a initial pose. Therefore, this node computes the distance between the initial location and all other waypoints. 

This node computes the distance between the initial pose and the provided Waypoints to determine the next waypoint. To compute the distance the pathfinder node utilizes the makePlan service by MoveBase, which returns a path between two positions on the provided map. With this path the pathfinder node computes the driving distance. The next waypoint is selected by the shortest distance and the current orientation of the initial pose. This process is repeated for each following waypoint until the whole path around the 3rd floor is computed. The complete path is published to the topics goals. 


References
--------
This package was designed by TAS Group 09



