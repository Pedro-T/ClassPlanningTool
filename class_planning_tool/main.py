import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import ttkbootstrap as ttk
from class_planning_tool.ui.dashboard import Dashboard

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    dashboard = Dashboard(root)
    root.mainloop()
