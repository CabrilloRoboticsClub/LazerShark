"""
json_tf2_parser.py

Provides functions which parse a json file which describes ROS tf2 transforms
and converts them into a list of arguements to be provided to a tf2_ros static_transform_publisher.

Copyright (C) 2023-2024 Cabrillo Robotics Club

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

import json
from importlib.resources import open_text

def get_tf_arg_list(file: str) -> list[list[str]]:
    """
    Converts JSON file of transforms into a list of lists list of arguements which 
    can be provided to `tf2_ros` `static_transform_publisher`.

    Usage:
        ```
        *[Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                arguments=tf
            ) 
        for tf in json_tf2_parser.get_tf_arg_list("file.json")]
        ```

    Args:
        file: JSON file located in `lazershark/resources` which contains transforms.

    Returns:
        List of arguements for a `static_transform_publisher`.
    """
    with open_text("resource", file) as f:
        return [_parse_tf_to_arg_list(tf) for tf in json.load(f).values()]

def _parse_tf_to_arg_list(tf: dict) -> list[str]:
    """
    Helper method to convert a transform into an arguement list for `static_transform_publisher`.

    Args:
        tf: A single transform

    Returns:
        Arguement list for `static_transform_publisher`.
    """
    return [
        "--x", f"{tf['translation']['x']}", 
        "--y", f"{tf['translation']['y']}", 
        "--z", f"{tf['translation']['z']}",
        "--qx", f"{tf['rotation']['x']}", 
        "--qy", f"{tf['rotation']['y']}", 
        "--qz", f"{tf['rotation']['z']}", 
        "--qw", f"{tf['rotation']['w']}",
        "--frame-id", f"{tf['frame_id']}", 
        "--child-frame-id", f"{tf['child_frame_id']}"
    ]