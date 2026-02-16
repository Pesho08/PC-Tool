import customtkinter as ctk
from main import get_cpu_usage, get_memory_usage, get_disk_usage
from xulbux import System

root = ctk.CTk()
root.title("Pesho's System Monitor")
root.geometry("1200x700")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(0, weight=1)


frame_left = ctk.CTkFrame(root)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
label_hostname = ctk.CTkLabel(frame_left, text=f"Hostname: {System.hostname}")
label_username = ctk.CTkLabel(frame_left, text=f"User: {System.username}")
label_os_name = ctk.CTkLabel(frame_left, text=f"OS: {System.os_name} Version: {System.os_version}")
label_hostname.grid(row=0, column=0, padx=10, pady=5, sticky="w")
label_username.grid(row=1, column=0, padx=10, pady=5, sticky="w")
label_os_name.grid(row=2, column=0, padx=10, pady=5, sticky="w")


frame_right = ctk.CTkFrame(root)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
label_stats = ctk.CTkLabel(frame_right, text="")
def upadte():
  cores, usage = get_cpu_usage()
  total_mem_gb, total_mem_av, total_mem_pc, mem_used = get_memory_usage()
  total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc = get_disk_usage()
  label_stats.configure(text= f"CPU Cores: {cores}, CPU Usage: {usage}\nTotal Memory: {total_mem_gb} GB, Available Memory: {total_mem_av} GB, Memory Usage: {total_mem_pc}%, Used Memory: {mem_used} GB\nTotal Disk: {total_disk_gb} GB, Used Disk: {used_disk_gb} GB, Free Disk: {free_disk_gb} GB, Disk Usage: {disk_usage_pc}%")
  root.after(1000, upadte)
upadte()
label_stats.grid(padx=10, pady=5)


root.mainloop()