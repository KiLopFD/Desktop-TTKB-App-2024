from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import numpy as np
from time import sleep
from ttkbootstrap.scrolled import ScrolledFrame
from src.models.engine_ai import EngineAI, CONST_MODEL, DATASET


class PageLeft2(ScrolledFrame):

    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle='info')
        self.master = master
        self.base_master = base_master
        self.pack(fill=BOTH, expand=True)
        # Variables
        self.list_img: list[Image.Image] = []
        self.base_master.path_selected_img_train = []
        #-------------------------------------
        self.create_widgets()

    def create_widgets(self):
        self.ctn_base = tb.Frame(self, bootstyle='dark', padding=10)
        self.ctn_base.pack(fill=X)
        self.lbl_frame_1 = tb.LabelFrame(self.ctn_base, text='Danh sách ảnh', padding=10)
        self.lbl_frame_1.pack(fill=X)
        self.scrollframe_imgs = ScrolledFrame(self.lbl_frame_1, padding=5, height=300)
        self.scrollframe_imgs.pack(fill=X)
        # Chọn Model vs Dataset
        self.lbl_frame_2 = tb.LabelFrame(self.ctn_base, text='Chọn Model vs Dataset', padding=5, height=100)
        self.lbl_frame_2.pack(fill=X)
        # Chọn Model
        self.scrollframe_models = ScrolledFrame(self.lbl_frame_2, padding=5, height=100)
        self.scrollframe_models.pack(side=LEFT, fill=X)
        self.first_row = tb.Frame(self.scrollframe_models, bootstyle='dark', padding=10)
        self.first_row.pack(fill=X)
        label = tb.Label(self.first_row, text='Chọn Model', bootstyle='info')
        label.pack(side=LEFT)
        self.btn_load_model = tb.Button(self.first_row, text='Thêm Model', bootstyle='info', command=self.add_model)
        self.btn_load_model.pack(side=RIGHT)
        cnt_row = 0
        for model in CONST_MODEL:
            if cnt_row % 2 == 0:
                self.row = tb.Frame(self.scrollframe_models, bootstyle='dark', padding=5)
                self.row.pack(fill=X)
            cnt_row += 1
            radiobutton = tb.Radiobutton(self.row, text=model, value=model, bootstyle='info')
            radiobutton.pack(side=LEFT, padx=5)
            self.base_master.set_model = self.set_model
            radiobutton.bind('<Button-1>', lambda event, model=model: self.base_master.set_model(model))
        # Chọn Dataset
        self.scrollframe_dataset = ScrolledFrame(self.lbl_frame_2, padding=5, height=100)
        self.scrollframe_dataset.pack(side=RIGHT, fill=X)
        
        # Action Group
        self.lbl_frame_btn_group = tb.LabelFrame(self.ctn_base, text='Action', padding=10)
        self.lbl_frame_btn_group.pack(fill=X)
        self.btn_open = tb.Button(self.lbl_frame_btn_group, text='Open', bootstyle='info', command=self.open_img)
        self.btn_open.pack(side=LEFT, padx=5)
        self.btn_predict = tb.Button(self.lbl_frame_btn_group, text='Predict', bootstyle='info', command=self.predict_img)
        self.btn_predict.pack(side=LEFT, padx=5)
        self.btn_train = tb.Button(self.lbl_frame_btn_group, text='Train', bootstyle='info', command=self.train_img)
        self.btn_train.pack(side=LEFT, padx=5)
        self.btn_save = tb.Button(self.lbl_frame_btn_group, text='Save', bootstyle='info', command=self.save_img)
        self.btn_save.pack(side=LEFT, padx=5)

    
    def open_img(self):
        file_path = askopenfilenames(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        self.base_master.path_selected_img_train = file_path
        self.show_img()

    def show_img(self):
        cnt = 0
        for path in self.base_master.path_selected_img_train:
            if cnt % 3 == 0:
                self.ctn_frame = tb.Frame(self.scrollframe_imgs, bootstyle='dark', padding=5)
                self.ctn_frame.pack(fill=X)
            img = Image.open(path)
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            self.list_img.append(photo)
            lbl = tb.Label(self.ctn_frame, image=photo)
            lbl.image = photo
            lbl.pack(side=LEFT)
            lbl.bind('<Button-1>', lambda event, path=path: self.show_img_detail(path))
            cnt += 1

    def show_img_detail(self, path):
        self.base_master.show_img_detail(path)


    def set_model(self, model):
        print(model)
        self.engine_model = EngineAI()
        self.engine_model.load_model(model)
        self.base_master.engine_model = self.engine_model
    
    def predict_img(self):
        results = self.engine_model.predict(self.base_master.selected_path_img)
        # Show results
        im_array = results[0].plot()
        pil_img = Image.fromarray(im_array[..., ::-1])
        self.base_master.dip_res_img = pil_img
        self.base_master.show_img_predict(pil_img)
            
    def train_img(self):
        self.engine_model.train()

    def save_img(self):
        print('Save img')
        file_path = askdirectory()
        self.base_master.dip_res_img.save(file_path+'/dip_res_img.png')

    def add_model(self):
        print('Add model')
        file_path = askopenfilename(filetypes=[('Model Files', '*.pt')])
        print(file_path)
        name_model = file_path.split('/')[-1]
        self.engine_model = EngineAI()
        self.engine_model.load_model(file_path)
        self.base_master.engine_model = self.engine_model
        row = tb.Frame(self.scrollframe_models, bootstyle='dark', padding=5)
        row.pack(fill=X)
        radiobutton = tb.Radiobutton(row, text=name_model, value=name_model, bootstyle='info')
        radiobutton.pack(side=LEFT, padx=5)
        radiobutton.bind('<Button-1>', lambda event, file_path=file_path: self.base_master.engine_model.load_model(file_path))
        
        