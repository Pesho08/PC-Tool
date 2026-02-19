import psutil
import time
from xulbux import System
import wmi


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

def get_used_processes():
  processes = [p for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])
               if p.info['name'] != "System Idle Process"]
  processes = sorted(processes, key=lambda process: process.info['cpu_percent'],reverse=True)
  return processes[:5]

def get_internet_speed():
  messung1 = psutil.net_io_counters()
  time.sleep(0.5)
  messung2 = psutil.net_io_counters()
  difference_download_speed = messung2.bytes_recv - messung1.bytes_recv
  difference_download_speed = round((difference_download_speed / 1024**2), 4)
  differnce_upload_speed = messung2.bytes_sent - messung1.bytes_sent
  differnce_upload_speed = round((differnce_upload_speed / 1024**2), 4)
  return difference_download_speed, differnce_upload_speed
  
if __name__ == "__main__":
  print("System Monitor - Press Ctrl+C to exit")
  while True:
    cores, usage = get_cpu_usage()
    print(f"CPU Cores: {cores}, CPU Usage: {usage}")
    total_mem_gb, total_mem_av, total_mem_pc, mem_used = get_memory_usage()
    print(f"Total Memory: {total_mem_gb} GB, Available Memory: {total_mem_av} GB, Memory Usage: {total_mem_pc}%, Used Memory: {mem_used} GB")
    total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc = get_disk_usage()
    print(f"Total Disk: {total_disk_gb} GB, Used Disk: {used_disk_gb} GB, Free Disk: {free_disk_gb} GB, Disk Usage: {disk_usage_pc}%")
    difference_download_speed, differnce_upload_speed = get_internet_speed()
    print(f"Download Speed: {difference_download_speed} MB/s, Upload Speed: {differnce_upload_speed} MB/s")
    time.sleep(5)
    