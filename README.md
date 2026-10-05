# ROS 2 系统状态监看与 Qt 展示

本项目包含两个 ROS 2 功能包，目标环境为 **Ubuntu 22.04 + ROS 2 Humble**：

- `status_interfaces`：`ament_cmake` 接口包，定义 `SystemStatus` 自定义消息。
- `status_publisher`：`ament_python` 功能包，包含系统状态采集、发布节点和基于 PyQt5 的监听窗口。

## 功能

`sys_status_pub` 节点按固定频率采集以下信息并发布到 `system_status` 话题：

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `stamp` | `builtin_interfaces/Time` | 本条状态数据的采集时间 |
| `hostname` | `string` | 主机名 |
| `cpu_percent` | `float32` | CPU 总使用率，单位 `%` |
| `memory_percent` | `float32` | 内存使用率，单位 `%` |
| `memory_total` | `float32` | 内存总大小，单位 byte |
| `memory_available` | `float32` | 可用内存，单位 byte |
| `net_sent` | `float32` | 系统启动以来累计发送字节数，单位 byte |
| `net_recv` | `float32` | 系统启动以来累计接收字节数，单位 byte |

`status_gui` 节点订阅同一话题，并通过 Qt 窗口显示上述信息。

> `net_sent` 和 `net_recv` 使用的是 `psutil.net_io_counters()` 返回的累计值，不是瞬时速率。

## 项目结构

```text
.
├── README.md
└── src/
    ├── status_interfaces/                 # 消息接口包 (ament_cmake)
    │   ├── CMakeLists.txt
    │   ├── LICENSE
    │   ├── package.xml
    │   └── msg/
    │       └── SystemStatus.msg
    └── status_publisher/                  # Python 功能包 (ament_python)
        ├── launch/
        │   └── status_monitor.launch.py
        ├── package.xml
        ├── resource/status_publisher
        ├── setup.cfg
        ├── setup.py
        ├── status_publisher/
        │   ├── __init__.py
        │   ├── status_gui.py              # Qt 订阅/显示节点
        │   └── sys_status_pub.py          # 状态采集/发布节点
        └── test/
            ├── test_copyright.py
            ├── test_flake8.py
            └── test_pep257.py
```

## 依赖安装

先确保系统已经安装 ROS 2 Humble。然后在 Ubuntu 终端安装本项目运行依赖：

```bash
sudo apt update
sudo apt install python3-psutil python3-pyqt5
```

如果使用最小化 ROS 2 安装，还需安装构建和测试工具：

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-pytest
```

也可以在 Python 虚拟环境中安装 `psutil` 和 `PyQt5`，但运行节点时必须先 `source` ROS 2 和当前工作区的环境脚本。

## 编译

本项目仓库根目录本身就是 ROS 2 工作区，因为两个功能包都位于 `src` 目录。

```bash
cd ~/project
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
colcon build --symlink-install
source install/setup.bash
```

## 运行

### 方式一：分别启动两个终端

终端 1，启动数据采集和发布节点：

```bash
source ~/project/install/setup.bash
ros2 run status_publisher sys_status_pub
```

终端 2，启动 Qt 显示窗口：

```bash
source ~/project/install/setup.bash
ros2 run status_publisher status_gui
```

### 方式二：使用 launch 文件

```bash
source ~/project/install/setup.bash
ros2 launch status_publisher status_monitor.launch.py
```

launch 文件需要图形桌面环境。如果只是采集和记录消息，可以只运行 `sys_status_pub`。

## 检查与验证

查看自定义消息定义：

```bash
ros2 interface show status_interfaces/msg/SystemStatus
```

查看实时话题：

```bash
ros2 topic echo /system_status
```

修改发布频率（默认 `1.0` Hz）：

```bash
ros2 run status_publisher sys_status_pub --ros-args -p publish_rate:=2.0
```

运行测试：

```bash
colcon test --packages-select status_publisher
colcon test-result --verbose
```

## 上传到 GitHub

本项目的 GitHub 仓库地址：

https://github.com/Shuaige979/project

提交并推送更新：

```bash
git add .
git commit -m "docs: update README"
git push
```

## License

MIT
