import ttkbootstrap as tb


class CompHeader(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pack(fill="x", side="top")
        # Variables

        #-----------------------------------------------------------------------
        # Widgets
        self.create_widgets()
        # Overide Style
        self.overide_style()

    def create_widgets(self):
        # Frame Right
        self.create_frame_right()
        # Frame Left
        self.create_frame_left()
        # Frame Center
        self.create_frame_center()
        


    def overide_style(self):
        print("Overide Style")
        self.config(padding=10, bootstyle="dark", height=50)

    def create_frame_right(self):
        frame_right = tb.Frame(self, padding=5, bootstyle="dark")
        frame_right.pack(fill="y", side="right")
        # Menu Avatar
        menu_avatar = tb.Menu(frame_right, tearoff=0)
        menu_avatar.add_command(label="Profile")
        menu_avatar.add_command(label="Logout")
        menu_avatar.add_separator()
        menu_avatar.add_command(label="Exit")
        # Dropdown Avatar
        self.menubtn_avatar = tb.Menubutton(frame_right, text=self.master.user_account.username, bootstyle="primary", menu=menu_avatar)
        self.menubtn_avatar.pack(side="right")
        # Menu Theme
        menu_theme = tb.Menu(frame_right, tearoff=0)
        for theme in self.master.theme_app.theme_names():
            menu_theme.add_command(label=theme, command=lambda theme=theme: self.master.theme_app.theme_use(theme))
        # Dropdown Theme
        self.menubtn_theme = tb.Menubutton(frame_right, text="Theme", bootstyle="primary", menu=menu_theme)
        self.menubtn_theme.pack(side="right", padx=5)
        


    


    
    def create_frame_left(self):
        ...

    def create_frame_center(self):
        ...

