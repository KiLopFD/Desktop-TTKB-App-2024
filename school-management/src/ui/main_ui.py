import ttkbootstrap as tb 
from src.configs.theme_window import window, config_window
from ttkbootstrap.constants import *
from src.db.dao.student_dao import StudentDao
from src.db.setup import Student, Teacher
from src.db.dao.teacher_dao import TeacherDao
from datetime import datetime
from src.util.table_util import TableUtil
from ttkbootstrap.tooltip import ToolTip


class MainUI(tb.Frame):
    def __init__(self, master=None, role='student', **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.role = role
        self.pack()
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
        # UI Input
        self.ui_input_field = [
            {
                "label": "full_name",
                "name_label": "Họ và tên",
                "name_var": tb.StringVar(),
            },
            {
                "label": "address",
                "name_label": "Địa chỉ",
                "name_var": tb.StringVar(),
            },
            {
                "label": "cmnd",
                "name_label": "CMND",
                "name_var": tb.StringVar(),
            },
            {
                "label": "birthday",
                "name_label": "Ngày sinh",
                "name_var": tb.StringVar(),
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

    def get_student_data(self):
        return {
            "columns": ["Id", "Họ và tên", "Địa chỉ", "CMND", "Ngày sinh"],
            "rows": [
                (student.id, student.name, student.address, student.cmnd, student.birth_day) for student in StudentDao().get_all()
            ]
        }
    
    def get_teacher_data(self):
        return {
            "columns": ["Id", "Họ và tên", "Địa chỉ", "CMND", "Ngày sinh"],
            "rows": [
                (teacher.id, teacher.name, teacher.address, teacher.cmnd, teacher.birth_day) for teacher in TeacherDao().get_all()
            ]
        }
    
    def create_widgets(self):
        # Split into two frames
        self.create_frame()
        
    
    def create_frame(self):
        self.frame_left = tb.Frame(self, height=500, width=400, bootstyle="dark")
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
        self.ctn_input = tb.LabelFrame(self.frame_left, text="Nhập thông tin", bootstyle="primary", padding=10)
        self.ctn_input.pack(pady=10)
        # Create input
        for input_field in self.ui_input_field:
            self.row_input = tb.Frame(self.ctn_input)
            self.row_input.pack(pady=5, fill=X)
            self.label = tb.Label(self.row_input, text=input_field["name_label"], bootstyle="primary")
            self.label.pack(side="left")
            if input_field["label"] == "birthday":
                self.dt_entry = tb.DateEntry(self.row_input,)
                self.dt_entry.pack(side="right")
            else:
                self.entry = tb.Entry(self.row_input, textvariable=input_field["name_var"], bootstyle="primary")
            self.entry.pack(side="right")
        # Create button group
        self.ctn_btn = tb.LabelFrame(self.frame_left, text="Chức năng", bootstyle="primary", padding=10)
        # Add Row ID
        self.ctn_id_update = tb.Frame(self.ctn_btn)
        self.ctn_id_update.pack(pady=10, fill=X)
        self.label_id = tb.Label(self.ctn_id_update, text="ID", bootstyle="primary")
        self.label_id.pack(side="left")
        self.entry_id = tb.Entry(self.ctn_id_update, bootstyle="primary")
        self.entry_id.pack(side="right")
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
        self.ctn_show_student = tb.LabelFrame(self.nb, text="Danh sách học sinh", bootstyle="primary", padding=10)
        self.nb.add(self.ctn_show_student, text="Học sinh")
        self.ctn_show_teacher = tb.LabelFrame(self.nb, text="Danh sách giáo viên", bootstyle="primary", padding=10)
        self.nb.add(self.ctn_show_teacher, text="Giáo viên")
        self.nb.pack(fill=BOTH, expand=YES)
        #---------------------
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
        student_dao = StudentDao()
        student = Student(
            name=self.ui_input_field[0]["name_var"].get(),
            address=self.ui_input_field[1]["name_var"].get(),
            cmnd=self.ui_input_field[2]["name_var"].get(),
            birth_day=datetime.strptime(self.dt_entry.entry.get(), "%m/%d/%Y"),
        )
        student_dao.add(student)
        print("Add student success", student)
        self.student_data = self.get_student_data()
        TableUtil.built_data_onchange(self, self.student_data, "student")
    
    def update_student(self):
        student_dao = StudentDao()
        student = student_dao.get_by_id(self.entry_id.get())
        student.name = self.ui_input_field[0]["name_var"].get()
        student.address = self.ui_input_field[1]["name_var"].get()
        student.cmnd = self.ui_input_field[2]["name_var"].get()
        student.birth_day = datetime.strptime(self.dt_entry.entry.get(), "%m/%d/%Y")
        student_dao.update(student)
        print("Update student success", student)
        self.student_data = self.get_student_data()
        TableUtil.built_data_onchange(self, self.student_data, "student")

    def delete_student(self):
        student_dao = StudentDao()
        student = student_dao.get_by_id(self.entry_id.get())
        student_dao.delete(student)
        print("Delete student success", student)
        self.student_data = self.get_student_data()
        TableUtil.built_data_onchange(self, self.student_data, "student")

    # Actions For Teacher
    def add_teacher(self):
        teacher_dao = TeacherDao()
        teacher = Teacher(
            name=self.ui_input_field[0]["name_var"].get(),
            address=self.ui_input_field[1]["name_var"].get(),
            cmnd=self.ui_input_field[2]["name_var"].get(),
            birth_day=datetime.strptime(self.dt_entry.entry.get(), "%m/%d/%Y"),
        )
        teacher_dao.add(teacher)
        print("Add teacher success", teacher)
        self.teacher_data = self.get_teacher_data()
        TableUtil.built_data_onchange(self, self.teacher_data, "teacher")

    def update_teacher(self):
        teacher_dao = TeacherDao()
        teacher = teacher_dao.get_by_id(self.entry_id.get())
        teacher.name = self.ui_input_field[0]["name_var"].get()
        teacher.address = self.ui_input_field[1]["name_var"].get()
        teacher.cmnd = self.ui_input_field[2]["name_var"].get()
        teacher.birth_day = datetime.strptime(self.dt_entry.entry.get(), "%m/%d/%Y")
        teacher_dao.update(teacher)
        print("Update teacher success", teacher)
        self.teacher_data = self.get_teacher_data()
        TableUtil.built_data_onchange(self, self.teacher_data, "teacher")

    def delete_teacher(self):
        teacher_dao = TeacherDao()
        teacher = teacher_dao.get_by_id(self.entry_id.get())
        teacher_dao.delete(teacher)
        print("Delete teacher success", teacher)
        self.teacher_data = self.get_teacher_data()
        TableUtil.built_data_onchange(self, self.teacher_data, "teacher")

    
    





        






def run_ui():
    MainUI(master=window)
    window.mainloop()