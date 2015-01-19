#include "control.h"

ros::Publisher newSpeed_pub;

control::control()
{
    control_servo_pub_ = nh_.advertise<geometry_msgs::Vector3>("servo", 1);

    cmd_sub_ = nh_.subscribe<geometry_msgs::Twist>("cmd_vel", 1000, &control::cmdCallback,this);

    odom_sub_ = nh_.subscribe<geometry_msgs::Twist>("odom_vel",1000,&control::odomCallback,this);

    wii_communication_sub = nh_.subscribe<std_msgs::Int16MultiArray>("wii_communication",1000,&control::wiiCommunicationCallback,this);

    laser_sub = nh_.subscribe<sensor_msgs::LaserScan>("scan",1000,&control::laserCallback,this);

    /* Initialization of optimalSpeed*/
    int optimalSpeed = 1600;

    //    Fp = 10;// need to test! defult:125

    //    current_ServoMsg.x = 1500;
    //    current_ServoMsg.y = 1500;

    //    previous_ServoMsg.x = 1500;
    //    previous_ServoMsg.y = 1500;

}
// We can subscribe to the odom here and get some feedback signals so later we can build our controllers
void control::odomCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    odom_linearVelocity = msg->linear.x;
    odom_angularVelocity = msg->angular.z;

    odom_steeringAngle = 180/PI*atan(odom_angularVelocity/odom_linearVelocity*CAR_LENGTH);

    odom_steeringAngle = 1500 + 500/30*odom_steeringAngle;

    if(odom_steeringAngle > 2000)
    {
        odom_steeringAngle = 2000;
    }
    else if(odom_steeringAngle < 1000)
    {
        odom_steeringAngle = 1000;
    }
}

//Subscribe to the local planner and map the steering angle (and the velocity-but we dont do that here-) to pulse width modulation values.
void control::cmdCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    cmd_linearVelocity = msg->linear.x;
    cmd_angularVelocity = msg->angular.z;

    cmd_steeringAngle = 180/PI*atan(cmd_angularVelocity/cmd_linearVelocity*CAR_LENGTH);

    cmd_steeringAngle = 1500 + 500/30*cmd_steeringAngle;

    if(cmd_steeringAngle > 2000)
    {
        cmd_steeringAngle = 2000;
    }
    else if(cmd_steeringAngle < 1000)
    {
        cmd_steeringAngle = 1000;
    }
}
// a flag method that tells us if we are controlling the car manually or automatically
void control::wiiCommunicationCallback(const std_msgs::Int16MultiArray::ConstPtr& msg)
{
    control_Mode.data = msg->data[0];
    control_Brake.data = msg->data[1];
}

/* calculate distances frontDistance, leftDistance, rightDistance for detecting corners */
void control::laserCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
    const unsigned int N = msg->ranges.size();
    const double angleResolution = msg->angle_increment *180/M_PI; //TO DO: test!

    //std::cout << "laserCallback: N " << N<< std::endl;
    //std::cout << "laserCallback: angleResolution " << angleResolution << std::endl;

    double frontDistance = 0.0; // average distance in front of the car for a 10 degree angle
	double minimumDistance = 10.0; // minimum distance in front of the car for a 10 degree angle
	
    // frontDistance
    int counter = 0;
    for (int i=N/2-5*(int)(1/angleResolution); i < N/2+5*(1/angleResolution); i++)
    {
        if (msg->ranges[i]>0)
        {
        //std::cout << "laserCallback: i " << i<< std::endl;
        
		// approximation by computing average
		frontDistance += msg->ranges[i];
        //std::cout << "laserCallback: msg->ranges[i] " << msg->ranges[i]<< std::endl;

        counter ++;

        if(msg->ranges[i] < minimumDistance)
            minimumDistance = msg->ranges[i];
        }
    }
    //std::cout << "laserCallback: Summe " << frontDistance<< std::endl;

    frontDistance = frontDistance/((double) counter);
    //std::cout << "laserCallback: frontDistance " << frontDistance<< std::endl;

    /* now speed is adjusted to distances */
    controlSpeed(frontDistance);
}

/* control speed (ACC) if car is going straight */
void control::controlSpeed(double frontDistance)
{
    //std::cout << "controlSpeed" << std::endl;
	
	// STRAIGHT
    optimalSpeed= (frontDistance/10.0)*30 + 1550; //linear control function based on frontDistance

    if(optimalSpeed>1600) optimalSpeed=1600; // for safety
}

int control::getNewSpeed()
{

    //std::cout << "Get New Speed" << std::endl;

    return optimalSpeed;

}
