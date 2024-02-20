import ttkbootstrap as tb
from app.layouts.auth_ui import AuthUI
from app.configs.info_window import *
'''
title: str = "ttkbootstrap",
    themename: str = "litera",
    iconphoto: str = '',
    size: Any | None = None,
    position: Any | None = None,
    minsize: Any | None = None,
    maxsize: Any | None = None,
    resizable: Any | None = None,
    hdpi: bool = True,
    scaling: Any | None = None,
    transient: Any | None = None,
'''





def main_ui():
    master_window = tb.Window(**AUTH_UI_WINDOW)
    # Create main window
    AuthUI(master_window)
    master_window.mainloop()