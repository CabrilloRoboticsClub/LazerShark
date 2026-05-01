"""
a50.py

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
import sys
from time import sleep
import socket
import json

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rcl_interfaces.msg import ParameterDescriptor

class A50(Node):
    """
    Reads data from a Waterlinked DVL A50 and publishes each reading as an Odometry message to `dvl/a50`.

    Ros2 params:
        TCP_IP: Local IP address of the A50's TCP server.
        TCP_PORT: Port the A50's TCP server is running on.
        frame_id: Frame ID of A50 as specified by `tf` topic.
    """

    def __init__(self):
        """
        Initialize `A50` node.
        """
        super().__init__("a50")

        self.publisher = self.create_publisher(Odometry, "dvl/a50", 10)

        self.declare_params()
        self.TCP_IP   = self.get_parameter("TCP_IP").value
        self.TCP_PORT = int(self.get_parameter("TCP_PORT").value)
        self.frame_id = self.get_parameter("frame_id").value
    
        # Holds start of next message for next callback.
        self.old_data = ""

        self.connect()

        self.timer = self.create_timer(1/10.0, self.callback)

    def declare_params(self) -> None:
        """
        Declares Ros2 parameters for A50:
            TCP_IP: Local IP address of the A50's TCP server.
            TCP_PORT: Port the A50's TCP server is running on.
            frame_id: Frame ID of A50 as specified by `tf` topic.
        """
        tcp_ip_descript = ParameterDescriptor(description="Local IP address of the A50's TCP server.")
        tcp_port_descript = ParameterDescriptor(description="Port the A50's TCP server is running on.")
        frame_id_descript = ParameterDescriptor(description="Frame ID of A50 as specified by `tf` topic.")

        self.declare_parameter("TCP_IP",    "Not set.", descriptor=tcp_ip_descript)
        self.declare_parameter("TCP_PORT",  "Not set.", descriptor=tcp_port_descript)
        self.declare_parameter("frame_id",  "Not set.", descriptor=frame_id_descript)

    def connect(self) -> None:
        """
        Connect to TCP server, reattempts connection after one second upon failure.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.TCP_IP, self.TCP_PORT))
        except socket.error as e:
            self.get_logger().warn(f"Unable to connect to socket:\n{e}\nReconnecting...") 
            sleep(1)
            # TODO: Retry without recursion.
            self.connect()

    def get_data(self) -> str:
        """
        Reads from the socket until a complete A50 message is read.

        Returns:
            A complete message as a str.
        """
        data = self.old_data

        # Messages are delimited by newlines.
        while "\n" not in data:
            try: 
                new_data = self.socket.recv(1).decode()
            except socket.timeout as e:
                new_data = ""
                self.get_logger().warn(f"Socket timeout:\n{e}\nReconnecting...")
                self.connect()
                continue

            if len(new_data) == 0:
                self.get_logger().warn(f"Socket closed.\nReconnecting...")
                self.connect()
            else:
                data += new_data

        data, self.old_data = data.split("\n")

        return data

    def callback(self) -> None:
        """
        Read data from A50 and publish to `dvl/a50`.
        """
        msg = Odometry()
        msg.header.frame_id = self.frame_id

        data = json.loads(self.get_data())

        # Ignore dead reckoning data.
        while data["type"] != "velocity":
            data = json.loads(self.get_data())

        # FIXME: This should be the z from dead reckoning.
        # TODO: Make a relative offset rather than absolute altitude.
        msg.pose.pose.position.z = data["altitude"]

        msg.twist.twist.linear.x = data["vx"]
        msg.twist.twist.linear.y = data["vy"]
        msg.twist.twist.linear.z = data["vz"]

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = A50()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == "__main__":
    main(sys.argv)
