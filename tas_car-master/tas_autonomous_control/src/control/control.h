#ifndef CONTROL_H
#define CONTROL_H

#include "ros/ros.h"
#include "std_msgs/Int16.h"
#include "std_msgs/Int16MultiArray.h"
#include <math.h>
#include <geometry_msgs/Vector3.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/LaserScan.h>
#include <tf/transform_datatypes.h>
#include <math.h>

#define PI                     3.14159265
#define CAR_LENGTH              0.355
#define SCALE_FAKTOR_STEERING   500

class control
{
public:
    control();

    ros::NodeHandle nh_;
    ros::Publisher control_servo_pub_;
    ros::Subscriber cmd_sub_;
    ros::Subscriber odom_sub_;
    ros::Subscriber wii_communication_sub;
    ros::Subscriber laser_sub; /* modified: laser needed for speed control */ 

    std_msgs::Int16 control_Brake; /* flag for brake */
    std_msgs::Int16 control_Mode; /* flag for car mode: manual or autonomous */

    double cmd_linearVelocity;
    double cmd_angularVelocity;
    double cmd_steeringAngle;

    double odom_linearVelocity;
    double odom_angularVelocity;
    double odom_steeringAngle;

    geometry_msgs::Vector3 control_servo;

    /* newSpeed is computed in control.cpp. This method is used in autonomous control to receive the new speed*/
    int getNewSpeed();
    int optimalSpeed;

private:
    /* subscribe the cmd message from move_base */
    void cmdCallback(const geometry_msgs::Twist::ConstPtr& msg);

    /* subscribe the virtual odom message as a feedback for controller */
    void odomCallback(const geometry_msgs::Twist::ConstPtr& msg);

    /* check the wii states and switch the flag for manual mode and autonomous mode */
    void wiiCommunicationCallback(const std_msgs::Int16MultiArray::ConstPtr& msg);

    /* calculate distances frontDistance, leftDistance, rightDistance for detecting corners */
    void laserCallback(const sensor_msgs::LaserScan::ConstPtr& msg);

    /* control speed (ACC) if car is going straight */
    void controlSpeed(double frontDistance);



};

#endif // CONTROL_H
