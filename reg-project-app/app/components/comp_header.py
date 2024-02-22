import ttkbootstrap as tb


class CompHeader(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, padding=10)
        self.master = master
        self.pack(fill=tb.X, side=tb.TOP)
        self.create_widgets()

    def create_widgets(self):
        ...