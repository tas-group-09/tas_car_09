#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from nav_msgs.msg import Path

from nav_msgs.srv   import GetPlan 


global tolerance



def computePathLength(startPose, goalPose):

    global tolerance

    tolerance = 0.1

    startPose = Pose()
    startPose.position.x = 10.0
    startPose.position.y = 8.0
    startPose.position.z = 0.000
    startPose.orientation.x = 0.000
    startPose.orientation.y = 0.000
    startPose.orientation.z = -0.586277589703
    startPose.orientation.w = 0.81011023189

    goalPose = Pose()
    goalPose.position.x = 12.0
    goalPose.position.y = 9.0
    goalPose.position.z = 0.000
    goalPose.orientation.x = 0.000
    goalPose.orientation.y = 0.000
    goalPose.orientation.z = -0.586277589703
    goalPose.orientation.w = 0.81011023189


    print "////////////////////////////////////////////////////"
    print "START = ",startPose
    print "////////////////////////////////////////////////////"
    print
    print	
    print "////////////////////////////////////////////////////"
    print "ENDE = ",goalPose
    print "////////////////////////////////////////////////////"

    rospy.wait_for_service('move_base_node/make_plan')
    
    print "Plan available"

    try:
        make_plan_connection = rospy.ServiceProxy('move_base_node/NavfnROS/make_plan', GetPlan)
        #make_plan_connection = rospy.ServiceProxy('move_base_node/make_plan', GetPlan)
	start = PoseStamped()
	goal = PoseStamped()

	start.header.stamp  = rospy.get_rostime()
	goal.header.stamp  = rospy.get_rostime()

	start.header.frame_id  = '/map'
	goal.header.frame_id  = '/map'

	start.pose = startPose
	goal.pose = goalPose

        response = make_plan_connection(start,goal,tolerance)
    
    	print
    	print	
    	print "////////////////////////////////////////////////////"
    	print response
    	print "////////////////////////////////////////////////////"
	print len(response.plan.poses)

        distance = 0
        currentPosition = (start.pose.position.x, start.pose.position.y)
        nextPosition = (0,0)
    
        for pose_on_Path in response.plan.poses:
            
            nextPosition = (pose_on_Path.pose.position.x, pose_on_Path.pose.position.y)

            distance = distance + ((currentPosition[0] - nextPosition[0])**2 + (currentPosition[1] - nextPosition[1])**2)**(1/2)

            currentPosition = nextPosition

        return distance

    except rospy.ServiceException, e:
        print "Service call failed: %s" %e
	



def computeOrientation(start, goal):
    
    global tolerance
    
    rospy.wait_for_service('make_plan')
    
    try:
        make_plan_connection = rospy.ServiceProxy('make_plan', makePlan)
        path = make_plan_connection(start,goal,tolerance)
        
        deltaX = start.pose.pose.position.x - path[0].pose.pose.position.x
        deltaY = start.pose.pose.position.y - path[0].pose.pose.position.y

        yaw = atan2(deltaY,deltaX)
        
        return yaw
    
    except rospy.ServiceException, e:
        print "Service call failed: %s" %e



    
