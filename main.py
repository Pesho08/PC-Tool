import psutil
import time
import os
from xulbux import System


def get_cpu_usage():
  cores = psutil.cpu_count()
  usage = psutil.cpu_percent(interval=1)
  return cores, usage


def get_memory_usage():
  mem = psutil.virtual_memory()
  total_mem_gb = round((mem.total / 1024**3), 2)
  total_mem_av = round((mem.available / 1024**3), 2)
  total_mem_pc = mem.percent
  mem_used = round((mem.used / 1024**3), 2)
  return total_mem_gb, total_mem_av, total_mem_pc, mem_used


def get_disk_usage():
  disk = psutil.disk_usage('/')
  total_disk_gb = round((disk.total / 1024**3), 2)
  used_disk_gb = round((disk.used / 1024**3), 2)
  free_disk_gb = round((disk.free / 1024**3), 2)
  disk_usage_pc = disk.percent
  return total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc

print("System Infos")
System.os_name
System.os_version
System.architecture
System.hostname
System.username
System.is_win
System.is_linux
System.is_mac
print(f"OS: {System.os_name} {System.os_version} ({System.architecture}), Hostname: {System.hostname}, Username: {System.username}")
print(f"Is Windows: {System.is_win}, Is Linux: {System.is_linux}, Is Mac: {System.is_mac}")
print("System Monitor - Press Ctrl+C to exit")
while True:
  #os.system('cls' if os.name == 'nt' else 'clear')
  cores, usage = get_cpu_usage()
  print(f"CPU Cores: {cores}, CPU Usage: {usage}")
  total_mem_gb, total_mem_av, total_mem_pc, mem_used = get_memory_usage()
  print(f"Total Memory: {total_mem_gb} GB, Available Memory: {total_mem_av} GB, Memory Usage: {total_mem_pc}%, Used Memory: {mem_used} GB")
  total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc = get_disk_usage()
  print(f"Total Disk: {total_disk_gb} GB, Used Disk: {used_disk_gb} GB, Free Disk: {free_disk_gb} GB, Disk Usage: {disk_usage_pc}%")
  time.sleep(5)
  