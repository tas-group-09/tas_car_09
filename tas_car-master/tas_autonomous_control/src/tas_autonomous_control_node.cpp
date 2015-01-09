#include "control/control.h"
#include <ros/ros.h>
#include <tf/transform_datatypes.h>
#include <sensor_msgs/LaserScan.h>
#include <math.h>


/*void laserCallback(const sensor_msgs::LaserScan & msg)
{

const unsigned int N = msg.ranges.size();
const double angel_res = msg.angle_increment;
//const unsigned int front_spann = (int)((FRONT_RES * GRAD_TO_RAD)/angel_res);
double frontDistance;

int i = 0;
frontDistance = 0.0;
// frontDistance is the average distance of 60 degree angle
for (i=0; i < front_spann*2; i++)
{
frontDistance += msg.ranges[i + N/2 - front_spann];
}
frontDistance = frontDistance/(front_spann*2);
}
*/
int main(int argc, char** argv)
{
    ros::init(argc, argv, "autonomous_control");
    control autonomous_control;

    ros::Rate loop_rate(50);

    bool isAutomaticControlOn=false;

    while(ros::ok())
    {
        if(autonomous_control.control_Mode.data==0)
        {
            if(isAutomaticControlOn==true){
               //ROS_INFO("Manually Control!");
               ROS_INFO("Switch to Manual Control!");
               isAutomaticControlOn=false;
            }

        }
        else
        {
            if(autonomous_control.control_Brake.data==1)
            {
                autonomous_control.control_servo.x=1500;
                autonomous_control.control_servo.y=1500;
            }
            else
            {
                if(isAutomaticControlOn==false){
                   //ROS_INFO("Automatic Control!");
                   ROS_INFO("Switch to Automatic Control!");
                   isAutomaticControlOn=true;
                }

                if(autonomous_control.cmd_linearVelocity>0)
                {
                    autonomous_control.control_servo.x = 1550;
                }
                else if(autonomous_control.cmd_linearVelocity<0)
                {
                    autonomous_control.control_servo.x = 1300;
                }
                else
                {
                    autonomous_control.control_servo.x = 1500;
                }

                autonomous_control.control_servo.y = autonomous_control.cmd_steeringAngle;
            }

            autonomous_control.control_servo_pub_.publish(autonomous_control.control_servo);

        }

        ros::spinOnce();
        loop_rate.sleep();

    }

    return 0;

}
