"""
targetpoint.py

Integrates a Targetpoint TCM with the ROS network.

Copyright (C) 2025-2026 Cabrillo Robotics Club

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
import sys

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from rcl_interfaces.msg import ParameterDescriptor

from targetpoint_lib import targetpoint

class TargetPoint(Node):
    """
    Reads messages from a Targerpoint. Publishes each reading as an IMU message type to `imu/targetpoint`.

    ROS params:
        dev: `/dev/ttyUSB` port to read from.
        frameID: Frame ID of Targetpoint as specified by `tf` topic.
    """

    def __init__(self):
        """
        Initialize `targetpoint` node.
        """
        super().__init__("targetpoint")

        self.declare_params()

        self.G = 9.80665 # m/s^2
        self.frame_id = self.get_parameter("frame_id").value

        self.imu = targetpoint.TargetPoint(dev=self.get_parameter("dev").value)
        self.imu.select_comp("kQuaternion", "kGyroX", "kGyroY", "kGyroZ", "kAccelX", "kAccelY", "kAccelZ")

        self.publisher = self.create_publisher(Imu, "imu/targetpoint", 10)
        self.create_timer(1.0/30, self.callback)

    def declare_params(self) -> None:
        """
        Declares ros parameters for Targetpoint:
            dev: `/dev/ttyUSB` port to read from.
            frame_id: Frame ID of Targetpoint as specified by `tf` topic.
        """
        dev_descript = ParameterDescriptor(description="`/dev/ttyUSB` port to read from.")
        frame_id_descript = ParameterDescriptor(description="Frame ID of Targetpoint as specified by `tf` topic.")

        self.declare_parameter("dev", "Not set.", descriptor=dev_descript)
        self.declare_parameter("frame_id", "Not set.", descriptor=frame_id_descript)

    def callback(self):
        """
        Read data from targetoint and publish to `imu/targetpoint`.
        """
        imu_msg = Imu()
        data = self.imu.read_data()

        imu_msg.orientation.x = data["kQuaternion"][0]
        imu_msg.orientation.y = data["kQuaternion"][1]
        imu_msg.orientation.z = data["kQuaternion"][2]
        imu_msg.orientation.w = data["kQuaternion"][3]

        imu_msg.angular_velocity.x = data["kGyroX"]
        imu_msg.angular_velocity.y = data["kGyroY"]
        imu_msg.angular_velocity.z = data["kGyroZ"]

        imu_msg.linear_acceleration.x = data["kAccelX"] * self.G
        imu_msg.linear_acceleration.y = data["kAccelY"] * self.G
        imu_msg.linear_acceleration.z = data["kAccelZ"] * self.G

        imu_msg.header.frame_id = self.frame_id
        imu_msg.header.stamp.sec, imu_msg.header.stamp.nanosec = self.get_clock().now().seconds_nanoseconds()

        self.publisher.publish(imu_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TargetPoint()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == "__main__":
    main(sys.argv)
