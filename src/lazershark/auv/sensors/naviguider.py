"""
naviguider.py

Integrates a Naviguider with the ROS network.

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
from time import sleep
from serial import Serial

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from rcl_interfaces.msg import ParameterDescriptor

from naviguider_simpleserial import (
    decode_line,
    encode_set_rotation_vector_sensor_rate,
    encode_set_linear_acceleration_sensor_rate,
    encode_system_restart,
    encode_set_gyroscope_sensor_rate,
    sensor_event,
)


class Naviguider(Node):
    """
    Reads messages from a Naviguider. Publishes each reading as an IMU message type to `imu/naviguider`.

    ROS params:
        dev: `/dev/ttyUSB` port to read from.
        frameID: Frame ID of Naviguider as specified by `tf` topic.
    """
    
    def __init__(self):
        """
        Initialize `naviguider` node.
        """
        super().__init__("naviguider")

        self.declare_params()

        self.SETUP_DELAY = 2 # s
    
        self.publisher = self.create_publisher(Imu, "imu/naviguider", 10)

        self.serial_init()
        self.get_data()
    
    def declare_params(self) -> None:
        """
        Declares ros parameters for Naviguider:
            dev: `/dev/ttyUSB` port to read from.
            frame_id: Frame ID of Naviguider as specified by `tf` topic.
        """
        dev_descript = ParameterDescriptor(description="`/dev/ttyUSB` port to read from.")
        frame_id_descript = ParameterDescriptor(description="Frame ID of Naviguider as specified by `tf` topic.")

        self.declare_parameter("dev", "Not set.", descriptor=dev_descript)
        self.declare_parameter("frame_id", "Not set.", descriptor=frame_id_descript)

    def serial_init(self):
        """
        Initialize the serial port and 
        """
        dev = self.get_parameter("dev").value
        self.serial_port = Serial(dev, 115200)
        self.get_logger().info(f"Port {dev} open: {self.serial_port.is_open}")
        
        self.serial_port.write(encode_system_restart().encode())
        sleep(self.SETUP_DELAY)

        # Request that the IMU sends us orientaton, angular velocity, and linear acceleration data
        self.serial_port.write(encode_set_rotation_vector_sensor_rate(15).encode())
        sleep(self.SETUP_DELAY)
        self.serial_port.write(encode_set_linear_acceleration_sensor_rate(15).encode())
        sleep(self.SETUP_DELAY)
        self.serial_port.write(encode_set_gyroscope_sensor_rate(15).encode())
        sleep(self.SETUP_DELAY)

        self.get_logger().info(f"Serial init complete.")

    def get_data(self):
        """
        Revieve data events from Naviguider and publish to `imu/naviguider`.
        """
        imu_msg = Imu()
        imu_msg.header.frame_id = self.get_parameter("frameID").value

        # The Naviguider streams sensor data as event packets (rotation, gyroscope, linear acceleration), 
        # There is no defined order and no defined rate at which we will recieve these sensor events 
        # To construct a complete ROS Imu message, we accumulate the latest events, tracking recieved events in a bit-map
        #   0b001 -> orientation event
        #   0b010 -> angular velocity event
        #   0b100 -> linear acceleration event
        # Once all three components are recieved (0b111) we publish the complete message.
        update_map = 0b000

        while True:
            try:
                data = self.serial_port.readline().decode("utf-8").strip()
                if data:
                    # If there is valid data, decode as an `Event`
                    event = decode_line(data)
            except ValueError as e:
                self.get_logger().warn(f"ValueError: {e}")
                continue
            except TypeError:
                self.get_logger().warn(f"TypeError: {e}")
                continue

            if event:
                if type(event) is sensor_event.RotationVectorSensorEvent:
                    imu_msg.orientation.x = event.qx
                    imu_msg.orientation.y = event.qy
                    imu_msg.orientation.z = event.qz
                    imu_msg.orientation.w = event.qw
                    update_map |= 0b001
                if type(event) is sensor_event.GyroscopeSensorEvent:
                    imu_msg.angular_velocity.x = event.x
                    imu_msg.angular_velocity.y = event.y
                    imu_msg.angular_velocity.z = event.z
                    update_map |= 0b010
                if type(event) is sensor_event.LinearAccelerationSensorEvent:
                    imu_msg.linear_acceleration.x = event.x
                    imu_msg.linear_acceleration.y = event.y
                    imu_msg.linear_acceleration.z = event.z
                    update_map |= 0b100
                if update_map == 0b111:
                    imu_msg.header.stamp.sec, imu_msg.header.stamp.nanosec = self.get_clock().now().seconds_nanoseconds()
                    self.publisher.publish(imu_msg)
                    update_map = 0b000


def main(args=None):
    rclpy.init(args=args)
    node = Naviguider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == "__main__":
    main(sys.argv)