cmake_minimum_required(VERSION 3.8)
project(lazershark)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# cpp nodes
add_executable(test_publisher sensors/test.cpp)

ament_target_dependencies(
  # cpp executables
  test_publisher

  # other dependencies
  rclcpp
  std_msgs
)

install(TARGETS
  # cpp programs  
  test_publisher
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  # python scripts
  sensors/test_subscriber.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()