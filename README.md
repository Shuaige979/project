# ROS 2 绯荤粺鐘舵€佺洃鐪嬩笌 Qt 灞曠ず

鏈」鐩寘鍚袱涓?ROS 2 鍔熻兘鍖咃紝鐩爣鐜涓?**Ubuntu 22.04 + ROS 2 Humble**锛?
- `status_interfaces`锛歚ament_cmake` 鎺ュ彛鍖咃紝瀹氫箟 `SystemStatus` 鑷畾涔夋秷鎭€?- `status_publisher`锛歚ament_python` 鍔熻兘鍖咃紝鍖呭惈绯荤粺鐘舵€侀噰闆嗐€佸彂甯冭妭鐐瑰拰鍩轰簬 PyQt5 鐨勭洃鍚獥鍙ｃ€?
## 鍔熻兘

`sys_status_pub` 鑺傜偣鎸夊浐瀹氶鐜囬噰闆嗕互涓嬩俊鎭苟鍙戝竷鍒?`system_status` 璇濋锛?
| 瀛楁 | 绫诲瀷 | 鍚箟 |
| --- | --- | --- |
| `stamp` | `builtin_interfaces/Time` | 鏈潯鐘舵€佹暟鎹殑閲囬泦鏃堕棿 |
| `hostname` | `string` | 涓绘満鍚?|
| `cpu_percent` | `float32` | CPU 鎬讳娇鐢ㄧ巼锛屽崟浣?`%` |
| `memory_percent` | `float32` | 鍐呭瓨浣跨敤鐜囷紝鍗曚綅 `%` |
| `memory_total` | `float32` | 鍐呭瓨鎬诲ぇ灏忥紝鍗曚綅 byte |
| `memory_available` | `float32` | 鍙敤鍐呭瓨锛屽崟浣?byte |
| `net_sent` | `float32` | 绯荤粺鍚姩浠ユ潵绱鍙戦€佸瓧鑺傛暟锛屽崟浣?byte |
| `net_recv` | `float32` | 绯荤粺鍚姩浠ユ潵绱鎺ユ敹瀛楄妭鏁帮紝鍗曚綅 byte |

`status_gui` 鑺傜偣璁㈤槄鍚屼竴璇濋锛屽苟閫氳繃 Qt 绐楀彛鏄剧ず涓婅堪淇℃伅銆?

> `net_sent` 鍜?`net_recv` 浣跨敤鐨勬槸 `psutil.net_io_counters()` 杩斿洖鐨勭疮璁″€硷紝涓嶆槸鐬椂閫熺巼銆?
## 椤圭洰缁撴瀯

```text
.
鈹溾攢鈹€ README.md
鈹斺攢鈹€ src/
    鈹溾攢鈹€ status_interfaces/                 # 娑堟伅鎺ュ彛鍖?(ament_cmake)
    鈹?  鈹溾攢鈹€ CMakeLists.txt
    鈹?  鈹溾攢鈹€ LICENSE
    鈹?  鈹溾攢鈹€ package.xml
    鈹?  鈹斺攢鈹€ msg/
    鈹?      鈹斺攢鈹€ SystemStatus.msg
    鈹斺攢鈹€ status_publisher/                  # Python 鍔熻兘鍖?(ament_python)
        鈹溾攢鈹€ launch/
        鈹?  鈹斺攢鈹€ status_monitor.launch.py
        鈹溾攢鈹€ package.xml
        鈹溾攢鈹€ resource/status_publisher
        鈹溾攢鈹€ setup.cfg
        鈹溾攢鈹€ setup.py
        鈹溾攢鈹€ status_publisher/
        鈹?  鈹溾攢鈹€ __init__.py
        鈹?  鈹溾攢鈹€ status_gui.py              # Qt 璁㈤槄/鏄剧ず鑺傜偣
        鈹?  鈹斺攢鈹€ sys_status_pub.py          # 鐘舵€侀噰闆?鍙戝竷鑺傜偣
        鈹斺攢鈹€ test/
            鈹溾攢鈹€ test_copyright.py
            鈹溾攢鈹€ test_flake8.py
            鈹斺攢鈹€ test_pep257.py
```

