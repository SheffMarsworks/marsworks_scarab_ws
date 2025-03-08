import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rover_description_dir = get_package_share_directory("rover_description")

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("rover_description"),
            "launch",
            "gazebo.launch.py",
        ),
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("rover_controller"),
            "launch",
            "controller.launch.py"
        ),
        launch_arguments={
            "use_simple_controller": "False",
            "use_python": "False"
        }.items(),
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("rover_controller"),
            "launch",
            "joystick_teleop.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "True"
        }.items()
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(rover_description_dir, "rviz", "display.rviz")],
    )

    return LaunchDescription(
        [
            gazebo,
            controller,
            joystick,
            rviz_node
        ]
    )
