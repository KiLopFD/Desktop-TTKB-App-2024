from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import numpy as np
from time import sleep

'''
    Class Page1:
    - Biến Đổi ảnh
'''
class PageLeft(tb.Frame):
    def __init__(self, master=None, base_master=None, **kw):
        self.master = master
        self.base_master = base_master
        super().__init__(self.master, **kw)
        self.pack(fill=BOTH, expand=True)
        master.add(self, text='Biến Đổi')
        self.ctn_left = tb.LabelFrame(self, text='Tools Biến Đổi', bootstyle='info', padding=10)
        self.ctn_left.pack(fill=X)
        
        # Create widgets filter
        for attr in self.base_master.attr_input:
            self.lbl_frame = tb.LabelFrame(self.ctn_left, text=attr['name'], bootstyle='info', padding=5)
            self.lbl_frame.pack(fill=X)
            attr['textvar_check'] = tb.IntVar()
            attr['check_var'] = tb.Checkbutton(self.lbl_frame, text='Chọn', bootstyle='info', onvalue=1, offvalue=0, variable=attr['textvar_check'])
            attr['check_var'].pack(side=LEFT)
            for category in attr['category']:
                self.row = tb.Frame(self.lbl_frame, bootstyle='dark', padding=5)
                self.row.pack(fill=X, side=RIGHT)
                self.lbl = tb.Label(self.row, text=category['name'], bootstyle='info')
                self.lbl.pack(side=LEFT)
                category['name_var'] = tb.Scale(self.row, from_=0, to=100, orient=HORIZONTAL, bootstyle='info')
                category['name_var'].pack(side=RIGHT, fill=X)

        # Create Action Group
        self.lbl_frame_btn_group = tb.LabelFrame(self.ctn_left, text='Action', bootstyle='info', padding=10)
        self.lbl_frame_btn_group.pack(fill=X)
        for action in self.base_master.acction_input:
            action['name_var'] = tb.Button(self.lbl_frame_btn_group, text=action['name'], bootstyle='info')
            action['name_var'].pack(side=LEFT, padx=5)