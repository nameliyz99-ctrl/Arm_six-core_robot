#include <memory>
#include <vector>
#include <string>
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  auto const node = std::make_shared<rclcpp::Node>("multi_pose_test_node", node_options);

  // MoveIt 需要一个 Executor 来处理后台任务
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  std::thread([&executor]() { executor.spin(); }).detach();

  static const std::string PLANNING_GROUP = "test_group";
  moveit::planning_interface::MoveGroupInterface move_group_interface(node, PLANNING_GROUP);
  
  auto const logger = rclcpp::get_logger("multi_pose_test_node");

  // 定义动作序列
  std::vector<std::string> target_poses = {"home", "pose_a", "pose_b", "home"};

  RCLCPP_INFO(logger, "准备开始往返运动序列...");

  for (const auto& target : target_poses) {
    RCLCPP_INFO(logger, "正在规划至目标: %s", target.c_str());
    
    // 设置目标为 SRDF 中定义的名称
    move_group_interface.setNamedTarget(target);

    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    bool success = (move_group_interface.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    if (success) {
      RCLCPP_INFO(logger, "规划成功，开始执行...");
      move_group_interface.execute(my_plan);
    } else {
      RCLCPP_ERROR(logger, "无法规划至目标: %s", target.c_str());
    }

    // 每个动作完成后稍微停顿一下
    rclcpp::sleep_for(std::chrono::seconds(1));
  }

  RCLCPP_INFO(logger, "运动序列执行完毕！");
  
  rclcpp::shutdown();
  return 0;
}