def computeOptimalPath(initialPose):

    rospy.init_node('PathPlanner', anonymous=True)    

    unorderedWaypoints = []
    orderedWaypoints = []
    

    
    # Corner 1/1
    waypoint1 = Pose()
    waypoint1.position.x = 10.4
    waypoint1.position.y = 8.0
    waypoint1.position.z = 0.000
    waypoint1.orientation.x = 0.000
    waypoint1.orientation.y = 0.000
    waypoint1.orientation.z = -0.586277589703
    waypoint1.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint1)

    # Corner 1/2
    waypoint2 = Pose()
    waypoint2.position.x = 10.4
    waypoint2.position.y = 6.74
    waypoint2.position.z = 0.000
    waypoint2.orientation.x = 0.000
    waypoint2.orientation.y = 0.000
    waypoint2.orientation.z = -0.37746662823
    waypoint2.orientation.w =0.81011023189
    
    unorderedWaypoints.append(waypoint2)

    
    # Corner 1/3
    waypoint3 = Pose()
    waypoint3.position.x = 12.7
    waypoint3.position.y = 6.3
    waypoint3.position.z = 0.00
    waypoint3.orientation.x = 0.000
    waypoint3.orientation.y = 0.000
    waypoint3.orientation.z = -0.0969236885705
    waypoint3.orientation.w = 0.81011023189
    
    unorderedWaypoints.append(waypoint3)
    
    # Corner 2/1
    waypoint4 = Pose()
    waypoint4.position.x = 21.4
    waypoint4.position.y = 5.9
    waypoint4.position.z = 0.000
    waypoint4.orientation.x = 0.000
    waypoint4.orientation.y = 0.000
    waypoint4.orientation.z = 0.0997332827304
    waypoint4.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint4)

    # Corner 2/2
    waypoint5 = Pose()
    waypoint5.position.x = 23.48
    waypoint5.position.y = 6.56
    waypoint5.position.z = 0.000
    waypoint5.orientation.x = 0.000
    waypoint5.orientation.y = 0.000
    waypoint5.orientation.z = 0.687557328387
    waypoint5.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint5)

    # Corner 2/3
    waypoint6 = Pose()
    waypoint6.position.x = 23.37
    waypoint6.position.y = 7.55
    waypoint6.position.z = 0.000
    waypoint6.orientation.x = 0.000
    waypoint6.orientation.y = 0.000
    waypoint6.orientation.z = 0.679364543684
    waypoint6.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint6)

    # Corner 3/1
    waypoint7 = Pose()
    waypoint7.position.x = 23.8
    waypoint7.position.y = 18
    waypoint7.position.z = 0.00
    waypoint7.orientation.x = 0.000
    waypoint7.orientation.y = 0.000
    waypoint7.orientation.z = 0.803224655087
    waypoint7.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint7)

    # Corner 3/2
    waypoint8 = Pose()
    waypoint8.position.x = 23.46
    waypoint8.position.y = 18.87
    waypoint8.position.z = 0.000
    waypoint8.orientation.x = 0.000
    waypoint8.orientation.y = 0.000
    waypoint8.orientation.z = 0.968665283717
    waypoint8.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint8)
    
    # Corner 3/3
    waypoint9 = Pose()
    waypoint9.position.x = 22.2
    waypoint9.position.y = 19.1
    waypoint9.position.z = 0.000
    waypoint9.orientation.x = 0.000
    waypoint9.orientation.y = 0.000
    waypoint9.orientation.z = 0.999914720206
    waypoint9.orientation.w = 0.81011023189
    
    unorderedWaypoints.append(waypoint9)
    
    # Corner 4/1
    waypoint10 = Pose()
    waypoint10.position.x = 12.8
    waypoint10.position.y = 19.6
    waypoint10.position.z = 0.000
    waypoint10.orientation.x = 0.000
    waypoint10.orientation.y = 0.000
    waypoint10.orientation.z = -0.997499162385
    waypoint10.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint10)
    
    # Corner 4/2
    waypoint11 = Pose()
    waypoint11.position.x = 11.36
    waypoint11.position.y = 19.63
    waypoint11.position.z = 0.000
    waypoint11.orientation.x = 0.00
    waypoint11.orientation.y = 0.000
    waypoint11.orientation.z = -0.87778145924
    waypoint11.orientation.w = 0.81011023189

    unorderedWaypoints.append(waypoint11)

    # Corner 4/3
    waypoint12 = Pose()
    waypoint12.position.x = 11.1
    waypoint12.position.y = 17.8
    waypoint12.position.z = 0.000;
    waypoint12.orientation.x = 0.000
    waypoint12.orientation.y = 0.000
    waypoint12.orientation.z = -0.715423519161
    waypoint12.orientation.w = 0.81011023189
    
    unorderedWaypoints.append(waypoint12)
    
    #while len(unorderedWaypoints) != 0:
    
    minimalDistance     = 9999
    closestPose         = Pose()
    closestPose_Index   = 9999

    
    currentPose = initialPose
    
    #    for pose in unorderedWaypoints:
    pose = unorderedWaypoints[5]
    distance = computePathLength(currentPose,pose)

    print "////////////////////////////////////////////////////"
    print distance
    print "////////////////////////////////////////////////////"


    #       if(distance < minimalDistance):
    #            minimalDistance = distance
    #            closestPose = pose


        #orderedWaypoints.append(closestPose)
        #unorderedWaypoints.remove(closestPose)


    # Adapt the orientation of each Waypoint to the previous Waypoint
    #for index in range(len(orderedWaypoints) - 1):

    #       ordererdWaypoints[i].pose.orientation.z = computeOrientation(orderedWaypoints[i], orderedWaypoints[i+1]):


    rospy.init_node('PathPlanner', anonymous=True)
    rate = rospy.Rate(10000) 					# 100hz
    pub = rospy.Publisher('goals', Path, queue_size=10)
 	
    #while not rospy.is_shutdown():

    #print "unordered Waypoints"
    #print unorderedWaypoints

    targetPath = Path()

    for temp_waypoint in unorderedWaypoints:
	tempPose = PoseStamped()
	tempPose.header.stamp = rospy.get_rostime()
	tempPose.pose = temp_waypoint
		
    	targetPath.poses.append(tempPose)
	

    #print unorderedWaypoints
    #print
    #print "//////////////////////////////////////////////////////////////////////////////"
    #print
    #print targetPath

    rospy.sleep(10.0)

    pub.publish(targetPath)

    rospy.sleep(10.0)
	
    #rate.sleep()




if __name__ == '__main__':
    	
	try:
    
        	initialPose = Pose()
        	initialPose.position.x = 12.7
        	initialPose.position.y = 6.3
        	initialPose.position.z = 0.00
        	initialPose.orientation.x = 0.000
        	initialPose.orientation.y = 0.000
        	initialPose.orientation.z = -0.0969236885705
        	initialPose.orientation.w = 0.995291815798
        
        
        	computeOptimalPath(initialPose)
    
	except rospy.ROSInterruptException:
        	pass