## 渚濊禆瀹夎

鍏堢‘淇濈郴缁熷凡缁忓畨瑁?ROS 2 Humble銆傜劧鍚庡湪 Ubuntu 缁堢瀹夎鏈」鐩繍琛屼緷璧栵細

```bash
sudo apt update
sudo apt install python3-psutil python3-pyqt5
```

濡傛灉浣跨敤鏈€灏忓寲 ROS 2 瀹夎锛岃繕闇€瀹夎鏋勫缓鍜屾祴璇曞伐鍏凤細

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-pytest
```

涔熷彲浠ュ湪 Python 铏氭嫙鐜涓畨瑁?`psutil` 鍜?`PyQt5`锛屼絾杩愯鑺傜偣鏃跺繀椤诲厛 `source` ROS 2 鍜屽綋鍓嶅伐浣滃尯鐨勭幆澧冭剼鏈€?
## 缂栬瘧

灏?`status_interfaces` 鍜?`status_publisher` 鏀惧叆 ROS 2 宸ヤ綔鍖虹殑 `src` 鐩綍锛?
```bash
mkdir -p ~/ros2_ws/src
cp -r src/status_interfaces src/status_publisher ~/ros2_ws/src/
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
colcon build --symlink-install
source install/setup.bash
```

## 杩愯

### 鏂瑰紡涓€锛氬垎鍒惎鍔ㄤ袱涓粓绔?
缁堢 1锛屽惎鍔ㄦ暟鎹噰闆嗗拰鍙戝竷鑺傜偣锛?
```bash
source ~/ros2_ws/install/setup.bash
ros2 run status_publisher sys_status_pub
```

缁堢 2锛屽惎鍔?Qt 鏄剧ず绐楀彛锛?
```bash
source ~/ros2_ws/install/setup.bash
ros2 run status_publisher status_gui
```

### 鏂瑰紡浜岋細浣跨敤 launch 鏂囦欢

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch status_publisher status_monitor.launch.py
```

launch 鏂囦欢闇€瑕佸浘褰㈡闈㈢幆澧冦€傚鏋滃彧鏄噰闆嗗拰璁板綍娑堟伅锛屽彲浠ュ彧杩愯 `sys_status_pub`銆?
## 妫€鏌ヤ笌楠岃瘉

鏌ョ湅鑷畾涔夋秷鎭畾涔夛細

```bash
ros2 interface show status_interfaces/msg/SystemStatus
```

鏌ョ湅瀹炴椂璇濋锛?
```bash
ros2 topic echo /system_status
```

淇敼鍙戝竷棰戠巼锛堥粯璁?`1.0` Hz锛夛細

```bash
ros2 run status_publisher sys_status_pub --ros-args -p publish_rate:=2.0
```

杩愯娴嬭瘯锛?
```bash
colcon test --packages-select status_publisher
colcon test-result --verbose
```

## 涓婁紶鍒?GitHub锛圥ublic锛?
鍏堝湪鏈満瀹夎 Git锛屽苟纭繚宸茬粡鐧诲綍 GitHub銆傞」鐩牴鐩綍鍒濆鍖栧苟鎻愪氦锛?
```bash
cd /path/to/this/project
git init -b main
git add .
git commit -m "feat: add ROS 2 system status monitor"
```

浣跨敤 GitHub CLI 鍒涘缓 Public 浠撳簱骞舵帹閫侊細

```bash
gh repo create ros2-system-status-monitor --public --source=. --remote=origin --push
```

涔熷彲浠ュ厛鍦ㄧ綉椤靛垱寤?Public 绌轰粨搴擄紝鍐嶆墽琛岋細

```bash
git remote add origin https://github.com/<浣犵殑鐢ㄦ埛鍚?/ros2-system-status-monitor.git
git push -u origin main
```

## License

MIT

