from textual.app import App
from textual.widgets import Header, Footer, Static
from xulbux import System as xx
from main import get_cpu_usage, get_memory_usage, get_disk_usage

class tuiApp(App):
  def compose(self):
    yield Header()
    yield Static("Hello, World!")
    yield Footer()
    
if __name__ == "__main__":
  app = tuiApp()
  app.run()