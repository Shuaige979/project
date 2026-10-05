# Copyright 2026 ROS 2 System Status Monitor contributors
#
# SPDX-License-Identifier: MIT

# Timestamp when this status sample was collected.
builtin_interfaces/Time stamp

# Host name reported by the operating system.
string hostname

# CPU utilization in percent.
float32 cpu_percent

# Memory utilization in percent.
float32 memory_percent

# Total physical memory in bytes.
float32 memory_total

# Available physical memory in bytes.
float32 memory_available

# Cumulative number of bytes sent since system boot.
float32 net_sent

# Cumulative number of bytes received since system boot.
float32 net_recv


