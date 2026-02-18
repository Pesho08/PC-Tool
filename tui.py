from textual.app import App
from textual.widgets import Header, Footer, Static, Label
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
        yield Label("Right")
    
# Start the TUI application
if __name__ == "__main__":
  app = tuiApp()
  app.run()
  