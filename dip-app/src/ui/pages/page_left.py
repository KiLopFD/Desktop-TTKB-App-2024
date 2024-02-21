from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import numpy as np
from time import sleep
from ttkbootstrap.scrolled import ScrolledFrame

'''
    Class Page1:
    - Biến Đổi ảnh
    - base_master: Self@CompBody
'''
class PageLeft(tb.Frame):
    def __init__(self, master=None, base_master=None, **kw):
        self.master = master
        self.base_master = base_master
        super().__init__(self.master, **kw)
        self.pack(fill=BOTH, expand=YES)
        master.add(self, text='Biến Đổi')
        self.scrollframe = ScrolledFrame(self, padding=5)
        self.scrollframe.pack(fill=BOTH, expand=YES)
        self.ctn_left = tb.LabelFrame(self.scrollframe, text='Tools Biến Đổi', bootstyle='info', padding=10)
        self.ctn_left.pack(fill=X, expand=YES)
        # Set global variable
        self.base_master.show_all_image = self.show_all_image
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


        # Create widgets
        self.create_widgets()

        # Override style
        master.config(width=500)

    def create_widgets(self):
        # Create Scroll Image
        self.lbl_frame = tb.LabelFrame(self.scrollframe, text='Ảnh', bootstyle='info', padding=10, height=300)
        self.lbl_frame.pack(fill=X, pady=5)
        self.scrollframe_imgs = ScrolledFrame(self.lbl_frame, padding=5, height=300)
        self.scrollframe_imgs.pack(fill=X)
        # Set global variable
        self.base_master.pl1_scrollframe_imgs = self.scrollframe_imgs

    def show_all_image(self, list_paths):
        cnt = 0
        for path in list_paths:
            if cnt % 3 == 0:
                self.row = tb.Frame(self.scrollframe_imgs, bootstyle='dark', padding=5)
                self.row.pack(fill=X)
            cnt += 1
            img = Image.open(path)
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            label = tb.Label(self.row, image=photo)
            label.image = photo
            label.pack(side=LEFT)
            label.bind('<Button-1>', lambda event, path=path: self.show_img_detail(path))

    def show_img_detail(self, path):
        self.base_master.path_image = path
        self.base_master.show_origin_image(path)