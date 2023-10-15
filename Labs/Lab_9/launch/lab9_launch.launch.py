import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node



def generate_launch_description():
    
    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', "gz_sim.launch.py")),
        launch_arguments=[('gz_args', '/home/redha/ros2_ws/src/lab9/sdf/maze.sdf')]
    )
    
    laser_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='camera_bridge',
        output='screen',
        arguments=[
            ['/lidar' +
             '@sensor_msgs/msg/LaserScan' +
             '[gz.msgs.LaserScan'],
        ]
    )
    tf_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='tf2_bridge',
        output='screen',
        arguments=[
            ['/vehicle_blue/chassis/tf' +
             '@tf2_msgs/msg/TFMessage' +
             '[gz.msgs.Pose_V'],
        ],
        remappings=[
                ('/vehicle_blue/chassis/tf', '/tf'),
        ]
    )
    gpu_lidar_to_chassis = Node (
        package='tf2_ros',
        executable='static_transform_publisher',
        name='gpu_lidar_to_chassis',
        arguments=[
            "0", "0", "0", "0", "0", "0", "/vehicle_blue/chassis", "vehicle_blue/chassis/gpu_lidar"
        ]
    )
    odom_to_world = Node (
        package='tf2_ros',
        executable='static_transform_publisher',
        name='odom_to_world',
        arguments=[
            "0", "0", "0", "0", "0", "0", "/world", "vehicle_blue/chassis/odom"
        ]
    )
    ld = LaunchDescription()
    ld.add_action(robot_spawn)
    ld.add_action(laser_bridge)
    ld.add_action(tf_bridge)
    ld.add_action(gpu_lidar_to_chassis)
    ld.add_action(odom_to_world)
    return ld

