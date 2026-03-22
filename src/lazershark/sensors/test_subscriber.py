#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class TestSubscriber(Node):

    def __init__(self):
        super().__init__("test_subscriber")
        self.subscription = self.create_subscription(String,"test", self.callback, 10)

    def callback(self, msg: String):
        self.get_logger().info(f"BALLS: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    test = TestSubscriber()
    rclpy.spin(test)
    rclpy.shutdown()


if __name__ == "__main__":
    main()