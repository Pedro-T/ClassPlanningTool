# import sys
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)

# import ttkbootstrap as ttk
# from class_planning_tool.ui.dashboard import Dashboard

# if __name__ == "__main__":
#     root = ttk.Window(themename="superhero")
#     dashboard = Dashboard(root)
#     root.mainloop()

import sys
import os
import logging


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import ttkbootstrap as ttk
from class_planning_tool.ui.dashboard import Dashboard

# Configure logging
def setup_logging():
    user_home = os.path.expanduser("~")
    log_file_path = os.path.join(user_home, "course_scheduler.log")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=log_file_path,
        filemode="w",
    )
    logging.info(f"Logging initialized. Log file at: {log_file_path}")


if __name__ == "__main__":
    setup_logging()  

    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir) 
    sys.path.insert(0, root_dir)
    root = ttk.Window(themename="superhero")
    dashboard = Dashboard(root)
    root.mainloop()

