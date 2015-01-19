cmake_minimum_required(VERSION 2.8.3)
project(slalom)

# Find the catkin build system and the other dependent packages
find_package(catkin REQUIRED COMPONENTS rospy std_msgs geometry_msgs message_generation)


#add_message_files(
#  FILES
#)

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
)

# Declare the catkin package
catkin_package()

# Declare executables
#add_executable(wifi_publisher wifi_publisher.py)
#add_executable(wifi_database wifi_database.py)
#add_executable(wifi_classifier wifi_classifier.py)
#add_executable(initialLocation initialLocation.py)

# Specify linking libraries
# target_link_libraries(wifi_localization ${catkin_LIBRARIES})

