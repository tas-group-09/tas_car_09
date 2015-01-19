Tas Car Master
==================

Overview
--------
This package contains the basic setup of the LSR cars. 


Additions by TAS Group 09:
--------

The basic setup was extended by a 

Dynamic Speed Control. This extension determines the optimal speed of the car by approximating the front distance that is obtained by a 10 degree angle in front of the car via laser scans. The speed control function is included in control.cpp, the optimal speed is used in tas_autonomous_control_node. 

------ Various Launch Files:

Various launch files for the primary task "Complete a Round around the LSR Floor" and the secondary task "Slalom" are added. Furthermore some parameter files for the global and local planner are changed.


References
--------
This package was designed by LSR (https://github.com/LSR-TAS/tas_car). The additions were created by TAS Group 09 for the TAS Car Project at the Technical University Munich in 2015.

