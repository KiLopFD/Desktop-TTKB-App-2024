from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window


class CompHeader(tb.Frame):

    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.base_master = base_master
        self.pack(fill=X)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create Frame Left:
        self.frame_left = tb.Frame(self, height=50, bootstyle='dark', width=200,padding=5)
        self.frame_left.pack(side=LEFT, fill=Y)
        
        #-------------------------------------
        # Create Frame Right:
        self.frame_right = tb.Frame(self, bootstyle='dark', height=50, width=200, padding=5)
        self.frame_right.pack(side=RIGHT, fill=Y)
        self.configure(style='primary.TFrame')
        # Create Menu Theme:
        self.menu_theme()
        #-------------------------------------
        # Create Frame Center:
        self.frame_center = tb.Frame(self, height=50, bootstyle='dark', padding=5)
        self.frame_center.pack(expand=YES, fill=BOTH, padx=5)
        self.implementation_center()
        # Override style
        self.configure(style='primary.TFrame', padding=5)


    def menu_theme(self):
        self.theme_menubutton = tb.Menubutton(self.frame_right, text='Giao diện')
        self.theme_menubutton.pack(side=RIGHT)
        self.theme_menu = tb.Menu(self.theme_menubutton, tearoff=0)

        for theme in BASE_THEME:
            self.theme_menu.add_command(label=theme, command=lambda theme=theme: self.change_theme(theme))
        
        self.theme_menubutton.config(menu=self.theme_menu)

    def change_theme(self, theme):
        origin_window.style.theme_use(theme)

    def implementation_center(self):
        self.label_name_app = tb.Label(self.frame_center, text='Alex Dev No CopyRight', font=('Helvetica', 15))
        self.label_name_app.pack()

        