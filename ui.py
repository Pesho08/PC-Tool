import customtkinter as ctk
import tkinter as tk
from main import get_cpu_usage, get_memory_usage, get_disk_usage
from xulbux import System
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("pesho.systemmonitor")

# Matplotlib dark style
matplotlib.rcParams.update({
    "axes.facecolor":   "#2b2b2b",
    "figure.facecolor": "#2b2b2b",
    "axes.edgecolor":   "#555555",
    "axes.labelcolor":  "#cccccc",
    "xtick.color":      "#cccccc",
    "ytick.color":      "#cccccc",
    "grid.color":       "#444444",
    "lines.linewidth":  2,
})

# App config
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 10)

COLOR_BG      = "#1e1e1e"
COLOR_FRAME   = "#2b2b2b"
COLOR_ACCENT  = "#4fc3f7"
COLOR_TEXT    = "#e0e0e0"
COLOR_SUBTEXT = "#888888"

# Root window
root = ctk.CTk()
root.title("Pesho's System Monitor")
root.geometry("1300x750")
root.configure(fg_color=COLOR_BG)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(1, weight=1)

# Set app icon
root.iconbitmap("icon/tool-icon.ico")

# Header
header = ctk.CTkFrame(root, fg_color=COLOR_FRAME, corner_radius=0, height=55)
header.grid(row=0, column=0, columnspan=2, sticky="ew")
header.grid_propagate(False)
ctk.CTkLabel(header, text="Pesho's System Monitor",
             font=FONT_TITLE, text_color=COLOR_ACCENT,
             ).pack(side="left", padx=20, pady=10)
ctk.CTkLabel(header, text=f"Python {System.python_version}  |  {System.architecture}",
             font=FONT_SMALL, text_color=COLOR_SUBTEXT,
             ).pack(side="right", padx=20)

# Left panel
frame_left = ctk.CTkFrame(root, fg_color=COLOR_FRAME, corner_radius=12)
frame_left.grid(row=1, column=0, padx=(12, 6), pady=12, sticky="nsew")
frame_left.columnconfigure(0, weight=1)

