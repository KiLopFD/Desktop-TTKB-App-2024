from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import origin_window
from src.ui.components.comp_header import CompHeader
from src.ui.components.comp_body import CompBody

class DipAppUi(tb.Frame):

    def __init__(self, master: tb.Window, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(expand=YES, fill=BOTH)
        # Style App
        self.my_style = tb.Style()
        self.my_style.configure('.', font=('Helvetica', 12))
        # Set UI
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create Header:
        self.ctn_header = tb.Frame(self, bootstyle='dark', height=50, padding=5)
        self.ctn_header.pack(side=TOP, fill=X)
        CompHeader(self.ctn_header, self)
        tb.Separator(self.ctn_header, orient=HORIZONTAL).pack(fill=X)
        # Create Body:
        self.ctn_body = tb.Frame(self, style='primary.TFrame')
        self.ctn_body.pack(expand=YES, fill=BOTH)
        CompBody(self.ctn_body)
        tb.Separator(self.ctn_body, orient=HORIZONTAL).pack(fill=X)
        # Create Footer:
        self.ctn_footer = tb.Frame(self, bootstyle='dark', height=50)
        self.ctn_footer.pack(side=BOTTOM, fill=X)



def run_app():
    DipAppUi(origin_window)
    origin_window.mainloop()