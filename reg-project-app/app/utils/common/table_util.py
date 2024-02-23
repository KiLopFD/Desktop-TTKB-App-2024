'''
    Lưu Ý: Phần Này Đọc Kĩ Doc Treeview, do được implement từ Treeview
'''
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *


class TableUtil:
    @staticmethod
    def initialize_table(widget, master, data):
        columns = data["columns"]
        rows = data["rows"]
        widget = Tableview(
            master,
            searchable=True,
            coldata=columns,
            rowdata=rows,
        )
        widget.pack(expand=YES, fill=BOTH)
        return widget


    @staticmethod
    def built_data_onchange(widget, data):
        widget.build_table_data(
            coldata=data["columns"],
            rowdata=data["rows"]
        )