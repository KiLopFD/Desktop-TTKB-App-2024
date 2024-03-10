import ttkbootstrap as tb
from app.components.main import CompHeader, CompBody, CompFooter
from app.db.main import Account
from typing import List, Optional



class MainUI(tb.Frame):
    def __init__(self, master: tb.Toplevel, user_account: Account, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.user_account: Account = user_account
        self.pack(expand=True, fill=tb.BOTH)
        #-----------------------------------------------------------------------
        # Variables
        self.theme_app = self.master.style # Style
        #-----------------------------------------------------------------------
        self.create_widgets()
        # Overide Style
        self.overide_style()
        

    def create_widgets(self):
        # Header Component
        CompHeader(self)
        tb.Separator(self, orient="horizontal").pack(fill="x")
        # Body Component
        CompBody(self)
        tb.Separator(self, orient="horizontal").pack(fill="x")
        # Footer Component
        CompFooter(self)

    def overide_style(self):
        self.config(bootstyle="dark")
