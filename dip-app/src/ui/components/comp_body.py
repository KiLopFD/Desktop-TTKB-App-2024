from src.ui.export_module import tb
from ttkbootstrap.constants import *
from src.ui.config.window import BASE_THEME, origin_window
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import numpy as np
from time import sleep
from src.ui.pages.page_left import PageLeft
from scipy.ndimage import convolve
import cv2
import os
from src.ui.pages.page_right_2 import PageRigt2
from src.ui.pages.page_left_2 import PageLeft2
from ttkbootstrap.scrolled import ScrolledFrame

class CompBody(tb.Frame):

    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle='warning')
        self.master = master
        self.base_master = base_master
        self.pack(expand=YES, fill=BOTH)
        # Image Size:
        self.image_size = (200, 200)
        # Set UI
        self.attr_input = [
            {
                "label": "logarit_base",
                "name": "Biến Đổi Logarit",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "constant_c",
                        "name": "Hệ Số C",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "piecewise_linear",
                "name": "Biến Đổi Đa Diểm",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "point_low",
                        "name": "Điểm Thấp",
                        "name_var": tb.Scale,
                    },
                    {
                        "label": "point_high",
                        "name": "Điểm Cao",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "gamma",
                "name": "Biến Đổi Gamma",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "gamma",
                        "name": "Gamma",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "average_filter",
                "name": "Lọc Trung Bình",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Kích Thước Lọc",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "median_filter",
                "name": "Lọc Trung Vị",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Kích Thước Lọc",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "gaussian_filter",
                "name": "Lọc Gaussian",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Kích Thước Lọc",
                        "name_var": tb.Scale,
                    },
                    {
                        "label": "filter_sigma",
                        "name": "Hệ Số Sigma",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "filter_histogram",
                "name": "Cân Bằng Histogram",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Giá Trị",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "filter_laplacian",
                "name": "Lọc Laplacian",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Giá Trị",
                        "name_var": tb.Scale,
                    }
                ]
            },
            {
                "label": "filter_sobel",
                "name": "Lọc Sobel",
                "check_var": tb.Checkbutton,
                "category": [
                    {
                        "label": "filter_size",
                        "name": "Giá Trị",
                        "name_var": tb.Scale,
                    }
                ]
            }
        ]
        self.acction_input = [
            {
                "label": "pick_image",
                "name": "Chọn Ảnh",
                "name_var": tb.Button,
            },
            {
                "label": "apply",
                "name": "Áp Dụng",
                "name_var": tb.Button,
            },
            {
                "label": "save",
                "name": "Lưu Ảnh",
                "name_var": tb.Button,
            },
            {
                "label": "reset",
                "name": "Reset",
                "name_var": tb.Button,
            }
        ]
        # -------------------------------------
        # Create widgets
        self.create_widgets()
        # Add Action
        self.acction_input[0]['name_var'].configure(command=self.open_image)
        self.acction_input[1]['name_var'].configure(command=self.apply_all_filter)
        self.acction_input[2]['name_var'].configure(command=self.save_image)
        self.acction_input[3]['name_var'].configure(command=self.reset_image)

        # Add Event Change Scale
        self.attr_input[0]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_logarithm_transform)
        self.attr_input[1]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_piecewise_transform)
        self.attr_input[1]['category'][1]['name_var'].bind("<ButtonRelease-1>", self.apply_piecewise_transform)
        self.attr_input[2]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_gamma_transform)
        self.attr_input[3]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_average_filter)
        self.attr_input[4]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_median_filter)
        self.attr_input[5]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_gaussian_filter)
        self.attr_input[5]['category'][1]['name_var'].bind("<ButtonRelease-1>", self.apply_gaussian_filter)
        self.attr_input[6]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_histogram_filter)
        self.attr_input[7]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_laplacian_filter)
        self.attr_input[8]['category'][0]['name_var'].bind("<ButtonRelease-1>", self.apply_sobel_filter)

    def create_widgets(self):
        # Create Frame Left:
        self.frame_left = tb.Frame(self, bootstyle='dark', width=400, padding=10)
        self.frame_left.pack(side=LEFT, fill=Y)
        self.implementation_frame_left()
        # Create Frame Right:
        self.frame_right = tb.Frame(self, bootstyle='dark', width=1000, padding=10)
        self.frame_right.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.implementation_frame_right()
        # Override style
        self.configure(style='primary.TFrame', padding=5)

    def implementation_frame_left(self):
        self.nb_left = tb.Notebook(self.frame_left, bootstyle='dark')
        self.nb_left.pack(fill=BOTH, expand=YES)
        # Pages:
        PageLeft(self.nb_left, self)
        self.page_left_2 = tb.Frame(self.nb_left, bootstyle='dark')
        self.nb_left.add(self.page_left_2, text='Traininig Data')
        PageLeft2(self.page_left_2, self)
        # -------------------------------------
        

    def implementation_frame_right(self):

        self.nb_right = tb.Notebook(self.frame_right, bootstyle='dark')
        self.nb_right.pack(fill=BOTH, expand=YES)
        # Pages:
        self.page_right_1 = tb.Frame(self.nb_right, bootstyle='dark',padding=5)
        self.nb_right.add(self.page_right_1, text='Biến Đổi Ảnh')
        # Page 2
        self.page_right_2 = tb.Frame(self.nb_right, bootstyle='dark')
        self.nb_right.add(self.page_right_2, text='Kết Quả Traning')
        PageRigt2(self.page_right_2, self)
        # -------------------------------------
        lbl_frame_ctn_top = tb.LabelFrame(self.page_right_1, text='Ảnh Gốc', bootstyle='info', padding=10)
        lbl_frame_ctn_top.pack(fill=X, pady=5)
        self.ctn_top = ScrolledFrame(lbl_frame_ctn_top, padding=5, height=300)
        self.ctn_top.pack(fill=X, side=TOP)
        lbl_frame_ctn_bottom = tb.LabelFrame(self.page_right_1, text='Ảnh Kết Quả', bootstyle='info', padding=10)
        lbl_frame_ctn_bottom.pack(fill=X, pady=5)
        self.ctn_bottom = ScrolledFrame(lbl_frame_ctn_bottom, padding=5, height=300)
        self.ctn_bottom.pack(fill=X, side=BOTTOM)

    def open_image(self):
        all_path_images = askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")] )
        self.show_all_image(all_path_images)

    def show_origin_image(self, path_image):
        self.image = Image.open(path_image)
        self.image = self.image.resize(self.image_size)
        self.origin_photo = ImageTk.PhotoImage(self.image)
        if hasattr(self, 'lbl_origin_img'):
            self.lbl_origin_img.destroy()
        self.lbl_origin_img = tb.Label(self.ctn_top, image=self.origin_photo, bootstyle='info')
        self.lbl_origin_img.image = self.origin_photo
        self.lbl_origin_img.pack()


    def resize_image(self, image, size=(200, 200)):
        return image.resize(size)

    def show_result_image(self, image: Image.Image):
        self.image = image.resize(self.image_size)
        self.res_photo = ImageTk.PhotoImage(self.image)
        if hasattr(self, 'lbl_res_img'):
            self.lbl_res_img.destroy()
        self.lbl_res_img = tb.Label(self.ctn_bottom, image=self.res_photo, bootstyle='info')
        self.lbl_res_img.image = self.res_photo
        self.lbl_res_img.pack()

    def apply_logarithm_transform(self, *args, **kwargs):
        print(self.attr_input[0]['category'][0]['name_var'].get())
        # Lấy giá trị từ các scale
        log_base = self.attr_input[0]['category'][0]['name_var'].get()
        # Lấy giá trị từ scale hệ số c

        # Thực hiện biến đổi logarit trực tiếp trên dữ liệu pixel của ảnh
        # Chuyển đổi ảnh thành mảng numpy
        img_array = np.array(self.image)
        # Áp dụng biến đổi logarit
        transformed_array = np.log(img_array.astype(np.float32) + 1) / (np.log(log_base +1) + 1)
        # Chuẩn hóa giá trị pixel
        transformed_array = (transformed_array - np.min(transformed_array)) / (np.max(transformed_array) - np.min(transformed_array)) * 255
        # Chuyển đổi lại kiểu dữ liệu thành uint8
        transformed_array = transformed_array.astype(np.uint8)
        # Chuyển đổi mảng numpy thành ảnh PIL
        transformed_image = Image.fromarray(transformed_array)
        # Hiển thị ảnh kết quả
        self.show_result_image(transformed_image)
    
    def apply_piecewise_transform(self, *args, **kwargs):
        print(self.attr_input[1]['category'][0]['name_var'].get())
        print(self.attr_input[1]['category'][1]['name_var'].get())
        # Lấy giá trị từ các scale
        point_low = self.attr_input[1]['category'][0]['name_var'].get()
        # Lấy giá trị từ scale điểm thấp
        point_high = self.attr_input[1]['category'][1]['name_var'].get()
        # Lấy giá trị từ scale điểm cao

        # Thực hiện biến đổi đa điểm trực tiếp trên dữ liệu pixel của ảnh
        img_array = np.array(self.image)
        # Tính toán giá trị pixel mới dựa trên các điểm thấp và cao
        transformed_array = np.piecewise(img_array, [img_array <= point_low, (img_array > point_low) & (img_array <= point_high), img_array > point_high], [0, lambda x: (x - point_low) * 255 / (point_high - point_low), 255])
        # Chuyển đổi mảng numpy thành ảnh PIL
        transformed_image = Image.fromarray(transformed_array)
        # Hiển thị ảnh kết quả
        self.show_result_image(transformed_image)
    
    def apply_gamma_transform(self, *args, **kwargs):
        # Lấy giá trị gamma từ scale
        gamma_value = self.attr_input[2]['category'][0]['name_var'].get()

        # Tạo một bản sao của ảnh gốc
        transformed_image = self.image.copy()

        # Áp dụng biến đổi gamma
        gamma_corrected = ImageEnhance.Contrast(transformed_image).enhance(gamma_value)

        # Câp nhật ảnh kết quả
        self.image = gamma_corrected

        # Hiển thị ảnh kết quả
        self.show_result_image(gamma_corrected)

    def apply_average_filter(self, *args, **kwargs):
        # Lấy kích thước của bộ lọc từ scale
        filter_size = float(self.attr_input[3]['category'][0]['name_var'].get())

        # Áp dụng bộ lọc trung bình
        filtered_image = self.image.filter(ImageFilter.BoxBlur(filter_size))

        # Cập nhật ảnh kết quả
        self.image = filtered_image

        # Hiển thị ảnh kết quả
        self.show_result_image(filtered_image)



    def apply_median_filter(self, *args, **kwargs):
        # Lấy kích thước của bộ lọc từ scale
        filter_size = int(self.attr_input[4]['category'][0]['name_var'].get())

        try:
            # Áp dụng bộ lọc trung vị
            filtered_image = self.image.filter(ImageFilter.MedianFilter(filter_size))
        except:
            filtered_image = self.image

        # Cập nhật ảnh kết quả
        self.image = filtered_image
        
        # Hiển thị ảnh kết quả
        self.show_result_image(filtered_image)


    def apply_gaussian_filter(self, *args, **kwargs):
        # Lấy kích thước của bộ lọc từ scale
        filter_size = int(self.attr_input[5]['category'][0]['name_var'].get())
        # Lấy giá trị sigma từ scale
        sigma = float(self.attr_input[5]['category'][1]['name_var'].get())

        # Chuyển đổi ảnh thành mảng numpy
        img_array = np.array(self.image)

        try:
            # Áp dụng bộ lọc Gaussian
            filtered_array = cv2.GaussianBlur(img_array, (filter_size, filter_size), sigma)
        except:
            filtered_array = img_array

        # Chuyển đổi mảng numpy thành ảnh PIL
        filtered_image = Image.fromarray(filtered_array)

        # Cập nhật ảnh kết quả
        self.image = filtered_image

        # Hiển thị ảnh kết quả
        self.show_result_image(filtered_image)
    

    def apply_histogram_filter(self, *args, **kwargs):
        # Lấy giá trị từ scale
        scale = self.attr_input[6]['category'][0]['name_var'].get() / 100

        # Cân bằng histogram
        equalized_image = ImageOps.equalize(self.image.convert('L'))

        # Điều chỉnh cường độ theo scale
        equalized_image = ImageEnhance.Contrast(equalized_image).enhance(scale)

        # Hiển thị ảnh kết quả
        self.show_result_image(equalized_image.convert('RGB'))


    def apply_laplacian_filter(self, *args, **kwargs):
        # Lấy giá trị từ scale
        scale = self.attr_input[7]['category'][0]['name_var'].get() / 100

        # Áp dụng bộ lọc Laplacian
        laplacian_image = self.image.filter(ImageFilter.FIND_EDGES)
        laplacian_image = ImageEnhance.Contrast(laplacian_image).enhance(scale)

        # Cập nhật ảnh kết quả
        self.image = laplacian_image

        # Hiển thị ảnh kết quả
        self.show_result_image(laplacian_image)
    
    def apply_sobel_filter(self, *args, **kwargs):
        # Lấy giá trị từ scale
        scale = self.attr_input[8]['category'][0]['name_var'].get() / 100

        # Áp dụng bộ lọc Sobel
        sobel_image = self.image.filter(ImageFilter.FIND_EDGES)
        sobel_image = ImageEnhance.Contrast(sobel_image).enhance(scale)

        # Cập nhật ảnh kết quả
        self.image = sobel_image

        # Hiển thị ảnh kết quả
        self.show_result_image(sobel_image)
        
    # -------------------------------------

    
    def reset_image(self):
        self.image = Image.open(self.path_image)
        self.show_result_image(self.image)
        for attr in self.attr_input:
            for category in attr['category']:
                category['name_var'].set(0)

    def apply_all_filter(self):
        self.image = Image.open(self.path_image)
        for attr in self.attr_input:
            print(attr['textvar_check'].get())
            if attr['textvar_check'].get() == 1:
                if attr['label'] == 'logarit_base' and 0 not in [category['name_var'].get() for category in attr['category']]:
                    self.apply_logarithm_transform()
                elif attr['label'] == 'piecewise_linear' and [category['name_var'].get() for category in attr['category']].count(0) > 1:
                    self.apply_piecewise_transform()
                elif attr['label'] == 'gamma' and 0 not in [category['name_var'].get() for category in attr['category']]:
                    self.apply_gamma_transform()
                elif attr['label'] == 'average_filter' and 0 not in [category['name_var'].get() for category in attr['category']]:
                    self.apply_average_filter()
                elif attr['label'] == 'median_filter' and 0 not in [category['name_var'].get() for category in attr['category']]:
                    self.apply_median_filter()
                elif attr['label'] == 'gaussian_filter' and [category['name_var'].get() for category in attr['category']].count(0) > 1:
                    self.apply_gaussian_filter()
                elif attr['label'] == 'filter_histogram' and 0 not in [category['name_var'].get() for category in attr['category']]:
                    self.apply_histogram_filter()


    def save_image(self):
        dir_save = askdirectory()
        self.image = self.image.resize(self.image_size)
        if 'result' in os.listdir(dir_save):
            self.image.save(f"{dir_save}/result_{len(os.listdir(dir_save))}.png")
        else:
            os.mkdir(f"{dir_save}/result")
            self.image.save(f"{dir_save}/result_{len(os.listdir(dir_save))}.png")
        print('Save Image')

    def adjust_size_image(self, height, width):
        self.image_size = (height, width)
        self.image = Image.open(self.path_image)
        # self.show_origin_image(self.path_image)
        self.show_origin_image(self.path_image)
        self.show_result_image(self.image)
        print(height, width)


                                                        

        




        
