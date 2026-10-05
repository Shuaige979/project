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
"""Qt window that subscribes to and displays ROS 2 system status."""

import sys
from datetime import datetime

import rclpy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from rclpy.node import Node
from rclpy.qos import QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy
from status_interfaces.msg import SystemStatus


def format_bytes(value):
    """Return a byte count in a compact, human-readable form."""
    size = float(value)
    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB')
    for unit in units:
        if abs(size) < 1024.0 or unit == units[-1]:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} TiB'


def format_stamp(stamp):
    """Convert a builtin_interfaces/Time value to a local timestamp."""
    seconds = stamp.sec + stamp.nanosec / 1_000_000_000.0
    try:
        value = datetime.fromtimestamp(seconds)
    except (OSError, OverflowError, ValueError):
        return f'{stamp.sec}.{stamp.nanosec:09d}'
    return value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


class MetricCard(QFrame):
    """Small panel used to display one system status field."""

    def __init__(self, title, parent=None):
        """Create a metric card with its title and placeholder value."""
        super().__init__(parent)
        self.setObjectName('metricCard')

        title_label = QLabel(title)
        title_label.setObjectName('cardTitle')

        self.value_label = QLabel('--')
        self.value_label.setObjectName('cardValue')
        self.value_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.value_label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        """Update the value shown in this card."""
        self.value_label.setText(value)


class StatusMonitorNode(Node):
    """Subscribe to SystemStatus messages from sys_status_pub."""

    def __init__(self):
        """Create the subscription and initialize the latest message."""
        super().__init__('status_gui')
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
        )
        self.latest_message = None
        self._subscription = self.create_subscription(
            SystemStatus,
            'system_status',
            self._status_callback,
            qos_profile,
        )

    def _status_callback(self, message):
        self.latest_message = message


class StatusWindow(QMainWindow):
    """Main Qt window for system status monitoring."""

    def __init__(self, node):
        """Build the UI and connect ROS spinning to a Qt timer."""
        super().__init__()
        self._node = node
        self._has_update = False

        self.setWindowTitle('ROS 2 系统状态监看')
        self.setMinimumSize(680, 560)
        self._build_ui()

        self._spin_timer = QTimer(self)
        self._spin_timer.timeout.connect(self._spin_ros)
        self._spin_timer.start(50)

        self._ui_timer = QTimer(self)
        self._ui_timer.timeout.connect(self._refresh_ui)
        self._ui_timer.start(200)

    def _build_ui(self):
        central = QWidget()
        central.setObjectName('central')
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(22, 20, 22, 20)
        root_layout.setSpacing(14)

        title = QLabel('系统实时状态')
        title.setObjectName('pageTitle')
        subtitle = QLabel('订阅话题 /system_status')
        subtitle.setObjectName('subtitle')

        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        self._cards = {
            'stamp': MetricCard('采集时间'),
            'hostname': MetricCard('主机名'),
            'cpu': MetricCard('CPU 使用率'),
            'memory_percent': MetricCard('内存使用率'),
            'memory_total': MetricCard('内存总大小'),
            'memory_available': MetricCard('剩余内存'),
            'net_sent': MetricCard('网络发送量（累计）'),
            'net_recv': MetricCard('网络接收量（累计）'),
        }

        order = (
            'stamp',
            'hostname',
            'cpu',
            'memory_percent',
            'memory_total',
            'memory_available',
            'net_sent',
            'net_recv',
        )
        for index, key in enumerate(order):
            grid.addWidget(self._cards[key], index // 2, index % 2)

        root_layout.addLayout(grid)
        root_layout.addStretch(1)

        self._connection_label = QLabel('等待状态消息...')
        self._connection_label.setObjectName('connection')
        self._connection_label.setAlignment(Qt.AlignCenter)
        root_layout.addWidget(self._connection_label)

        self.setStyleSheet(
            '''
            QWidget#central {
                background: #f3f6fa;
                color: #172033;
                font-family: "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
            }
            QLabel#pageTitle {
                font-size: 25px;
                font-weight: 700;
                color: #14213d;
            }
            QLabel#subtitle {
                color: #667085;
                font-size: 12px;
            }
            QFrame#metricCard {
                background: white;
                border: 1px solid #dbe2ea;
                border-radius: 9px;
            }
            QLabel#cardTitle {
                color: #667085;
                font-size: 12px;
            }
            QLabel#cardValue {
                color: #14213d;
                font-size: 19px;
                font-weight: 600;
            }
            QLabel#connection {
                color: #667085;
                font-size: 12px;
                padding: 8px;
                background: #e9eef5;
                border-radius: 6px;
            }
            '''
        )

    def _spin_ros(self):
        if rclpy.ok():
            rclpy.spin_once(self._node, timeout_sec=0.0)

    def _refresh_ui(self):
        message = self._node.latest_message
        if message is None:
            return

        self._cards['stamp'].set_value(format_stamp(message.stamp))
        self._cards['hostname'].set_value(message.hostname or 'unknown')
        self._cards['cpu'].set_value(f'{message.cpu_percent:.1f} %')
        self._cards['memory_percent'].set_value(
            f'{message.memory_percent:.1f} %'
        )
        self._cards['memory_total'].set_value(
            format_bytes(message.memory_total)
        )
        self._cards['memory_available'].set_value(
            format_bytes(message.memory_available)
        )
        self._cards['net_sent'].set_value(format_bytes(message.net_sent))
        self._cards['net_recv'].set_value(format_bytes(message.net_recv))

        if not self._has_update:
            self._has_update = True
            self._connection_label.setText('状态数据接收正常')
            self._connection_label.setStyleSheet(
                'color: #087443; background: #e6f4ea; '
                'border-radius: 6px; padding: 8px;'
            )

    def closeEvent(self, event):
        """Stop ROS communication before closing the window."""
        self._spin_timer.stop()
        self._ui_timer.stop()
        self._node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        event.accept()


def main(args=None):
    """Run the Qt system status monitor."""
    rclpy.init(args=args)
    application = QApplication(sys.argv)
    node = StatusMonitorNode()
    window = StatusWindow(node)
    window.show()
    exit_code = application.exec_()
    if rclpy.ok():
        rclpy.shutdown()
    return exit_code


if __name__ == '__main__':
    main()
