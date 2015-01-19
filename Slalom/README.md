Slalom
==================
This ROS package contains different nodes to fulfill the slalom task of the TAS project. The intial position for the car is set automatically. Afterwards, first a static goal for the scanning position is published to the TAS09 simple goal navigation planner. When the car approaches the scanning position the pylons are detected and corresponding waypoints will be generated automatically. 


Overview
--------

This package includes two nodes:

- Slalom_InitialLocation:	The Initial Position Node publsihes the inital position for the slalom task at the start of the execution.
- Slalom:			The Slalom Node detects the pylons, calculates the waypoints and publishes them to the navigation planner.

Dependencies
--------
The Slalom Node requires the scan data from the laserscanner, the pose estimate from amcl and publishes waypoints / path data to the simple goal navigation planner.



Usage instructions
------------------

###Slalom_InitialLocation
This node publishes the intial location for the slalom task.

###Slalom
This node handles the waypoints for the slalom parcours

At first the following function is executed:
```
  sendScanPosition()
```
This function publishes the predefined waypoint of the desired scan position to the navigation planner. The scan position is excentered to the line of pylons in ordert to enable a detection of individual objects with the laserscanner.

Afterwards, the function
```
  calculateWaypoints()
```
is executed and waits for the pose to pass a certain threshold, which is near the predifined scan position.

When these conditions are fulfilled, the subscribed scan data is evaluated. To detect the pylons within the scan data, each range of the lidar data is compared to the previous one. If there is a jump in distance with at least the predefined size the corresponding scan ray is declared as pylon candidate. This candidate has to pass further validations to hold the properties of a pylon. Therefore, the width of the object and a jump in distance after the object back to the wall is evaluated.

The width of the object is evaluated as follows:
```
  max_width_object_frames = (math.atan(max_width_object/(2*ranges[temp_i])*2)//increment)
```
Where "max_width_object_frames" is the maximum amount of frames allowed to be declared as pylon. The "max_width_object" variable holds the width of a pylon in meters. The parameters "ranges" and "increment" hold the data from the laserscanner (distance and angle increment respectively).

If the number of detected objects is then between two and the maximum of definfed points, the laserscan data of these objects can be converted into map coordinates. In order to further evaluate the detected points, the distance between each of the points is calculated. The calculated mean distance should be in the range of the predifined limits.

The next step determines the closest object in order to reference any further waypoints onto this point. Now, a target vector which points from one pylon to the next can be calculated (subtraction of the two points).

Due to reflection issues at the first pylon and therefore faulty scan data a further evaluation was implemented. If the distance of the closest point is higher than a certain threshold, then reflection issues at the first pylon caused the evaluation routines to ignore the "real" first pylon. Therefore, this error is canceled with a virtual estimation of the first pylon.

Finally, all waypoints can be calculated with the use of simple vector summation / subtraction and vector scaling. First between each pylon a waypoint is calculated by adding the half target vector onto each pylon point. Afterwards a waypoint is calculated next to each pylon with the use of an orthogonal vector (relative to the target vector).

These waypoints are then published as "path" to the simple goal navigation planner.


Additional Information
----------------------

This package was created by TAS Group 09 for the TAS Car Project at the Technical University Munich in 2015.

