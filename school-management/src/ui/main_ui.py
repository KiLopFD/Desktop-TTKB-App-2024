import ttkbootstrap as tb 
from src.configs.theme_window import window, config_window, edit_window
from ttkbootstrap.constants import *
from src.db.dao.student_dao import StudentDao
from src.db.setup import Student, Teacher
from src.db.dao.teacher_dao import TeacherDao
from datetime import datetime
from src.util.table_util import TableUtil
from ttkbootstrap.tooltip import ToolTip
from src.util.validation_util import FormValidation
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from src.ui.edit_ui import EditUI

'''
    Đọc kĩ Frame, do được implement từ Frame
    Tạo giao diện chính
'''
class MainUI(tb.Frame):
    def __init__(self, master=None, role='student', **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.role = role
        self.pack(fill=BOTH, expand=YES)
        # Setup UI
        # Style 
        self.app_style = {
            "font": "Arial 12",
            "fg": "white",
        }
        #---------------------
        self.tb_style = tb.Style()
        self.tb_style.configure(".", **self.app_style)
        self.tb_style.configure("TLabel", font=f"{self.app_style['font']} bold")
        EditUI.state_selected = 0

        # UI Input
        self.ui_input_field = [
            {
                "label": "fullname",
                "name_label": "Họ và tên",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "address",
                "name_label": "Địa chỉ",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "cmnd",
                "name_label": "CMND",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "birthday",
                "name_label": "Ngày sinh",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "phone",
                "name_label": "Số điện thoại",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "sex",
                "name_label": "Giới tính",
                "name_var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "email",
                "name_label": "Email",
                "name_var": tb.StringVar(),
                "widget": None,
            }
        ]
        #---------------------
        # Create widgets
        self.create_widgets()
        # Create Table UI
        self.student_data = self.get_student_data()
        TableUtil.initialize_student_table(self, self.ctn_show_student, self.student_data)
        self.teacher_data = self.get_teacher_data()
        TableUtil.initialize_teacher_table(self, self.ctn_show_teacher, self.teacher_data)
        # Add Event
        self.student_table.bind_all('<<TreeviewSelect>>', self.edit_detail)
        self.teacher_table.bind_all('<<TreeviewSelect>>', self.edit_detail)

        # DAO
        self.student_dao = StudentDao()
        self.teacher_dao = TeacherDao()
        #---------------------
        # Validate
        FormValidation.base_master = self
        FormValidation.check_all_field(self.ui_input_field)
        # Overide Style
        self.overide_style()


    

    def get_student_data(self):
        return {
            "columns": ["Id", "Họ và tên", "Địa chỉ", "CMND", "Ngày sinh", "Số điện thoại", "Giới tính", "Email"],
            "rows": [
                (student.id, student.name, student.address, student.cmnd, student.birth_day, student.phone, student.sex, student.email) for student in StudentDao().get_all()
            ]
        }
    
    def get_teacher_data(self):
        return {
            "columns": ["Id", "Họ và tên", "Địa chỉ", "CMND", "Ngày sinh", "Số điện thoại", "Giới tính", "Email"],
            "rows": [
                (teacher.id, teacher.name, teacher.address, teacher.cmnd, teacher.birth_day, teacher.phone, teacher.sex, teacher.email) for teacher in TeacherDao().get_all()
            ]
        }
    
    def get_full_widget(self):
        return dict(zip([field["label"] for field in self.ui_input_field], [field["widget"] for field in self.ui_input_field]))
    
    def create_widgets(self):
        # Split into two frames
        self.create_frame()
        
    
    def create_frame(self):
        self.frame_left = tb.Frame(self, width=400, bootstyle="dark")
        self.frame_left.pack(side="left", expand=YES, fill=BOTH)
        self.frame_right = tb.Frame(self, height=500, width=1000)
        self.frame_right.pack(side="right", expand=YES, fill=BOTH)
        # Create UI for frame right
        self.create_ui_frame_right()
        # Create UI for frame left
        self.create_ui_frame_left()
        # Create teacher action widgets
        self.create_teacher_action_widgets()
        # Add Event
        self.nb.bind("<<NotebookTabChanged>>", self.nb_change_tab)
    
    def nb_change_tab(self, *args):
        if self.nb.index(self.nb.select()) == 0:
            print("Student")
            self.student_data = self.get_student_data()
            TableUtil.built_data_onchange(self, self.student_data, "student")
            self.tooltip_id = ToolTip(self.ctn_id_update, "Nhập ID để cập nhật hoặc xóa cho sinh viên")
            self.btn_add.configure(command=self.add_student)
            self.btn_update.configure(command=self.update_student)
            self.btn_delete.configure(command=self.delete_student)
        else:
            print("Teacher")
            self.teacher_data = self.get_teacher_data()
            TableUtil.built_data_onchange(self, self.teacher_data, "teacher")
            self.tooltip_id = ToolTip(self.ctn_id_update, "Nhập ID để cập nhật hoặc xóa cho giáo viên")
            self.btn_add.configure(command=self.add_teacher)
            self.btn_update.configure(command=self.update_teacher)
            self.btn_delete.configure(command=self.delete_teacher)

    def create_ui_frame_left(self):
        self.frame_left.configure(padding=10)
        self.ctn_input = tb.LabelFrame(self.frame_left, text="Nhập thông tin", bootstyle="dark", padding=10)
        self.ctn_input.pack(pady=10, fill=BOTH,)
        # Create input
        self.lbl_frame_reg = {}
        for input_field in self.ui_input_field:
            self.lbl_frame_reg[input_field["label"]] = tb.LabelFrame(self.ctn_input, text=input_field["name_label"], bootstyle="dark", padding=5)
            self.lbl_frame_reg[input_field["label"]].pack(pady=3, fill=X)
            if input_field["label"] == "birthday":
                input_field["widget"] = tb.DateEntry(self.lbl_frame_reg[input_field["label"]], bootstyle="dark")
                input_field["widget"].pack(fill=X)
            else:
                input_field["widget"] = tb.Entry(self.lbl_frame_reg[input_field["label"]], textvariable=input_field["name_var"], bootstyle="dark")
                input_field["widget"].pack(fill=X)
            
        # Create button group
        self.ctn_btn = tb.LabelFrame(self.frame_left, text="Chức năng", bootstyle="primary", padding=10)
        # Add Row ID
        self.ctn_id_update = tb.Frame(self.ctn_btn)
        self.ctn_id_update.pack(pady=10, fill=X)
        self.label_id = tb.Label(self.ctn_id_update, text="ID", bootstyle="primary")
        self.label_id.pack(side="left")
        self.entry_id = tb.Entry(self.ctn_id_update, bootstyle="primary")
        self.entry_id.pack(side="left", padx=5)
        # ---------------------
        # Add Button Acitons
        self.ctn_btn.pack(pady=10, fill=X)
        self.btn_add = tb.Button(self.ctn_btn, text="Thêm", bootstyle="primary")
        self.btn_add.pack(side="left", padx=5)
        self.btn_update = tb.Button(self.ctn_btn, text="Cập nhật", bootstyle="primary")
        self.btn_update.pack(side="left", padx=5)
        self.btn_delete = tb.Button(self.ctn_btn, text="Xóa", bootstyle="primary")
        self.btn_delete.pack(side="left", padx=5)


    def create_ui_frame_right(self):
        self.frame_right.configure(padding=10)
        self.nb = tb.Notebook(self.frame_right, width=1000, height=500)
        #---------------------
        # Create Tab
        self.ctn_show_student = tb.LabelFrame(self.nb, text="Danh sách học sinh", bootstyle="primary", padding=10)
        self.nb.add(self.ctn_show_student, text="Học sinh")
        self.ctn_show_teacher = tb.LabelFrame(self.nb, text="Danh sách giáo viên", bootstyle="primary", padding=10)
        self.nb.add(self.ctn_show_teacher, text="Giáo viên")
        self.nb.pack(fill=BOTH, expand=YES)
        #---------------------
        # Hide Teacher Tab
        self.check_show_data()
        
    def check_show_data(self):
        if self.role == "student":
            self.nb.hide(self.ctn_show_teacher)

    def create_teacher_action_widgets(self):
        self.ctn_action = tb.LabelFrame(self.frame_right, text="Mở Teacher App", bootstyle="primary", padding=10)
        self.ctn_action.pack(pady=10, fill=X)
        # Create New Window

        #---------------------
        self.btn_open = tb.Button(self.ctn_action, text="Mở", 
        bootstyle="primary", command=self.open_teacher_app)
        self.btn_open.pack(side="left", padx=5)


    def open_teacher_app(self):
        new_window = tb.Toplevel(title="Teacher App", position=(250, 250))
        MainUI(master=new_window, role="teacher")
        new_window.mainloop()

    # Actions For Student
    def add_student(self):
        FormValidation.check_all_field(self.ui_input_field)
        print([value for value in FormValidation.state_validate.values() if value == True].count(True))
        if [value for value in FormValidation.state_validate.values() if value == True].count(True) == 7: # 7 Field
            toast = ToastNotification(
                title="Add Student Success",
                message="Thêm học sinh thành công",
                duration=3000,
            )
            toast.show_toast()
            student = Student(
                name=self.ui_input_field[0]["name_var"].get(),
                address=self.ui_input_field[1]["name_var"].get(),
                cmnd=self.ui_input_field[2]["name_var"].get(),
                birth_day=datetime.strptime(self.ui_input_field[3]["widget"].entry.get(), "%m/%d/%Y"),
                phone=self.ui_input_field[4]["name_var"].get(),
                sex=self.ui_input_field[5]["name_var"].get(),
                email=self.ui_input_field[6]["name_var"].get()
            )
            self.student_dao.add(student)
            print("Add student success", student)
            self.student_data = self.get_student_data()
            TableUtil.built_data_onchange(self, self.student_data, "student")
            FormValidation.state_validate={} # Uncheck all field
            self.clear_all_input()

        else:
            toast = ToastNotification(
                title="Add Student Fail",
                message="Thêm học sinh không thành công",
                duration=3000,
                bootstyle="danger"
            )
            toast.show_toast()
            FormValidation.state_validate = {}

    
    def clear_all_input(self):
        for input_field in self.ui_input_field:
            if input_field["label"] == "birthday":
                input_field["widget"].entry.setvar("", datetime.strftime(datetime.now(), "%m/%d/%Y"))
            else:
                input_field["name_var"].set("")

    
    def update_student(self):
        FormValidation.uncheck_all_field(self.ui_input_field)
        FormValidation.state_validate={}
        student = self.student_dao.get_by_id(self.entry_id.get())
        student.name = self.ui_input_field[0]["name_var"].get() if self.ui_input_field[0]["name_var"].get() != "" else student.name
        student.address = self.ui_input_field[1]["name_var"].get() if self.ui_input_field[1]["name_var"].get() != "" else student.address
        student.cmnd = self.ui_input_field[2]["name_var"].get() if self.ui_input_field[2]["name_var"].get() != "" else student.cmnd
        student.birth_day = datetime.strptime(self.ui_input_field[3]["widget"].entry.get(), "%m/%d/%Y") if self.ui_input_field[3]["widget"].entry.get() !=  datetime.strftime(datetime.now(), "%m/%d/%Y") else student.birth_day
        student.phone = self.ui_input_field[4]["name_var"].get() if self.ui_input_field[4]["name_var"].get() != "" else student.phone
        student.sex = self.ui_input_field[5]["name_var"].get() if self.ui_input_field[5]["name_var"].get() != "" else student.sex
        student.email = self.ui_input_field[6]["name_var"].get() if self.ui_input_field[6]["name_var"].get() != "" else student.email
        self.student_dao.update(student)
        print("Update student success", student)
        self.student_data = self.get_student_data()
        TableUtil.built_data_onchange(self, self.student_data, "student")
        self.clear_all_input()

    def delete_student(self):
        FormValidation.uncheck_all_field(self.ui_input_field)
        FormValidation.state_validate={}
        student_dao = StudentDao()
        student = student_dao.get_by_id(self.entry_id.get())
        student_dao.delete(student)
        print("Delete student success", student)
        self.student_data = self.get_student_data()
        TableUtil.built_data_onchange(self, self.student_data, "student")

    # Actions For Teacher
    def add_teacher(self):
        FormValidation.check_all_field(self.ui_input_field)
        if [value for value in FormValidation.state_validate.values() if value == True].count(True) == 7:
            toast = ToastNotification(
                title="Add Teacher Success",
                message="Thêm giáo viên thành công",
                duration=3000,
            )
            toast.show_toast()
            teacher_dao = TeacherDao()
            teacher = Teacher(
                name=self.ui_input_field[0]["name_var"].get(),
                address=self.ui_input_field[1]["name_var"].get(),
                cmnd=self.ui_input_field[2]["name_var"].get(),
                birth_day=datetime.strptime(self.ui_input_field[3]["widget"].entry.get(), "%m/%d/%Y"),
                phone=self.ui_input_field[4]["name_var"].get(),
                sex=self.ui_input_field[5]["name_var"].get(),
                email=self.ui_input_field[6]["name_var"].get()
            )
            teacher_dao.add(teacher)
            print("Add teacher success", teacher)
            self.teacher_data = self.get_teacher_data()
            TableUtil.built_data_onchange(self, self.teacher_data, "teacher")
            FormValidation.state_validate={} # Uncheck all field
            self.clear_all_input()
        else:
            toast = ToastNotification(
                title="Add Teacher Fail",
                message="Thêm giáo viên không thành công",
                duration=3000,
                bootstyle="danger"
            )
            toast.show_toast()
            self.clear_all_input()
            FormValidation.state_validate = {}

    def update_teacher(self):
        FormValidation.uncheck_all_field(self.ui_input_field)
        teacher = self.teacher_dao.get_by_id(self.entry_id.get())
        teacher.name = self.ui_input_field[0]["name_var"].get() if self.ui_input_field[0]["name_var"].get() != "" else teacher.name
        teacher.address = self.ui_input_field[1]["name_var"].get() if self.ui_input_field[1]["name_var"].get() != "" else teacher.address
        teacher.cmnd = self.ui_input_field[2]["name_var"].get() if self.ui_input_field[2]["name_var"].get() != "" else teacher.cmnd
        teacher.birth_day = datetime.strptime(self.ui_input_field[3]["widget"].entry.get(), "%m/%d/%Y") if self.ui_input_field[3]["widget"].entry.get() !=  datetime.strftime(datetime.now(), "%m/%d/%Y") else teacher.birth_day
        teacher.phone = self.ui_input_field[4]["name_var"].get() if self.ui_input_field[4]["name_var"].get() != "" else teacher.phone
        teacher.sex = self.ui_input_field[5]["name_var"].get() if self.ui_input_field[5]["name_var"].get() != "" else teacher.sex
        teacher.email = self.ui_input_field[6]["name_var"].get() if self.ui_input_field[6]["name_var"].get() != "" else teacher.email
        self.teacher_dao.update(teacher)
        print("Update teacher success", teacher)
        self.teacher_data = self.get_teacher_data()
        TableUtil.built_data_onchange(self, self.teacher_data, "teacher")
        self.clear_all_input()

    def delete_teacher(self):
        FormValidation.uncheck_all_field(self.ui_input_field)
        FormValidation.state_validate={}
        teacher_dao = TeacherDao()
        teacher = teacher_dao.get_by_id(self.entry_id.get())
        teacher_dao.delete(teacher)
        print("Delete teacher success", teacher)
        self.teacher_data = self.get_teacher_data()
        TableUtil.built_data_onchange(self, self.teacher_data, "teacher")

    # Edit Detail
    def edit_detail(self, event):
        ...
        # selected_rows = self.student_table.get_rows(selected=True)
        # for row in selected_rows:
        #     if EditUI.state_selected > 3:
        #         '''
        #             Đã fix lỗi khi mở nhiều cửa sổ chỉnh sửa
        #             - Kiểm tra nếu có cửa sổ chỉnh sửa thì destroy cửa sổ đó, mở EditUI mới
        #             - Tạo cửa sổ mới
        #             - Lấy dữ liệu từ row được chọn
        #         '''
        #         if hasattr(self, "new_window"): 
        #             self.new_window.destroy()
        #         self.new_window = tb.Toplevel(**edit_window)
        #         print(row.values[0])
        #         if self.nb.index(self.nb.select()) == 0:
        #             self.selected_obj = self.student_dao.get_by_id(row.values[0])
        #         else:
        #             self.selected_obj = self.teacher_dao.get_by_id(row.values[0])
        #         EditUI(self.new_window, self)
        #         self.new_window.mainloop()
        #     EditUI.state_selected += 1


    # Overide
    def overide_style(self):
        self.frame_left.config(width=400)
    
    





        






def run_ui():
    MainUI(master=window)
    window.mainloop()