import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime
from src.util.table_util import TableUtil

'''
    Đọc kĩ Frame, do được implement từ Frame
    Tạo giao diện chỉnh sửa thông tin
'''
class EditUI(tb.Frame):
    state_selected = 0

    def __init__(self, master: tb.Toplevel, base_master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.base_master = base_master
        self.pack(fill='both', expand=True)
        self.ui_input_field = self.base_master.ui_input_field.copy()
        self.create_widgets()

    def create_widgets(self):
        self.lbl_frame_reg = {}
        for input_field in self.ui_input_field:
            self.lbl_frame_reg[input_field["label"]] = tb.LabelFrame(self, text=input_field["name_label"], bootstyle="dark", padding=5)
            self.lbl_frame_reg[input_field["label"]].pack(pady=3, fill=X)
            if input_field["label"] == "birthday":
                input_field["widget"] = tb.DateEntry(self.lbl_frame_reg[input_field["label"]], bootstyle="dark")
                input_field["widget"].pack(fill=X)
            else:
                input_field["widget"] = tb.Entry(self.lbl_frame_reg[input_field["label"]], textvariable=input_field["name_var"], bootstyle="dark")
                input_field["widget"].pack(fill=X)

        self.btn_frame = tb.Frame(self, bootstyle="dark")
        self.btn_frame.pack(fill=X, pady=10)
        self.btn_save = tb.Button(self.btn_frame, text="Save", command=self.save, bootstyle="primary")
        self.btn_save.pack(side=LEFT, padx=5)

    def save(self):
        self.base_master.selected_obj.name = self.ui_input_field[0]["name_var"].get()
        self.base_master.selected_obj.address = self.ui_input_field[1]["name_var"].get()
        self.base_master.selected_obj.cmnd = self.ui_input_field[2]["name_var"].get()
        self.base_master.selected_obj.birth_day = datetime.strptime(self.ui_input_field[3]["widget"].entry.get(), "%m/%d/%Y")
        self.base_master.selected_obj.phone = self.ui_input_field[4]["name_var"].get()
        if self.base_master.nb.index(self.base_master.nb.select()) == 0:
            self.base_master.student_dao.update(self.base_master.selected_obj)
            self.base_master.student_data = self.base_master.get_student_data()
            TableUtil.built_data_onchange(self.base_master, self.base_master.student_data, "student")
            EditUI.state_selected = 0
            # self.master.destroy()
        else:
            self.base_master.teacher_dao.update(self.base_master.selected_obj)
            self.base_master.teacher_data = self.base_master.get_teacher_data()
            TableUtil.built_data_onchange(self.base_master, self.base_master.teacher_data, "teacher")
            EditUI.state_selected = 0
            # self.master.destroy()
        
    