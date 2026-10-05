#!/usr/bin/env python3
#
# Copyright 2026 ROS 2 System Status Monitor contributors
#
# SPDX-License-Identifier: MIT

import os
from glob import glob

from setuptools import find_packages, setup


package_name = 'status_publisher'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS 2 Developer',
    maintainer_email='developer@example.com',
    description='Publish and display ROS 2 system status information.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sys_status_pub = status_publisher.sys_status_pub:main',
            'status_gui = status_publisher.status_gui:main',
        ],
    },
)
