# Copyright 2026 ROS 2 System Status Monitor contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""ROS 2 node that publishes local system status information."""

import platform

import psutil
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy
from status_interfaces.msg import SystemStatus


class SysStatusPub(Node):
    """Collect system metrics and publish them as SystemStatus messages."""

    def __init__(self):
        """Initialize parameters, the publisher, and the sampling timer."""
        super().__init__('sys_status_pub')

        self.declare_parameter('publish_rate', 1.0)
        publish_rate = float(self.get_parameter('publish_rate').value)
        if publish_rate <= 0.0:
            self.get_logger().warning(
                'publish_rate must be greater than zero; using 1.0 Hz'
            )
            publish_rate = 1.0

        # Prime psutil so the first published CPU sample is meaningful.
        psutil.cpu_percent(interval=None)

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
        )
        self._publisher = self.create_publisher(
            SystemStatus, 'system_status', qos_profile
        )
        self._timer = self.create_timer(
            1.0 / publish_rate, self.publish_status
        )

        self.get_logger().info(
            'Publishing system status on /system_status at '
            f'{publish_rate:.2f} Hz'
        )

    def publish_status(self):
        """Collect current metrics and publish one status message."""
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()

        message = SystemStatus()
        message.stamp = self.get_clock().now().to_msg()
        message.hostname = platform.node() or 'unknown'
        message.cpu_percent = float(psutil.cpu_percent(interval=None))
        message.memory_percent = float(memory.percent)
        message.memory_total = float(memory.total)
        message.memory_available = float(memory.available)
        message.net_sent = float(network.bytes_sent) if network else 0.0
        message.net_recv = float(network.bytes_recv) if network else 0.0

        self._publisher.publish(message)


def main(args=None):
    """Run the system status publisher node."""
    rclpy.init(args=args)
    node = None
    try:
        node = SysStatusPub()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
