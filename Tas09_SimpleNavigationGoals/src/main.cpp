/**
 * This node sends fixed goals to move base via ROS Action API and receives feedback via callback functions.
 */

#include <iostream>
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <move_base_msgs/MoveBaseActionResult.h>
#include <nav_msgs/Path.h>
#include <actionlib/client/simple_action_client.h>

using namespace std;

//ToDo: External access (e.g. Wii-Remote)
//Switching variable for slalom true / false
bool slalom = false;
std::vector<geometry_msgs::Pose> waypoints; // vector of goals, with position and orientation



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


void PathCallback(const nav_msgs::Path& msg)
{
    std::cout << "PATH CALLBACK HAPPENED!" << std::endl;

    for(int i = 0; i < msg.poses.size() ; i++)
    {
        waypoints.push_back(msg.poses[i].pose);
    }

    return;
}



/**
 * Main function
 */
int main(int argc, char** argv){
    ros::init(argc, argv, "simple_navigation_goals"); // init and set name

    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("goals",10,PathCallback);


    MoveBaseClient ac("move_base", true); // action client to spin a thread by default




    ros::Rate loop_rate(50);


    while(ros::ok())
    {
        if(waypoints.size() != 0)
        {
            std::cout << "I am in" << std::endl;

            //std::cout << std::endl << std::endl << std::endl << "New Array" << std::endl;

            for(int i = 0; i < waypoints.size(); ++i)
            {
                //std::cout << "Waypoint"<< i << "[" <<waypoints[i].position.x << ", " << waypoints[i].position.y << "]" << std::endl;

            }
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
        }



        ros::spinOnce();
        //loop_rate.sleep();

    }


    return 0;
}
