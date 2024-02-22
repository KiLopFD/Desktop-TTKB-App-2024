import ttkbootstrap as tb
from app.layouts.auth_ui import AuthUI
from app.configs.info_window import *

# Run main window   
def main_ui():
    master_window = tb.Window(**AUTH_UI_WINDOW)
    # Create main window
    AuthUI(master_window)
    master_window.mainloop()