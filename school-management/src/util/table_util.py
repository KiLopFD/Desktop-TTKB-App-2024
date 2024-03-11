'''
    Phần Này Đọc Kĩ Doc Treeview, do được implement từ Treeview
'''
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *


class TableUtil:
    @staticmethod
    def initialize_student_table(self, master, data):
        columns = data["columns"]
        rows = data["rows"]
        self.student_table = Tableview(
            master,
            searchable=True,
            coldata=columns,
            rowdata=rows,
        )
        self.student_table.pack(fill=BOTH, expand=True)
        
    @staticmethod
    def initialize_teacher_table(self, master, data):
        columns = data["columns"]
        rows = data["rows"]
        self.teacher_table = Tableview(
            master,
            searchable=True,
            coldata=columns,
            rowdata=rows,
        )
        self.teacher_table.pack(fill=BOTH, expand=True)

        
    @staticmethod
    def built_data_onchange(self, data, table_type):
        if table_type == "teacher":
            self.teacher_table.build_table_data(
                coldata=data["columns"],
                rowdata=data["rows"]
            )
        else:
            self.student_table.build_table_data(
                coldata=data["columns"],
                rowdata=data["rows"]
            )