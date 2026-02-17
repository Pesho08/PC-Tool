import customtkinter as ctk
from xulbux import System as xx

# App Configurations
app = ctk.CTk()
app.geometry("400x300")
app.title("Pesho's Tool App")

# System Information
windows_info = [
  xx.hostname,
  xx.username,
  xx.os_name,
  xx.os_version
]

for info in windows_info:
    label = ctk.CTkLabel(app, text=info)
    label.pack(pady=1)

app.mainloop()
