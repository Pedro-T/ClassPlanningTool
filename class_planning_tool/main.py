import ttkbootstrap as ttk
from ui.dashboard import Dashboard

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    dashboard = Dashboard(root)
    root.mainloop()