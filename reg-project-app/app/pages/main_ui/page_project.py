import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from app.utils.main import TableUtil
from app.db.main import ProjectDao, Project
from datetime import datetime
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tableview import Tableview, TableRow
'''
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
'''
'''
    base_master: Self@CompBody
'''


class PageProject(ScrolledFrame):
    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle="dark")
        self.master = master
        self.base_master = base_master
        # DAO
        self.project_dao = ProjectDao()
        # Variables
        self.table_data = self.get_table_data()
        #-----------------------------------------------------------------------
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.overide_style()
        # Global Base Master
        self.base_master.refresh_table_project = self.refresh_table


    def create_widgets(self):
        self.create_table()
        self.create_action_group()
    
    def overide_style(self):
        ...

    def get_table_data(self):
        return {
            "columns": ["id", "name", "description", "start_date", "end_date", "number_register"],
            "rows": self.get_data_project()
        }

    def get_data_project(self):
        return [
            (
                project.id,
                project.name,
                project.description,
                project.start_date,
                project.end_date,
                self.get_account_register(project)
            ) for project in self.project_dao.get_all()
        ]
    
    


    def create_table(self):
        self.lbl_frame = tb.LabelFrame(self, text="Danh sách dự án", height=350, padding=10)
        self.lbl_frame.pack(fill="x", side="top", padx=5, pady=5)
        # Build Table
        self.base_master.table_fields[0]['widget']=TableUtil.initialize_table(self.base_master.table_fields[0]['widget'], self.lbl_frame, data=self.table_data)
        # Add Event for Table
        self.base_master.table_fields[0]['widget'].bind_all('<<TreeviewSelect>>', self.on_select_table)
    
    def on_select_table(self, event):
        rows: list[TableRow]= self.base_master.table_fields[0]['widget'].get_rows(selected=True)
        for row in rows:
            print(row._values)

    
    
    def create_action_group(self):
        self.lbl_frame_action = tb.LabelFrame(self, text="Thiết lập và tùy chỉnh", padding=10, height=200)
        self.lbl_frame_action.pack(fill="x", side="top", padx=5, pady=5)
        # Create Widgets
        frame_form = tb.LabelFrame(self.lbl_frame_action, text="Thông tin dự án", padding=10)
        frame_form.pack(fill="y", side="left")
        self.fields = [
            {
                "label": "name",
                "name": "Tên dự án",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "description",
                "name": "Mô tả",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "start_date",
                "name": "Ngày bắt đầu",
                "var": tb.StringVar(),
                "widget": None,
            },
            {
                "label": "end_date",
                "name": "Ngày kết thúc",
                "var": tb.StringVar(),
                "widget": None,
            },
        ]
        first_row = tb.Frame(frame_form)
        first_row.pack(fill="x", side="top")
        lbl_frame = tb.LabelFrame(first_row, text=self.fields[0]['name'])
        lbl_frame.pack(fill="x", padx=3)
        self.fields[0]['widget'] = tb.Entry(lbl_frame, textvariable=self.fields[0]['var'])
        self.fields[0]['widget'].pack(fill="x", padx=5, pady=5)
        second_row = tb.Frame(frame_form)
        second_row.pack(fill="x", side="top")
        for field in self.fields[2:]:
            lbl_frame = tb.LabelFrame(second_row, text=field['name'])
            lbl_frame.pack(fill="x", side="left", padx=3)
            field['widget'] = tb.DateEntry(lbl_frame)
            field['widget'].pack(fill="x", padx=5, pady=5)
        
        # ScrollText
        self.lbl_frame_description = tb.LabelFrame(self.lbl_frame_action, text="Mô tả", padding=10)
        self.lbl_frame_description.pack(fill="y", side="left", padx=5)
        self.fields[1]['widget'] = ScrolledText(self.lbl_frame_description, height=5, width=40)
        self.fields[1]['widget'].pack(fill="both", padx=5, pady=5)

        # Action Group
        self.lbl_frame_action_group = tb.LabelFrame(self.lbl_frame_action, text="Thao tác", width=200)
        self.lbl_frame_action_group.pack(fill="y", side="left", padx=5)
        # Create Id for project
        lbl_frame = tb.LabelFrame(self.lbl_frame_action_group, text="Nhập id dự án bạn muốn", padding=10)
        lbl_frame.pack(fill="x", side="top", padx=5, pady=5)
        entry = tb.Entry(lbl_frame, width=25)
        entry.pack(fill="x", padx=5, pady=5)
        # Create Button Group
        btn_group = tb.Frame(self.lbl_frame_action_group)
        btn_group.pack(fill="both", side="top", expand=True)
        btn_create = tb.Button(btn_group, text="Tạo mới", bootstyle="primary", command=self.create_project)
        btn_create.pack(side="left", padx=5)
        btn_update = tb.Button(btn_group, text="Cập nhật", bootstyle="secondary")
        btn_update.pack(side="left", padx=5)
        btn_delete = tb.Button(btn_group, text="Xóa", bootstyle="danger")
        btn_delete.pack(side="left", padx=5)
        btn_register = tb.Button(btn_group, text="Đăng ký", bootstyle="info")
        btn_register.pack(side="left", padx=5)
    
    def create_project(self):
        project = Project(
            name=self.fields[0]['var'].get(),
            description=self.fields[1]['widget'].text.get(1.0, "end-1c"),
            start_date=datetime.strptime(self.fields[2]['widget'].entry.get(), "%m/%d/%Y"),
            end_date=datetime.strptime(self.fields[3]['widget'].entry.get(), "%m/%d/%Y"),
        )
        self.project_dao.add(project)
        print('Create project success')
        # Reload data for table
        TableUtil.built_data_onchange(self.base_master.table_fields[0]['widget'],self.get_table_data())

    def refresh_table(self):
        TableUtil.built_data_onchange(self.base_master.table_fields[0]['widget'],self.get_table_data())

    def get_account_register(self, project):
        all_account_in_group = [group.accounts for group in project.groups]
        length = 0
        for accounts in all_account_in_group:
            length += len(accounts)
        return length

