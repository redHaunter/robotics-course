from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='turtlemania',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'},
            ]
        ),
        Node(
            package='turtlemania',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[
                {'turtlename': 'turtle2'},
            ]
        ),
        Node(
            package='turtlemania',
            executable='turtle_tf2_broadcaster',
            name='broadcaster3',
            parameters=[
                {'turtlename': 'turtle3'},
            ]
        ),
        Node(
            package='turtlemania',
            executable='turtle_tf2_broadcaster',
            name='broadcaster4',
            parameters=[
                {'turtlename': 'turtle4'},
            ]
        ),

        DeclareLaunchArgument(
            'target_frame_1', default_value='turtle1',
            description='Target frame name.'
        ),
        DeclareLaunchArgument(
            'source_frame_1', default_value='turtle2',
            description='Target frame name.'
        ),

        Node(
            package='turtlemania',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[
                {'target_frame': LaunchConfiguration('target_frame_1')},
                {'source_frame': LaunchConfiguration('source_frame_1')},
            ]
        ),



        DeclareLaunchArgument(
            'target_frame_2', default_value='turtle2',
            description='Target frame name.'
        ),
        DeclareLaunchArgument(
            'source_frame_2', default_value='turtle3',
            description='Target frame name.'
        ),

        Node(
            package='turtlemania',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[
                {'target_frame': LaunchConfiguration('target_frame_2')},
                {'source_frame': LaunchConfiguration('source_frame_2')},
            ]
        ),


        DeclareLaunchArgument(
            'target_frame_3', default_value='turtle3',
            description='Target frame name.'
        ),
        DeclareLaunchArgument(
            'source_frame_3', default_value='turtle4',
            description='Target frame name.'
        ),

        Node(
            package='turtlemania',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[
                {'target_frame': LaunchConfiguration('target_frame_3')},
                {'source_frame': LaunchConfiguration('source_frame_3')},
            ]
        ),

    ])