import ttkbootstrap as tb
from ttkbootstrap.constants import *
from app.pages.auth_ui.page_reg import PageReg
from app.pages.auth_ui.page_log import PageLog
from app.db.dao.account_dao import AccountDao

class AuthUI(tb.Frame):

    def __init__(self, master: tb.Window, **kwargs):
        # Set master window
        super().__init__(master, **kwargs, padding=50)
        self.master = master
        self.pack(expand=True, fill=BOTH)
        # Variables
        self.log_input_fields = [
            {
                "label": "username",
                "name": "Tên Đăng Nhập",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "password",
                "name": "Mật Khẩu",
                "var": tb.StringVar(),
                "widget": None,
            },
        ]
        self.reg_input_fields = [
            {
                "label": "username",
                "name": "Tên Đăng Nhập",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "fullname",
                "name": "Họ và Tên",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "email",
                "name": "Email",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "phone",
                "name": "Số Điện Thoại",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "birthday",
                "name": "Ngày Sinh",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "password",
                "name": "Mật Khẩu",
                "var": tb.StringVar(),
                "widget": None,
            }
        ]
        # Create DAO
        self.account_dao = AccountDao()
        # Create widgets
        self.create_widgets()
    


    def create_widgets(self):
        # Create Components
        self.nb = tb.Notebook(self)
        self.nb.pack(fill=X)
        # Create tabs
        self.frame_1 = tb.Frame(self.nb)
        self.frame_2 = tb.Frame(self.nb)
        self.nb.add(self.frame_1, text='Trang Đăng Nhập')
        self.nb.add(self.frame_2, text='Trang Đăng Ký')
        # Extend frame_1
        PageLog(self.frame_1, self)
        # Extend frame_2
        PageReg(self.frame_2, self)




    def new_window(self):
        ...