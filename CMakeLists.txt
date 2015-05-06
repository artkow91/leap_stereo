cmake_minimum_required(VERSION 2.8.3)
project(leap_stereo)

find_package(catkin REQUIRED COMPONENTS roscpp rospy roslib std_msgs geometry_msgs message_generation sensor_msgs visualization_msgs camera_info_manager rospack camera_calibration_parsers)

find_package(OpenMP)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")


#add_message_files(
#    FILES
#    leap.msg
#    leapros.msg
#)

generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
   sensor_msgs
   visualization_msgs
)

catkin_package(
   INCLUDE_DIRS include
#  LIBRARIES leap_motion
   CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
#  DEPENDS system_lib
)

include_directories(include
  ${catkin_INCLUDE_DIRS} /home/artur/LeapSDK/include)

#install(PROGRAMS
#  scripts/leap_interface.py scripts/sender.py scripts/subscriber.py
#  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)


  add_executable(dane_kalibracyjne src/dane_kalibracyjne.cpp)
  target_link_libraries(dane_kalibracyjne
    ${catkin_LIBRARIES} /home/artur/LeapSDK/lib/x64/libLeap.so
  )