ctk.CTkLabel(frame_left, text="System Info",
             font=FONT_HEADER, text_color=COLOR_ACCENT
             ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")
ctk.CTkFrame(frame_left, height=1, fg_color="#444444"
             ).grid(row=1, column=0, padx=16, sticky="ew")

info_items = [
    ("Hostname", System.hostname),
    ("User",     System.username),
    ("OS",       System.os_name),
    ("Version",  System.os_version),
    ("Platform", System.os_name),
]

for i, (key, val) in enumerate(info_items):
    row = i * 2 + 2
    ctk.CTkLabel(frame_left, text=key.upper(),
                 font=("Segoe UI", 9, "bold"), text_color=COLOR_SUBTEXT
                 ).grid(row=row, column=0, padx=16, pady=(10, 0), sticky="w")
    ctk.CTkLabel(frame_left, text=val,
                 font=FONT_BODY, text_color=COLOR_TEXT
                 ).grid(row=row + 1, column=0, padx=16, pady=(0, 4), sticky="w")

# Right panel
frame_right = ctk.CTkFrame(root, fg_color=COLOR_FRAME, corner_radius=12)
frame_right.grid(row=1, column=1, padx=(6, 12), pady=12, sticky="nsew")
frame_right.columnconfigure(0, weight=1)
frame_right.rowconfigure(0, weight=1)
frame_right.rowconfigure(1, weight=1)
frame_right.rowconfigure(2, weight=1)

def make_stat_frame(parent, row, title, color):
    f = ctk.CTkFrame(parent, fg_color="#333333", corner_radius=10)
    f.grid(row=row, column=0, padx=12, pady=6, sticky="nsew")
    f.columnconfigure(0, weight=1)
    f.rowconfigure(2, weight=1)
    ctk.CTkLabel(f, text=title, font=FONT_HEADER, text_color=color
                 ).grid(row=0, column=0, padx=12, pady=(10, 2), sticky="w")
    lbl = ctk.CTkLabel(f, text="Loading...", font=FONT_BODY, text_color=COLOR_TEXT)
    lbl.grid(row=1, column=0, padx=12, pady=(0, 4), sticky="w")
    return f, lbl

def make_canvas(frame, fig):
    c = FigureCanvasTkAgg(fig, master=frame)
    c.get_tk_widget().grid(row=2, column=0, padx=8, pady=(0, 10), sticky="nsew")
    return c

# CPU
frame_cpu, label_cpu = make_stat_frame(frame_right, 0, "CPU", COLOR_ACCENT)
fig_cpu = Figure(figsize=(5, 1.8), tight_layout=True)
ax_cpu  = fig_cpu.add_subplot(111)
canvas_cpu = make_canvas(frame_cpu, fig_cpu)
cpu_history = []

def update_cpu():
    cores, usage = get_cpu_usage()
    label_cpu.configure(text=f"{cores} Cores  |  Usage: {usage}%")
    cpu_history.append(usage)
    if len(cpu_history) > 60:
        cpu_history.pop(0)
    ax_cpu.clear()
    ax_cpu.set_ylim(0, 100)
    ax_cpu.set_ylabel("%", color=COLOR_SUBTEXT, fontsize=9)
    ax_cpu.grid(True, alpha=0.3)
    ax_cpu.fill_between(range(len(cpu_history)), cpu_history, alpha=0.25, color=COLOR_ACCENT)
    ax_cpu.plot(cpu_history, color=COLOR_ACCENT)
    canvas_cpu.draw()
    root.after(1000, update_cpu)

# Memory
frame_mem, label_mem = make_stat_frame(frame_right, 1, "Memory", "#81c784")
fig_mem = Figure(figsize=(5, 1.8), tight_layout=True)
ax_mem  = fig_mem.add_subplot(111)
canvas_mem = make_canvas(frame_mem, fig_mem)
mem_history = []

def update_mem():
    total_mem_gb, total_mem_av, total_mem_pc, mem_used = get_memory_usage()
    label_mem.configure(text=f"Total: {total_mem_gb} GB  |  Used: {mem_used} GB  |  {total_mem_pc}%")
    mem_history.append(total_mem_pc)
    if len(mem_history) > 60:
        mem_history.pop(0)
    ax_mem.clear()
    ax_mem.set_ylim(0, 100)
    ax_mem.set_ylabel("%", color=COLOR_SUBTEXT, fontsize=9)
    ax_mem.grid(True, alpha=0.3)
    ax_mem.fill_between(range(len(mem_history)), mem_history, alpha=0.25, color="#81c784")
    ax_mem.plot(mem_history, color="#81c784")
    canvas_mem.draw()
    root.after(2000, update_mem)

# Disk
frame_disk, label_disk = make_stat_frame(frame_right, 2, "Disk", "#ffb74d")
fig_disk = Figure(figsize=(5, 1.8), tight_layout=True)
ax_disk  = fig_disk.add_subplot(111)
canvas_disk = make_canvas(frame_disk, fig_disk)
disk_history = []

def update_disk():
    total_disk_gb, used_disk_gb, free_disk_gb, disk_usage_pc = get_disk_usage()
    label_disk.configure(text=f"Total: {total_disk_gb} GB  |  Used: {used_disk_gb} GB  |  {disk_usage_pc}%")
    disk_history.append(disk_usage_pc)
    if len(disk_history) > 60:
        disk_history.pop(0)
    ax_disk.clear()
    ax_disk.set_ylim(0, 100)
    ax_disk.set_ylabel("%", color=COLOR_SUBTEXT, fontsize=9)
    ax_disk.grid(True, alpha=0.3)
    ax_disk.fill_between(range(len(disk_history)), disk_history, alpha=0.25, color="#ffb74d")
    ax_disk.plot(disk_history, color="#ffb74d")
    canvas_disk.draw()
    root.after(5000, update_disk)

# Start
update_cpu()
update_mem()
update_disk()

root.mainloop()