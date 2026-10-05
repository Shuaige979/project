# Copyright 2026 ROS 2 System Status Monitor contributors
#
# SPDX-License-Identifier: MIT

"""Launch the system status publisher and Qt monitor together."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Create the launch description."""
    return LaunchDescription([
        Node(
            package='status_publisher',
            executable='sys_status_pub',
            name='sys_status_pub',
            output='screen',
        ),
        Node(
            package='status_publisher',
            executable='status_gui',
            name='status_gui',
            output='screen',
        ),
    ])

