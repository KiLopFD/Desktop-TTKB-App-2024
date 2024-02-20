import ttkbootstrap as tb
from ttkbootstrap.constants import *

class PageLog(tb.Frame):

    def __init__(self, master, base_master,**kwargs):
        super().__init__(master, **kwargs, bootstyle='dark', padding=10)
        self.master = master
        self.base_master = base_master
        self.pack(expand=True, fill=tb.BOTH)
        # Set base master
        #--------------------------------
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Login Group
        frame_log = tb.Frame(self)
        frame_log.pack(fill=X, pady=30, side=TOP)
        for field in self.base_master.log_input_fields:
            lbl_frame = tb.LabelFrame(frame_log, text=field['name'])
            lbl_frame.pack(fill=X)
            entry = tb.Entry(lbl_frame, textvariable=field['var'])
            entry.pack(fill=X, padx=5, pady=5)

        # Action Group
        frame_action = tb.Frame(self)
        frame_action.pack(fill=X, pady=10, side=TOP)
        frame_center = tb.Frame(frame_action)
        frame_center.pack()
        btn_login = tb.Button(frame_center, text='Đăng Nhập', bootstyle='secondary')
        btn_login.pack(side=LEFT, padx=5)
        btn_register = tb.Button(frame_center, text='Đăng Ký', bootstyle='primary', command=lambda: self.base_master.nb.select(1))
        btn_register.pack(side=LEFT, padx=5)

        # Footer Group
        frame_footer = tb.Frame(self)
        frame_footer.pack(fill=X, pady=10, side=BOTTOM)
        lbl_footer = tb.Label(frame_footer, text='Chào mừng bạn quay lại')
        lbl_footer.pack()


    def log_in(self):
        ...


