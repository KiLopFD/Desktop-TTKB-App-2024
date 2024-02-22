import ttkbootstrap as tb
from app.components.comp_header import CompHeader



class MainUI(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, padding=50)
        self.master = master
        self.pack(expand=True, fill=tb.BOTH)
        self.create_widgets()

    def create_widgets(self):
        # Header Component
        CompHeader(self)