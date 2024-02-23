import ttkbootstrap as tb


class CompFooter(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bootstyle="info", height=50)
        self.master = master
        self.pack(fill="x", side="top")
        self.create_widgets()

    def create_widgets(self):
        ...