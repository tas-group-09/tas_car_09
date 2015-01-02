/**
 * This node sends fixed goals to move base via ROS Action API and receives feedback via callback functions.
 */

#include <iostream>
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <move_base_msgs/MoveBaseActionResult.h>
#include <actionlib/client/simple_action_client.h>

using namespace std;

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

/**
 * Callback function
 */
void doneCb(const actionlib::SimpleClientGoalState& state, const move_base_msgs::MoveBaseResultConstPtr& result) {
    ROS_INFO("Finished in state [%s]", state.toString().c_str());
}

/**
 * Callback function, called once when the goal becomes active
 */
void activeCb() {
    ROS_INFO("Goal just went active");
}

/**
 * Callback function, called every time feedback is received for the goal
 */
void feedbackCb(const move_base_msgs::MoveBaseFeedbackConstPtr& feedback) {
    //ROS_INFO("[X]:%f [Y]:%f [W]: %f [Z]: %f", feedback->base_position.pose.position.x,feedback->base_position.pose.position.y,feedback->base_position.pose.orientation.w, feedback->base_position.pose.orientation.z);
    return;
}

/**
 * Main function
 */
int main(int argc, char** argv){
    ros::init(argc, argv, "simple_navigation_goals"); // init and set name
    std::vector<geometry_msgs::Pose> waypoints; // vector of goals, with position and orientation

    // Corner 1/1
    geometry_msgs::Pose waypoint1;
    waypoint1.position.x = 10.4;
    waypoint1.position.y = 8.0;
    waypoint1.position.z = 0.000;
    waypoint1.orientation.x = 0.000;
    waypoint1.orientation.y = 0.000;
    waypoint1.orientation.z = -0.586277589703;
    waypoint1.orientation.w = 0.81011023189;
    waypoints.push_back(waypoint1);

    // Corner 1/2
    geometry_msgs::Pose waypoint2;
    waypoint1.position.x = 10.4;
    waypoint1.position.y = 6.74;
    waypoint1.position.z = 0.000;
    waypoint1.orientation.x = 0.000;
    waypoint1.orientation.y = 0.000;
    waypoint1.orientation.z = -0.37746662823;
    waypoint1.orientation.w = 0.926023187924;
    waypoints.push_back(waypoint2);

    // Corner 1/3
    geometry_msgs::Pose waypoint3;
    waypoint2.position.x = 12.7;
    waypoint2.position.y = 6.3;
    waypoint2.position.z = 0.000;
    waypoint2.orientation.x = 0.000;
    waypoint2.orientation.y = 0.000;
    waypoint2.orientation.z = -0.0969236885705;
    waypoint2.orientation.w = 0.995291815798;
    waypoints.push_back(waypoint3);

    // Corner 2/1
    geometry_msgs::Pose waypoint4;
    waypoint3.position.x = 21.4;
    waypoint3.position.y = 5.9;
    waypoint3.position.z = 0.000;
    waypoint3.orientation.x = 0.000;
    waypoint3.orientation.y = 0.000;
    waypoint3.orientation.z = 0.0997332827304;
    waypoint3.orientation.w = 0.995014207092;
    waypoints.push_back(waypoint4);

    // Corner 2/2
    geometry_msgs::Pose waypoint5;
    waypoint4.position.x = 23.48;
    waypoint4.position.y = 6.56;
    waypoint4.position.z = 0.000;
    waypoint4.orientation.x = 0.000;
    waypoint4.orientation.y = 0.000;
    waypoint4.orientation.z = 0.687557328387;
    waypoint4.orientation.w = 0.726130098661;
    waypoints.push_back(waypoint5);


    // Corner 2/3
    geometry_msgs::Pose waypoint6;
    waypoint5.position.x = 23.37;
    waypoint5.position.y = 7.55;
    waypoint5.position.z = 0.000;
    waypoint5.orientation.x = 0.000;
    waypoint5.orientation.y = 0.000;
    waypoint5.orientation.z = 0.679364543684;
    waypoint5.orientation.w = 0.73380093812;
    waypoints.push_back(waypoint6);

    // Corner 3/1
    geometry_msgs::Pose waypoint7;
    waypoint6.position.x = 23.8;
    waypoint6.position.y = 18;
    waypoint6.position.z = 0.000;
    waypoint6.orientation.x = 0.000;
    waypoint6.orientation.y = 0.000;
    waypoint6.orientation.z = 0.803224655087;
    waypoint6.orientation.w = 0.595676215288;
    waypoints.push_back(waypoint7);

    // Corner 3/2
    geometry_msgs::Pose waypoint8;
    waypoint7.position.x = 23.46;
    waypoint7.position.y = 18.87;
    waypoint7.position.z = 0.000;
    waypoint7.orientation.x = 0.000;
    waypoint7.orientation.y = 0.000;
    waypoint7.orientation.z = 0.968665283717;
    waypoint7.orientation.w = 0.248369821278;
    waypoints.push_back(waypoint8);

    // Corner 3/3
    geometry_msgs::Pose waypoint9;
    waypoint7.position.x = 22.2;
    waypoint7.position.y = 19.1;
    waypoint7.position.z = 0.000;
    waypoint7.orientation.x = 0.000;
    waypoint7.orientation.y = 0.000;
    waypoint7.orientation.z = 0.999914720206;
    waypoint7.orientation.w = 0.00726689410215;
    waypoints.push_back(waypoint9);



    // Corner 4/1
    geometry_msgs::Pose waypoint10;
    waypoint8.position.x = 12.8;
    waypoint8.position.y = 19.6;
    waypoint8.position.z = 0.000;
    waypoint8.orientation.x = 0.000;
    waypoint8.orientation.y = 0.000;
    waypoint8.orientation.z = -0.997499162385;
    waypoint8.orientation.w = 0.0706782925783;
    waypoints.push_back(waypoint10);

    // Corner 4/2
    geometry_msgs::Pose waypoint11;
    waypoint9.position.x = 11.36;
    waypoint9.position.y = 19.63;
    waypoint9.position.z = 0.000;
    waypoint9.orientation.x = 0.000;
    waypoint9.orientation.y = 0.000;
    waypoint9.orientation.z = -0.87778145924;
    waypoint9.orientation.w = 0.47906127981;
    waypoints.push_back(waypoint11);

    // Corner 4/3
    geometry_msgs::Pose waypoint12;
    waypoint9.position.x = 11.1;
    waypoint9.position.y = 17.8;
    waypoint9.position.z = 0.000;
    waypoint9.orientation.x = 0.000;
    waypoint9.orientation.y = 0.000;
    waypoint9.orientation.z = -0.715423519161;
    waypoint9.orientation.w = 0.698691053493;
    waypoints.push_back(waypoint12);


/*  Version 0.01
    // 1/3 Hall 1
    geometry_msgs::Pose waypoint1;
    waypoint1.position.x = 11.0;
    waypoint1.position.y = 15.0;
    waypoint1.position.z = 0.000;
    waypoint1.orientation.x = 0.000;
    waypoint1.orientation.y = 0.000;
    waypoint1.orientation.z = 0;
    waypoint1.orientation.w = 1;
    waypoints.push_back(waypoint1);

    // 2/3 Hall 1
    geometry_msgs::Pose waypoint2;
    waypoint2.position.x = 10.5;
    waypoint2.position.y = 10.0;
    waypoint2.position.z = 0.000;
    waypoint2.orientation.x = 0.000;
    waypoint2.orientation.y = 0.000;
    waypoint2.orientation.z = 0;
    waypoint2.orientation.w = 1;
    waypoints.push_back(waypoint2);

    // Corner 1
    geometry_msgs::Pose waypoint3;
    waypoint3.position.x = 10.8;
    waypoint3.position.y = 6.8;
    waypoint3.position.z = 0.000;
    waypoint3.orientation.x = 0.000;
    waypoint3.orientation.y = 0.000;
    waypoint3.orientation.z = 0;
    waypoint3.orientation.w = 1;
    waypoints.push_back(waypoint3);

    // 1/3 Hall 2
    geometry_msgs::Pose waypoint4;
    waypoint4.position.x = 15.3;
    waypoint4.position.y = 6.3;
    waypoint4.position.z = 0.000;
    waypoint4.orientation.x = 0.000;
    waypoint4.orientation.y = 0.000;
    waypoint4.orientation.z = 0;
    waypoint4.orientation.w = 1;
    waypoints.push_back(waypoint4);

    // 2/3 Hall 2
    geometry_msgs::Pose waypoint5;
    waypoint5.position.x = 19.8;
    waypoint5.position.y = 6.0;
    waypoint5.position.z = 0.000;
    waypoint5.orientation.x = 0.000;
    waypoint5.orientation.y = 0.000;
    waypoint5.orientation.z = 0;
    waypoint5.orientation.w = 1;
    waypoints.push_back(waypoint5);

    // Corner 2
    geometry_msgs::Pose waypoint6;
    waypoint6.position.x = 23.3;
    waypoint6.position.y = 6.3;
    waypoint6.position.z = 0.000;
    waypoint6.orientation.x = 0.000;
    waypoint6.orientation.y = 0.000;
    waypoint6.orientation.z = 0;
    waypoint6.orientation.w = 1;
    waypoints.push_back(waypoint6);


    // 1/3 Hall 3
    geometry_msgs::Pose waypoint7;
    waypoint7.position.x = 23.5;
    waypoint7.position.y = 10;
    waypoint7.position.z = 0.000;
    waypoint7.orientation.x = 0.000;
    waypoint7.orientation.y = 0.000;
    waypoint7.orientation.z = 0;
    waypoint7.orientation.w = 1;
    waypoints.push_back(waypoint7);

    // 2/3 Hall 3
    geometry_msgs::Pose waypoint8;
    waypoint8.position.x = 23.4;
    waypoint8.position.y = 14;
    waypoint8.position.z = 0.000;
    waypoint8.orientation.x = 0.000;
    waypoint8.orientation.y = 0.000;
    waypoint8.orientation.z = 0;
    waypoint8.orientation.w = 1;
    waypoints.push_back(waypoint8);

    // Corner 3
    geometry_msgs::Pose waypoint9;
    waypoint9.position.x = 23.3;
    waypoint9.position.y = 18.7;
    waypoint9.position.z = 0.000;
    waypoint9.orientation.x = 0.000;
    waypoint9.orientation.y = 0.000;
    waypoint9.orientation.z = 0;
    waypoint9.orientation.w = 1;
    waypoints.push_back(waypoint9);

    // 1/3 Hall 4
    geometry_msgs::Pose waypoint10;
    waypoint10.position.x = 19.4;
    waypoint10.position.y = 19.2;
    waypoint10.position.z = 0.000;
    waypoint10.orientation.x = 0.000;
    waypoint10.orientation.y = 0.000;
    waypoint10.orientation.z = 0;
    waypoint10.orientation.w = 1;
    waypoints.push_back(waypoint10);

    // 2/3 Hall 4
    geometry_msgs::Pose waypoint11;
    waypoint11.position.x = 15.3;
    waypoint11.position.y = 19.3;
    waypoint11.position.z = 0.000;
    waypoint11.orientation.x = 0.000;
    waypoint11.orientation.y = 0.000;
    waypoint11.orientation.z = 0;
    waypoint11.orientation.w = 1;
    waypoints.push_back(waypoint11);

    // Corner 4
    geometry_msgs::Pose waypoint12;
    waypoint12.position.x = 11.4;
    waypoint12.position.y = 19.3;
    waypoint12.position.z = 0.000;
    waypoint12.orientation.x = 0.000;
    waypoint12.orientation.y = 0.000;
    waypoint12.orientation.z = 0;
    waypoint12.orientation.w = 1;
    waypoints.push_back(waypoint12);
*/

    MoveBaseClient ac("move_base", true); // action client to spin a thread by default

    while (!ac.waitForServer(ros::Duration(5.0))) { // wait for the action server to come up
        ROS_INFO("Waiting for the move_base action server to come up");
    }

    move_base_msgs::MoveBaseGoal goal;
    goal.target_pose.header.frame_id = "map"; // set target pose frame of coordinates

    for(int i = 0; i < waypoints.size(); ++i) { // loop over all goal points, point by point
        goal.target_pose.header.stamp = ros::Time::now(); // set current time
        goal.target_pose.pose = waypoints.at(i);
        ROS_INFO("Sending goal");
        ac.sendGoal(goal, &doneCb, &activeCb, &feedbackCb); // send goal and register callback handler
        ac.waitForResult(); // wait for goal result

        if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) {
            ROS_INFO("The base moved to %d goal", i);
        } else {
            ROS_INFO("The base failed to move to %d goal for some reason", i);
        }
    }
    return 0;
}
