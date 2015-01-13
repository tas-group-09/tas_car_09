#ifndef PATHPLANNER_H
#define PATHPLANNER_H

#include <iostream>
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <move_base_msgs/MoveBaseActionResult.h>

enum DIRECTION {CLOCKWISE, COUNTER_CLOCKWISE};


std::vector<geometry_msgs::Pose> Pathplanner(DIRECTION direction, geometry_msgs::Pose startPose)
{
    std::vector<geometry_msgs::Pose> unordered_Waypoints;
    std::vector<geometry_msgs::Pose> ordered_Waypoints;

//    geometry_msgs::Pose initialWaypoint;
//    initialWaypoint.position.x = 10.0;
//    initialWaypoint.position.y = 18.0;
//    initialWaypoint.position.z = 0.000;
//    initialWaypoint.orientation.x = 0.000;
//    initialWaypoint.orientation.y = 0.000;
//    initialWaypoint.orientation.z = -1.570796327;
//    initialWaypoint.orientation.w = 0.81011023189;


    // Corner 1/1
    geometry_msgs::Pose waypoint;
    waypoint.position.x = 10.4;
    waypoint.position.y = 8.0;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.586277589703;
    waypoint.orientation.w = 0.81011023189;
    unordered_waypoints.push_back(waypoint);

    // Corner 1/2
    waypoint.position.x = 10.4;
    waypoint.position.y = 6.74;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.37746662823;
    waypoint.orientation.w = 0.926023187924;
    unordered_waypoints.push_back(waypoint);

    // Corner 1/3
    waypoint.position.x = 12.7;
    waypoint.position.y = 6.3;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.0969236885705;
    waypoint.orientation.w = 0.995291815798;
    unordered_waypoints.push_back(waypoint);


    // Corner 2/1
    waypoint.position.x = 21.4;
    waypoint.position.y = 5.9;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.0997332827304;
    waypoint.orientation.w = 0.995014207092;
    unordered_waypoints.push_back(waypoint);

    // Corner 2/2
    waypoint.position.x = 23.48;
    waypoint.position.y = 6.56;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.687557328387;
    waypoint.orientation.w = 0.726130098661;
    unordered_waypoints.push_back(waypoint);


    // Corner 2/3
    waypoint.position.x = 23.37;
    waypoint.position.y = 7.55;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.679364543684;
    waypoint.orientation.w = 0.73380093812;
    unordered_waypoints.push_back(waypoint);




    // Corner 3/1
    waypoint.position.x = 23.8;
    waypoint.position.y = 18;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.803224655087;
    waypoint.orientation.w = 0.595676215288;
    unordered_waypoints.push_back(waypoint);

    // Corner 3/2
    waypoint.position.x = 23.46;
    waypoint.position.y = 18.87;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.968665283717;
    waypoint.orientation.w = 0.248369821278;
    unordered_waypoints.push_back(waypoint);

    // Corner 3/3
    waypoint.position.x = 22.2;
    waypoint.position.y = 19.1;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = 0.999914720206;
    waypoint.orientation.w = 0.00726689410215;
    unordered_waypoints.push_back(waypoint);



    // Corner 4/1
    waypoint.position.x = 12.8;
    waypoint.position.y = 19.6;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.997499162385;
    waypoint.orientation.w = 0.0706782925783;
    unordered_waypoints.push_back(waypoint);

    // Corner 4/2
    waypoint.position.x = 11.36;
    waypoint.position.y = 19.63;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.87778145924;
    waypoint.orientation.w = 0.47906127981;
    unordered_waypoints.push_back(waypoint);

    // Corner 4/3
    waypoint.position.x = 11.1;
    waypoint.position.y = 17.8;
    waypoint.position.z = 0.000;
    waypoint.orientation.x = 0.000;
    waypoint.orientation.y = 0.000;
    waypoint.orientation.z = -0.715423519161;
    waypoint.orientation.w = 0.698691053493;
    unordered_waypoints.push_back(waypoint);

    double minimalDistance = 99;

    for(int i = 0; i < unordered_Waypoints.size; i++)
    {

        ros::NodeHandle n;
        ros::ServiceClient client = n.serviceClient<move_base::make_plan>("make_plan");
        move_base::make_plan srv;
        srv.request.start = atoll(initialWaypoint);
        srv.request. = atoll(unordered_Waypoints[i]);

        if (client.call(srv))
        {
          srv.response.path


          ROS_INFO("Sum: %ld", (long int)srv.response.sum);
        }
        else
        {
          ROS_ERROR("Failed to call service add_two_ints");
          return 1;
        }


    }



    return ordered_Waypoints;

}


#endif // PATHPLANNER_H
