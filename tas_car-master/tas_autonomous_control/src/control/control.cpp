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
r
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

    double frontDistance = 0.0; // average distance in front of the car for a 30 degree angle
    double leftDistance = 1.0;  // average distance in the left of the car for a 30 degree angle
    double rightDistance = 1.0; // average distance in the right of the car for a 30 degree angle
    double minimumDistance = 10.0; // minimum distance to a detected object in the front

    // frontDistance
    int counter = 0;
    for (int i=N/2-5*(int)(1/angleResolution); i < N/2+5*(1/angleResolution); i++)
    {
        if (msg->ranges[i]>0)
        {
        //std::cout << "laserCallback: i " << i<< std::endl;
        frontDistance += msg->ranges[i];
        //std::cout << "laserCallback: msg->ranges[i] " << msg->ranges[i]<< std::endl;

        counter ++;

        if(msg->ranges[i] < minimumDistance)
            minimumDistance = msg->ranges[i];
        }
    }
    //std::cout << "laserCallback: Summe " << frontDistance<< std::endl;

    frontDistance = frontDistance/((double) counter);
    std::cout << "laserCallback: frontDistance " << frontDistance<< std::endl;


    /* Data Structure not finished yet (05.01.)
    // leftDistance
    int counter = 0;
    for (int i=N/2-round(15/angleResolution); i < N/2+round(15/angleResolution); i++)
    {
    leftDistance += msg.ranges[i];
        counter ++;
    }
    leftDistance = leftDistance/(double) counter;

    // rightDistance
    int counter = 0;
    for (int i=N/2-round(15/angleResolution); i < N/2+round(15/angleResolution); i++)
    {
    rightDistance += msg.ranges[i];
        counter ++;
    }
    rightDistance = rightDistance/(double) counter;
    */

    leftDistance=1.0; rightDistance=1.0;

    /* now speed is adjusted to distances */
    controlSpeed(frontDistance, leftDistance, rightDistance, minimumDistance);
}

/* control speed (ACC) if car is going straight */
void control::controlSpeed(double frontDistance, double leftDistance, double rightDistance, double minimumDistance)
{
    //std::cout << "Control Speed" << std::endl;

    //    // Speed values are estimated based on Servo tests and default settings
    //    if(minimumDistance < 0.2 || leftDistance < 0.2 || rightDistance < 0.2)
    //    {
    //        optimalSpeed = 1500;

    //    } //break if closest object is <0.5m or too close to wall
    //    else
    //    {
    // TO DO: State machine

    // STRAIGHT
    optimalSpeed= (frontDistance/10.0)*50 + 1550; //linear control function based on frontDistance

    if(optimalSpeed>1600) optimalSpeed=1600; // for safety

    //    }

    //std::cout << "Control Speed \t Optimal Speed = " << optimalSpeed << std::endl;


}

int control::getNewSpeed()
{

    //std::cout << "Get New Speed" << std::endl;

    return optimalSpeed;

}
