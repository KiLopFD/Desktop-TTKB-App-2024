from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window


class CompFooter(tb.Frame):
    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, height=50, bootstyle='dark')
        self.master = master
        self.base_master = base_master
        self.pack(fill=X, expand=YES)

        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        ...