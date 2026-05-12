# 24赛季国赛工程机械臂 moveit2 配置文件

[动手学Moveit2|使用配置助手创建自己机械臂的功能包](https://mp.weixin.qq.com/s?__biz=MzkzMzI2MTU2Nw==&mid=2247487446&idx=1&sn=f913e65bc359578144b244499905759b&chksm=c24e7646f539ff50c6057346905088d87c78e0e58bd1ff127b4a2dad4681127c76c21c56beca&token=895124457&lang=zh_CN#rd)
[动手学Moveit2 | 运行配置好的机械臂功能demo](https://mp.weixin.qq.com/s?__biz=MzkzMzI2MTU2Nw==&mid=2247487456&idx=1&sn=33421159364ac21c3f47c5cebd886a54&chksm=c24e7670f539ff6648fa315df6267df2a1c949494781df4c030530a79c56895731684bd9d5d2&token=895124457&lang=zh_CN#rd)

[URDF/SRDF介绍](https://blog.csdn.net/ryanji/article/details/139594556)

## 统一规定

同样，moveit 生成的包名指定为 `arm_moveit_config`，文件夹名可为 `xxx_arm_moveit_config` 以作区分。

## 环境安装

```bash
sudo apt install ros-humble-moveit ros-humble-moveit-setup-assistant -y
sudo apt install ros-humble-controller-manager -y
sudo apt install ros-humble-joint-trajectory-controller ros-humble-joint-state-broadcaster -y
```

## 生成 moveit2 所需文件

```bash
# 提前进 moveit2 和机械臂描述文件urdf的工作环境
# 如 moveit2 在 ~/ws_moveit 路径编译
# 如 机械臂描述文件urdf 在 ~/Desktop/arm_ws 路径编译
# source ~/ws_moveit/install/setup.bash 
# source ~/Desktop/arm_ws/install/setup.bash 

ros2 run moveit_setup_assistant moveit_setup_assistant

# 之后参考教程进行配置并生成 moveit2 所需文件
```

## 可视化

```bash
# 提前进入xxx_moveit_config的工作环境
# 如 xxx_moveit_config 在 ~/Desktop/arm_ws 路径编译
# source ~/Desktop/arm_ws/install/setup.bash 

ros2 launch arm_moveit_config demo.launch.py 
```