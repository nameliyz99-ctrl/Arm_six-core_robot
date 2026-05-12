cmake_minimum_required(VERSION 3.8)
project(arm_bringup)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. 查找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(geometry_msgs REQUIRED)

# 2. 添加可执行文件
add_executable(random_test_node src/random_test.cpp)

# 3. 关键修正：使用 ament 宏来链接依赖
# 不要使用 target_link_libraries，这会绕过一些复杂的路径问题
ament_target_dependencies(random_test_node
  rclcpp
  moveit_ros_planning_interface
  geometry_msgs
)

# 4. 安装
install(TARGETS
  random_test_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

ament_package()