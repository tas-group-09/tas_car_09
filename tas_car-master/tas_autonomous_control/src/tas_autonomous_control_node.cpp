#include "control/control.h"


/* variable newSpeed is used to adjust the speed when the car is going straight. It is received by 'getNewSpeed()' */
int newSpeed;


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
            /* Notifies only when control mode is changed */
            if(isAutomaticControlOn==true)
            {
                ROS_INFO("Switch to Manual Control!"); //before: ROS_INFO("Manually Control!");
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
                if(isAutomaticControlOn==false)
                {
                    ROS_INFO("Switch to Automatic Control!"); //before: ROS_INFO("Automatic Control!");
                    isAutomaticControlOn=true;
                }
                
                /* variable newSpeed is set here! (in case: automatic, V>0) */
                if(autonomous_control.cmd_linearVelocity>0)
                {
                    newSpeed=autonomous_control.getNewSpeed();
                    
                    //std::cout << "Main \t servo x = " << newSpeed << std::endl;
                    
                    autonomous_control.control_servo.x = newSpeed; // before: 1550
                }
                else if(autonomous_control.cmd_linearVelocity<0)
                {
                    autonomous_control.control_servo.x = 1450;
                }
                else
                {
                    autonomous_control.control_servo.x = 1550;
                }
                
                autonomous_control.control_servo.y = autonomous_control.cmd_steeringAngle;
            }
            
            std::cout << "Servo = [" << autonomous_control.control_servo.x << "," << autonomous_control.control_servo.y << "]" << std::endl;
            
            autonomous_control.control_servo_pub_.publish(autonomous_control.control_servo);
            
        }
        
        ros::spinOnce();
        loop_rate.sleep();
        
    }
    
    return 0;
    
}
