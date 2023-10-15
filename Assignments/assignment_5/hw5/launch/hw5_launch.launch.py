import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

import xacro


ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='',
                          description='Robot namespace'),
    DeclareLaunchArgument('world', default_value='empty',
                          description='Eddie World'),
    DeclareLaunchArgument('model', default_value='eddie_kinect_v1',
                          choices=['eddie_kinect_v1'],
                          description='Eddiebot Model'),
]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'{pose_element} component of the robot pose.'))

def generate_launch_description():
    
    gz_ros2_control_demos_path = os.path.join(
        get_package_share_directory('eddiebot_gazebo'))

    xacro_file = os.path.join(gz_ros2_control_demos_path,
                              'worlds',
                              'maze_marked')

    # doc = xacro.parse(open(xacro_file))
    # xacro.process_doc(doc)
    
    

    pkg_eddiebot_gazebo = get_package_share_directory(
        'eddiebot_gazebo')

    # Paths
    gz_sim_launch = PathJoinSubstitution(
        [pkg_eddiebot_gazebo, 'launch', 'gz_sim.launch.py'])
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_eddiebot_gazebo, 'launch', 'eddiebot_spawn.launch.py'])
    
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gz_sim_launch]),
        launch_arguments=[
            ('world', xacro_file)
        ]
    )

    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawn_launch]),
        launch_arguments=[
            ('namespace', LaunchConfiguration('namespace')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw'))]
    )
    kinect_camera_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='camera_bridge',
        output='screen',
        arguments=[
            ['/kinect_rgbd_camera/image' +
             '@sensor_msgs/msg/Image' +
             '[gz.msgs.Image'],
             ['/model/eddiebot/cmd_vel'+
              '@geometry_msgs/msg/Twist'+
              ']gz.msgs.Twist'],
        ]
    )

    hw5_node = Node(
                package='hw5',
                executable='main',
                name='main',
            )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(gz_sim)
    ld.add_action(robot_spawn)
    ld.add_action(kinect_camera_bridge)
    ld.add_action(hw5_node)
    return ld


