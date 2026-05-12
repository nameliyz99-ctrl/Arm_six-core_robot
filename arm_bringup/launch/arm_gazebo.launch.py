import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. 获取各个包的路径
    arm_moveit_config = get_package_share_directory('arm_moveit_config')
    arm_description = get_package_share_directory('arm_description')

    # 2. 启动 Gazebo (加载一个空世界)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 3. Spawn 机器人 (把 URDF 放到 Gazebo 里)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'arm'],
        output='screen'
    )

    # 4. 加载并启动 joint_state_broadcaster (发布关节状态)
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    # 5. 加载并启动你的 test_group_controller (接收 MoveIt 指令)
    load_arm_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'test_group_controller'],
        output='screen'
    )

    # 6. 包含 MoveIt 的启动文件 (让 MoveIt 跑起来)
    # 注意：这里通常调用 moveit_config 包里的 demo.launch.py，但要设为 use_sim_time:=true
    moveit_demo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(arm_moveit_config, 'launch', 'demo.launch.py')]),
        launch_arguments={'use_sim_time': 'true'}.items(),
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
        load_joint_state_broadcaster,
        # 确保在机器人生成后再加载控制器
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_arm_controller],
            )
        ),
        moveit_demo,
    ])