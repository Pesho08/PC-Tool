import customtkinter as ctk
from xulbux import System as xx
from main import get_cpu_usage, get_memory_usage, get_disk_usage
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

# App Configurations
app = ctk.CTk()
app.geometry("400x300")
app.title("Pesho's Tool App")

# Grid configuration
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.rowconfigure(0, weight=1)



# App fonts
# TODO: Add custom fonts


# System Information
windows_info = [
  xx.hostname,
  xx.username,
  xx.os_name,
  xx.os_version
]

# System Information Frame
system_frame = ctk.CTkFrame(app)
system_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# System Stats Frame
stats_frame = ctk.CTkFrame(app)
stats_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# stats_frame configuration
stats_frame.rowconfigure(0, weight=1)
stats_frame.rowconfigure(1, weight=1)
stats_frame.rowconfigure(2, weight=1)
stats_frame.columnconfigure(0, weight=1)

# Display System Information
for info in windows_info:
  label = ctk.CTkLabel(system_frame, text=info)
  label.pack(pady=5)
  # TODO: make it look better with each having his own header

# CPU System Stats
cpu_frame = ctk.CTkFrame(stats_frame)
cpu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
cpu_label = ctk.CTkLabel(cpu_frame, text="")
cpu_label.pack(pady=5)

# CPU Usage Graph
fig_cpu = Figure(figsize=(4, 2), tight_layout=True)
ax_cpu = fig_cpu.add_subplot(111)
canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=cpu_frame)
canvas_cpu.get_tk_widget().pack(fill="both", expand=True)
cpu_history = []

def update_cpu_stats():
  cpu_cores, cpu_usage = get_cpu_usage()
  cpu_label.configure(text=f"CPU Cores: {cpu_cores}, CPU Usage: {cpu_usage}%")
  cpu_history.append(cpu_usage)
  if len(cpu_history) > 60:
    cpu_history.pop(0)
  ax_cpu.clear()
  ax_cpu.plot(cpu_history)
  canvas_cpu.draw()
  app.after(1000, update_cpu_stats)
update_cpu_stats()


# Memory System Stats
memory_frame = ctk.CTkFrame(stats_frame)
memory_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
mem_label = ctk.CTkLabel(memory_frame, text="")
mem_label.pack(pady=5)

# Memory Usage Graph
fig_mem = Figure(figsize=(4, 2), tight_layout=True)
ax_mem = fig_mem.add_subplot(111)
canvas_mem = FigureCanvasTkAgg(fig_mem, master=memory_frame)
canvas_mem.get_tk_widget().pack(fill="both", expand=True)
mem_history = []

def update_memory_stats():
  total_mem_gb, total_mem_av, total_mem_pc, mem_used = get_memory_usage()
  mem_label.configure(text=f"Total Memory: {total_mem_gb} GB, Available memory: {total_mem_av} GB, Memory Usage: {total_mem_pc}%, Used Memory: {mem_used} GB")
  mem_history.append(total_mem_pc)
  if len(mem_history) > 60:
    mem_history.pop(0)
  ax_mem.clear()
  ax_mem.plot(mem_history)
  canvas_mem.draw()
  app.after(1000, update_memory_stats)
update_memory_stats()


# Disk System Stats
disk_frame = ctk.CTkFrame(stats_frame)
disk_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
disk_label = ctk.CTkLabel(disk_frame, text="")
disk_label.pack(pady=5)

# Disk Usage Graph
fig_disk = Figure(figsize=(4, 2), tight_layout=True)
ax_disk = fig_disk.add_subplot(111)
canvas_disk = FigureCanvasTkAgg(fig_disk, master=disk_frame)
canvas_disk.get_tk_widget().pack(fill="both", expand=True)
disk_history = []

def update_disk_stats():
  total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc = get_disk_usage()
  disk_label.configure(text=f"Total Disk: {total_disk_gb} GB, Used Disk: {used_disk_gb} GB, Free Disk: {free_disk_gb} GB, Disk Usage: {disk_usage_pc}%")
  disk_history.append(disk_usage_pc)
  if len(disk_history) > 60:
    disk_history.pop(0)
  ax_disk.clear()
  ax_disk.plot(disk_history)
  canvas_disk.draw()
  app.after(1000, update_disk_stats)
update_disk_stats()
app.mainloop()
