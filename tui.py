from textual.app import App
from textual.widgets import Header, Footer, Static, Label, ProgressBar
from textual.containers import Horizontal, Vertical
from xulbux import System as xx
from main import get_cpu_usage, get_memory_usage, get_disk_usage

class tuiApp(App):
  # CSS for the TUI layout
  CSS = """
  #left-panel {
    width: 30%;
    border: round white;
    }
  #right-panel {
    width: 70%;
    border: round red;
    }
    """
  TITLE = "Pesho's Tool App"
  
  def compose(self):
    yield Header(show_clock=True)
    yield Label("System Monitor - Press Ctrl+P to exit or use ICON in the top left corner")
    with Horizontal():
      
      # Left Panel for System Information
      with Vertical(id="left-panel"):
        yield Label("System Information", id="header")
        system_info = [
          f"Hostname: {xx.hostname}",
          f"Username: {xx.username}",
          f"OS Name: {xx.os_name}",
          f"OS Version: {xx.os_version}"
        ]
        system_info_label = Label("\n".join(system_info))
        yield system_info_label

      # Right Panel for System Stats
      with Vertical(id="right-panel"):  
        self.cpu_label = Label("")
        self.memory_label = Label("")
        self.disk_label = Label("")
        yield self.cpu_label
        yield ProgressBar(total=100, id="cpu_progress", show_eta=False)
        yield self.memory_label
        yield self.disk_label
  def on_mount(self):
    self.set_interval(1, self.update_stats)
    
  def update_stats(self):
    cpu_cores, cpu_usage = get_cpu_usage()
    mem_total, mem_avail, mem_percent, mem_used = get_memory_usage()
    disk_total, disk_used, disk_free, disk_percent = get_disk_usage()
    
    self.cpu_label.update(f"CPU Cores: {cpu_cores}, CPU Usage: {cpu_usage}%")
    self.query_one("#cpu_progress", ProgressBar).update(progress=cpu_usage)
    self.memory_label.update(f"Memory: {mem_used} GB / {mem_total} GB ({mem_percent}%)")
    self.disk_label.update(f"Disk: {disk_used} GB / {disk_total} GB ({disk_percent}%)")
      
# Start the TUI application
if __name__ == "__main__":
  app = tuiApp()
  app.run()
  