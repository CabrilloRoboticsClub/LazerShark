"""
auv.launch.py

Launches ROS nodes for LazerShark AUV

Copyright (C) 2026-2027 Cabrillo Robotics Club

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Cabrillo Robotics Club
6500 Soquel Drive Aptos, CA 95003
cabrillorobotics@gmail.com
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from utils import json_tf2_parser


def generate_launch_description() -> LaunchDescription:
    """
    Launch with: `ros2 launch lazershark auv.launch.py`
    """

    nodes = [ 
        # Publish static TF for robot components described in resource/static_component_tf2.json
        *[Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                arguments=tf
            ) 
        for tf in json_tf2_parser.get_tf_arg_list("static_component_tf2.json")]
    ]

    return LaunchDescription(nodes)