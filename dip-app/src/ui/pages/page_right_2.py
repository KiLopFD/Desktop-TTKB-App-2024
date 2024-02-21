from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import numpy as np
from time import sleep
from ttkbootstrap.scrolled import ScrolledFrame

'''
    Page Right 2
    - Hiển thị ảnh gốc và ảnh sau khi xử lý qua model AI
    - base_master: Self@CompBody
'''

class PageRigt2(ScrolledFrame):

    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle='dark', padding=5)
        self.master = master
        self.base_master = base_master
        self.pack(fill=BOTH, expand=True)
        # Variables
        # Extend Base Master
        self.base_master.show_img_detail = self.show_img_detail
        self.base_master.show_img_predict = self.show_img_predict
        #-------------------------------------
        self.create_widgets()

    def create_widgets(self):
        # Ảnh Gốc
        self.lbl_frame_1 = tb.LabelFrame(self, text='Ảnh Gốc', padding=10, height=300)
        self.lbl_frame_1.pack(fill=X)
        # Ảnh Biến Đổi
        self.lbl_frame_2 = tb.LabelFrame(self, text='Ảnh Model AI DIP', padding=10, height=300)
        self.lbl_frame_2.pack(fill=X)


    def show_img_detail(self, path):
        print('Show img detail')
        img = Image.open(path)
        tmp_img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(tmp_img)
        if hasattr(self, 'origin_lbl'):
            self.origin_lbl.destroy()
        self.origin_lbl = tb.Label(self.lbl_frame_1, image=photo)
        self.origin_lbl .image = photo
        self.origin_lbl .pack()
        self.base_master.selected_path_img = path

    def show_img_predict(self, img):
        print('Show img predict')
        tmp_img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(tmp_img)
        if hasattr(self, 'predict_lbl'):
            self.predict_lbl.destroy()
        self.predict_lbl = tb.Label(self.lbl_frame_2, image=photo)
        self.predict_lbl.image = photo
        self.predict_lbl.pack()
