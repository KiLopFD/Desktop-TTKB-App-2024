import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from app.utils.main import TableUtil
from app.db.main import GroupDao, Group, Project, ProjectDao, Account, AccountDao, Task, TaskDao, Grade, GradeDao
from datetime import datetime
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tableview import Tableview, TableRow



class PageTask(tb.Panedwindow):
    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle="info", orient="horizontal")
        self.master = master
        self.base_master = base_master
        self.table_task = None
        #----------------------------------------
        # DAO
        self.group_dao = GroupDao()
        self.project_dao = ProjectDao()
        self.account_dao = AccountDao()
        self.task_dao = TaskDao()
        self.grade_dao = GradeDao()
        # Variables
        self.table_data_group = self.get_table_data_group()
        self.table_data_task = self.get_table_data_task()
        #----------------------------------------
        self.pack(expand=True, fill="both")
        # Create Widgets
        self.create_widgets()
        # Overide Style
        self.overide_style()
        # Global Base Master
        self.base_master.refresh_table_group = self.refresh_table

    def create_widgets(self):
        # Create Frame Left
        self.create_frame_left()
        # Create Frame Right
        self.create_frame_right()

    def create_frame_right(self):
        self.frame_right = tb.Frame(self, bootstyle="dark")
        self.frame_right.pack(fill="both", side="right", expand=True)
        self.add(self.frame_right)
        self.implemenet_frame_right()

    def create_frame_left(self):
        self.frame_left = tb.Frame(self, bootstyle="dark")
        self.frame_left.pack(fill="both", side="left", expand=True)
        self.add(self.frame_left)
        self.implemenet_frame_left()

    def implemenet_frame_left(self):
        self.srcoll_frame_left = ScrolledFrame(self.frame_left, bootstyle="dark")
        self.srcoll_frame_left.pack(fill="both", expand=True)
        # Create Score Group
        self.scrore_evaluate = tb.Meter(
            self.srcoll_frame_left,
            metersize=100,
            amountused=25,
            interactive=True,
            subtextstyle='primary',
            bootstyle='success'
        )
        self.scrore_evaluate.pack(fill='x', padx=3, pady=3)
        # Update the amount used
        lbl_frame = tb.LabelFrame(self.srcoll_frame_left, text="Đánh giá", padding=10)
        lbl_frame.pack(fill="x", side="top", padx=3, pady=3)
        # Entry update
        lbl_frame_score = tb.LabelFrame(lbl_frame, text="Nhập số điểm", padding=10)
        lbl_frame_score.pack(fill="x", padx=3, pady=3)
        self.entry_score = tb.Entry(lbl_frame_score, width=25, textvariable=self.scrore_evaluate.amountusedvar)
        self.entry_score.pack(fill="x", padx=3, pady=3)
        # Group Register
        lbl_frame_group = tb.LabelFrame(lbl_frame, text="Nhóm", padding=10)
        lbl_frame_group.pack(fill="x", padx=3, pady=3)
        # Menu Group
        self.menu_group_left = tb.Menubutton(lbl_frame_group, text="Chọn nhóm", bootstyle="dark")
        self.menu_group_left.pack(fill="x", padx=3, pady=3)
        self.menu_group_left.menu = tb.Menu(self.menu_group_left, tearoff=0)
        self.menu_group_left["menu"] = self.menu_group_left.menu
        # Built Data
        self.built_data_menu_group_left()
        # Add Event
        self.menu_group_left.bind("<Button-1>", self.built_data_menu_group_left)
        #--------------------------------------
        # Table Scrore Group
        lbl_frame_table = tb.LabelFrame(lbl_frame, text="Bảng điểm", padding=10)
        lbl_frame_table.pack(fill="x", padx=3, pady=3)
        # Build Table
        self.table_score_group = TableUtil.initialize_table(self.table_data_group, lbl_frame_table, self.get_table_data_score_group())
        #--------------------------------------
        # Action Group
        lbl_frame_action = tb.LabelFrame(lbl_frame, text="Thao tác", padding=10)
        lbl_frame_action.pack(fill="x", padx=3, pady=3)
        # Button Group
        btn_group = tb.Frame(lbl_frame_action)
        btn_group.pack(fill="both", side="top", expand=True)
        btn_grade = tb.Button(btn_group, text="Đánh giá", bootstyle="primary", command=self.grade_group)
        btn_grade.pack(side="left", padx=3)

    def grade_group(self):
        # if None not in [account.grade for account in self.selected_group_left.accounts]:
        #     print("Đã đánh giá")
        #     return
        score = float(self.scrore_evaluate.amountusedvar.get())
        grade = Grade(
            mark=score,
            date=datetime.strptime(datetime.now().strftime("%m/%d/%Y"), "%m/%d/%Y"),
            accounts=[account for account in self.selected_group_left.accounts]
        )
        self.grade_dao.add(grade)
    
    def get_data_score_group(self):
        if not hasattr(self, "selected_group_left"):
            self.selected_group_left = self.account_dao.get_all()
        else:
            self.selected_group_left = self.selected_group_left.accounts
        return [
            (
                account.id,
                account.grade.mark if account.grade else "Chưa đánh giá",
                account.grade.date if account.grade else "Chưa đánh giá",
                account.username
            ) for account in (self.selected_group_left if self.selected_group_left else [])
        ]
    
    def get_table_data_score_group(self):
        return {
            "columns": ["id", "mark", "date", "username"],
            "rows": self.get_data_score_group()
        }

        
    def built_data_menu_group_left(self, event=None):
        self.menu_group_left.menu.delete(0, "end")
        for group in self.group_dao.get_all():
            self.menu_group_left.menu.add_cascade(label=group.name, command=lambda group=group: self.action_select_group_left(group))

    def action_select_group_left(self, group):
        self.selected_group_left = group
        self.menu_group_left.config(text=group.name)
        
        
    def implemenet_frame_right(self):
        # Create Tab Frame
        self.nb_tab = tb.Notebook(self.frame_right, bootstyle="dark")
        self.nb_tab.pack(fill="both", expand=True)
        # Create Tab
        # Tab 1
        self.frame_tab_1 = tb.Frame(self.nb_tab, bootstyle="dark")
        self.nb_tab.add(self.frame_tab_1, text="Nhóm")
        # Tab 2
        self.frame_tab_2 = tb.Frame(self.nb_tab, bootstyle="dark")
        self.nb_tab.add(self.frame_tab_2, text="Công Việc")
        #----------------------------------------
        # Implement Tab 1
        self.srcoll_frame_right = ScrolledFrame(self.frame_tab_1 , bootstyle="dark")
        self.srcoll_frame_right.pack(fill="both", expand=True)
        # Create Table
        self.create_table_tab1()
        # Create Action Group
        self.create_action_tab1()
        #----------------------------------------
        # Implement Tab 2
        self.srcoll_frame_right_2 = ScrolledFrame(self.frame_tab_2 , bootstyle="dark")
        self.srcoll_frame_right_2.pack(fill="both", expand=True)
        # Create Table
        self.create_table_tab2()
        # Create Action Group
        self.create_action_tab2()
        #----------------------------------------
        # Add event for tab
        self.nb_tab.bind("<<NotebookTabChanged>>", self.on_change_tab)

    def on_change_tab(self, event):
        if self.nb_tab.index(self.nb_tab.select()) == 0:
            TableUtil.built_data_onchange(self.base_master.table_fields[1]["widget"], self.get_table_data_group())
        if self.nb_tab.index(self.nb_tab.select()) == 1:
            print("Tab 2")
            self.update_project_and_group()
            TableUtil.built_data_onchange(self.table_task, self.get_table_data_task())
            
        


    def create_table_tab2(self):
        # print(self.get_table_data_task())
        lbl_frame = tb.LabelFrame(self.srcoll_frame_right_2, text=f'{self.base_master.selected_account.group.name if self.base_master.selected_account.group else "Chưa có nhóm"}', width=500,height=350, padding=10)
        lbl_frame.pack(fill="x", side="top", padx=3, pady=3)
        # Build Table
        self.table_task = TableUtil.initialize_table(self.table_task, lbl_frame, data=self.get_table_data_task())


    def create_action_tab2(self):
        lbl_frame = tb.LabelFrame(self.srcoll_frame_right_2, text="Thao tác", padding=10)
        lbl_frame.pack(fill="x", side="top", padx=3, pady=3)
        # Button Group
        self.field_task = [
            {
                "label": "name",
                "name": "Tên công việc",
                "var": tb.StringVar(value="Tên công việc"),
                "widget": tb.Entry
            },
            {
                "label": "description",
                "name": "Mô tả",
                "var": tb.StringVar(value="Mô tả"),
                "widget": tb.ScrolledText
            },
            {
                "label": "done",
                "name": "Hoàn thành",
                "var": tb.BooleanVar(value=False),
                "widget": tb.Checkbutton
            },
            {
                "label": "deadline",
                "name": "Hạn chót",
                "var": tb.StringVar,
                "widget": tb.DateEntry
            }
        ]
        self.lbl_frame_task = {}
        row = tb.Frame(lbl_frame)
        row.pack(fill="x", side="left")
        cnt = 0
        for field in self.field_task:
            if cnt == 2:
                row = tb.Frame(lbl_frame)
                row.pack(fill="x", side="left")
                cnt = 0
            cnt += 1
            self.lbl_frame_task[field['label']] = tb.LabelFrame(row, text=field['name'], padding=10)
            self.lbl_frame_task[field['label']].pack(fill="x", padx=3, pady=3)
            if field['label'] == "done":
                field['widget'] = tb.Checkbutton(self.lbl_frame_task[field['label']], text=field['name'], variable=field['var'])
                field['widget'].pack(fill="x", padx=3, pady=3)
            elif field['label'] == "deadline":
                field['widget'] = tb.DateEntry(self.lbl_frame_task[field['label']])
                field['widget'].pack(fill="x", padx=3, pady=3)
            elif field['label'] == "description":
                field['widget'] = ScrolledText(self.lbl_frame_task[field['label']], height=5, width=40)
                field['widget'].pack(fill="x", padx=3, pady=3)
            else:
                field['widget'] = tb.Entry(self.lbl_frame_task[field['label']], textvariable=field['var'])
                field['widget'].pack(fill="x", padx=3, pady=3)
        #----------------------------------------
        # Label Frame Create Group
        lbl_frame_create = tb.LabelFrame(lbl_frame, text="Tạo công việc", padding=10)
        lbl_frame_create.pack(fill="x", side="left", padx=3, pady=3)
        # Id to update
        lbl_frame_id = tb.LabelFrame(lbl_frame_create, text="Nhập id công việc", padding=10)
        lbl_frame_id.pack(fill="x", padx=3, pady=3)
        self.entry_id_task = tb.Entry(lbl_frame_id, width=25)
        self.entry_id_task.pack(fill="x", padx=3, pady=3)
        # Button Group
        lbl_frame_btn_group = tb.LabelFrame(lbl_frame_create, text="Thao tác", padding=10)
        lbl_frame_btn_group.pack(fill="x", padx=3, pady=3)
        # Button Create Group
        self.btn_create_task = tb.Button(lbl_frame_btn_group, text="Tạo", bootstyle="primary", command=self.create_task)
        self.btn_create_task.pack(padx=3, pady=3, side="left")
        # Btn Delete All Group
        self.btn_delete_all_task = tb.Button(lbl_frame_btn_group, text="Xóa tất cả", bootstyle="danger", command=self.delete_all_task)
        self.btn_delete_all_task.pack(padx=3, pady=3, side="left")
        # Btn Update Task
        self.btn_update_task = tb.Button(lbl_frame_btn_group, text="Cập nhật", bootstyle="warning", command=self.update_task)
        self.btn_update_task.pack(padx=3, pady=3, side="left")

    def update_task(self):
        task = self.task_dao.get_by_id(int(self.entry_id_task.get()))
        task.name = self.field_task[0]["var"].get() if self.field_task[0]["var"].get() != task.name else task.name
        task.description = self.field_task[1]['widget'].text.get(1.0, "end-1c") if self.field_task[1]['widget'].text.get(1.0, "end-1c") != task.description else task.description
        task.done = self.field_task[2]["var"].get() if self.field_task[2]["var"].get() != task.done else task.done
        task.deadline = datetime.strptime(self.field_task[3]['widget'].entry.get(), "%m/%d/%Y") if datetime.strptime(self.field_task[3]['widget'].entry.get(), "%m/%d/%Y") != task.deadline else task.deadline
        self.task_dao.update(task)
        TableUtil.built_data_onchange(self.table_task, self.get_table_data_task())

    def delete_all_task(self):
        self.task_dao.delete_all()
        TableUtil.built_data_onchange(self.table_task, self.get_table_data_task())

    def create_task(self):
        task = Task(
            name=self.field_task[0]["var"].get(),
            description=self.field_task[1]['widget'].text.get(1.0, "end-1c"),
            done=self.field_task[2]["var"].get(),
            deadline=datetime.strptime(self.field_task[3]['widget'].entry.get(), "%m/%d/%Y"),
            project=self.base_master.selected_account.group.project if self.base_master.selected_account.group else None,
            account=self.base_master.selected_account,
            group=self.base_master.selected_account.group if self.base_master.selected_account.group else None
        )
        self.task_dao.add(task)
        TableUtil.built_data_onchange(self.table_task, self.get_table_data_task())

    def update_project_and_group(self):
        for task in self.task_dao.get_all():
            if task.account == self.base_master.selected_account:
                if self.base_master.selected_account.group.project:
                    print('Project: ', self.base_master.selected_account.group.project)
                    task.project = self.base_master.selected_account.group.project
                if self.base_master.selected_account.group:
                    print('Group: ', self.base_master.selected_account.group)
                    task.group = self.base_master.selected_account.group
                self.task_dao.update(task)

    

    def create_action_tab1(self):
        # Add row
        frame_row = tb.Frame(self.srcoll_frame_right)
        frame_row.pack(fill="x", side="top", padx=3, pady=3)
        lbl_frame = tb.LabelFrame(frame_row, text="Đăng Kí Nhóm", width=500,height=350, padding=10)
        lbl_frame.pack(fill="x", side="left", padx=3, pady=3)
        # Action Group
        lbl_frame_info = tb.LabelFrame(lbl_frame, text="Thông tin nhóm", padding=10)
        lbl_frame_info.pack(side="left", padx=3, pady=3)
        # Fields
        self.register_fields = [
            {
                "label": "group_name",
                "name": "Tên nhóm",
                "var": tb.StringVar(value="Tên nhóm"),
                "widget": tb.Menubutton
            },
            {
                "label": "project_name",
                "name": "Tên dự án",
                "var": tb.StringVar(value="Tên dự án"),
                "widget": tb.Menubutton
            }
        ]
        # Create Widgets
        self.lbl_frame_reg = {}
        for field in self.register_fields:
            self.lbl_frame_reg[field['label']] = tb.LabelFrame(lbl_frame_info, text=field['name'], padding=10)
            self.lbl_frame_reg[field['label']].pack(fill="x", padx=3, pady=3)
            field['widget'] = tb.Menubutton(self.lbl_frame_reg[field['label']], bootstyle="dark", text=field['name'], textvariable=field['var'])
            field['widget'].pack(fill="x", padx=3, pady=3)
        #  Implement Menu When data change
        self.immplement_menu_group()

        # Action Group
        lbl_frame_action = tb.LabelFrame(lbl_frame, text="Thao tác", padding=10)
        lbl_frame_action.pack(side="left", padx=3, pady=3)
        # Button Group
        btn_group = tb.Frame(lbl_frame_action)
        btn_group.pack(fill="both", side="top", expand=True)
        btn_register = tb.Button(btn_group, text="Đăng kí", bootstyle="primary", command=self.action_register_group)
        btn_register.pack(side="left", padx=3)
        #----------------------------------------
        # Label Frame Create Group
        lbl_frame_create = tb.LabelFrame(frame_row, text="Tạo nhóm", padding=10)
        lbl_frame_create.pack(side="left", padx=3, pady=3)
        # Fields
        self.list_number_create_group = [i for i in range(0, 100 + 1, 5)]
        # Create Widgets
        self.lbl_frame_create = tb.LabelFrame(lbl_frame_create, text="Tạo nhóm", padding=10)
        self.lbl_frame_create.pack(fill="x", padx=3, pady=3)
        self.menu_number_group = tb.Menubutton(self.lbl_frame_create, text="Số Lượng")
        self.menu_number_group.pack(fill="x", padx=3, pady=3)
        self.menu_number_group.menu = tb.Menu(self.menu_number_group, tearoff=0)
        self.menu_number_group["menu"] = self.menu_number_group.menu
        for number in self.list_number_create_group:
            self.menu_number_group.menu.add_cascade(label=number, command=lambda number=number: self.menu_number_group.config(text=number))
        # Button Create Group
        # Btn Create Group
        lbl_frame_action = tb.LabelFrame(lbl_frame_create, text="Thao tác", padding=10)
        lbl_frame_action.pack(fill='x', padx=3, pady=3)
        self.btn_create_group = tb.Button(lbl_frame_action, text="Tạo", bootstyle="primary", command=self.create_group)
        self.btn_create_group.pack(padx=3, pady=3, side="left")
        # Btn Delete All Group
        self.btn_delete_all_group = tb.Button(lbl_frame_action, text="Xóa tất cả", bootstyle="danger", command=self.delete_all_group)
        self.btn_delete_all_group.pack(padx=3, pady=3, side="left")
        # Group Registered
        self.lbl_frame_reg = tb.LabelFrame(frame_row, text="Nhóm đã đăng kí", padding=10)
        self.lbl_frame_reg.pack(fill="x", side="left", padx=3, pady=3)
        self.show_group_registered()

    def show_group_registered(self):
        account = self.base_master.selected_account
        if hasattr(self, "lbl_reg_group"):
            self.lbl_reg_group.destroy()
        if account.group:
            self.lbl_reg_group = tb.Label(self.lbl_frame_reg, text=account.group.name, bootstyle="success", font=("Arial", 15))
            self.lbl_reg_group.pack(pady=3)
        else:
            self.lbl_reg_group = tb.Label(self.lbl_frame_reg, text="Chưa đăng kí nhóm", bootstyle="warning")
            self.lbl_reg_group.pack(pady=3)

    def immplement_menu_group(self):
        self.menu_group = self.register_fields[0]["widget"]
        self.menu_project = self.register_fields[1]["widget"]
        self.menu_group.menu = tb.Menu(self.menu_group, tearoff=0)
        self.menu_group["menu"] = self.menu_group.menu
        self.menu_project.menu = tb.Menu(self.menu_project, tearoff=0)
        self.menu_project["menu"] = self.menu_project.menu
        # Built Data
        self.built_data_menu_group()
        self.built_data_menu_project()
        # Add Event
        self.menu_group.bind("<Button-1>", self.built_data_menu_group)
        self.menu_project.bind("<Button-1>", self.built_data_menu_project)

    def built_data_menu_group(self, event=None):
        self.menu_group.menu.delete(0, "end")
        for group in self.group_dao.get_all():
            self.menu_group.menu.add_cascade(label=group.name, command=lambda group=group: self.action_select_group(group))

    def action_select_group(self, group):
        self.selected_group_right = group
        self.register_fields[0]["var"].set(group.name)
        

    def built_data_menu_project(self, event=None):
        self.menu_project.menu.delete(0, "end")
        for project in self.project_dao.get_all():
            self.menu_project.menu.add_cascade(label=project.name, command=lambda project=project: self.action_select_project(project))

    def action_select_project(self, project):
        self.selected_project = project
        self.register_fields[1]["var"].set(project.name)
        print(self.base_master.selected_account)



    def delete_all_group(self):
        # Delete All Account Register
        for group in self.group_dao.get_all():
            for account in group.accounts:
                group.accounts.remove(account)
            self.group_dao.update(group)
        # Delete All Group
        self.group_dao.delete_all()
        TableUtil.built_data_onchange(self.base_master.table_fields[1]["widget"], self.get_table_data_group())
        # Clear Menu
        self.menu_group.menu.delete(0, "end")
        self.register_fields[0]["var"].set("Tên nhóm")
        self.menu_project.menu.delete(0, "end")
        self.register_fields[1]["var"].set("Tên dự án")
        # Clear Selected
        self.selected_group_right = None
        self.selected_project = None
        # Refresh Label
        self.show_group_registered()


    def create_group(self):
        self.max_id_group = max([group.id for group in self.group_dao.get_all()]) if len(self.group_dao.get_all()) > 0 else 0
        print(self.menu_number_group.cget("text"))
        for _ in range(int(self.menu_number_group.cget("text"))):
            self.max_id_group += 1
            group = Group(name=f"Group {self.max_id_group}", accounts=[], project=None)
            self.group_dao.add(group)
        TableUtil.built_data_onchange(self.base_master.table_fields[1]["widget"], self.get_table_data_group())

    def action_register_group(self):
        if self.selected_group_right and self.selected_project:
            self.selected_group_right.project = self.selected_project
            self.selected_group_right.accounts.append(self.base_master.selected_account)
            self.group_dao.update(self.selected_group_right)
            self.show_group_registered()
            self.remove_project_group()
            TableUtil.built_data_onchange(self.base_master.table_fields[1]["widget"], self.get_table_data_group())
        else:
            print("Chưa chọn nhóm hoặc dự án")

    def remove_project_group(self):
        for group in self.group_dao.get_all():
            if group.project and len(group.accounts) == 0:
                # print('Group id: ',group.id)
                group.project = None
                self.group_dao.update(group)

    def overide_style(self):
        self.frame_left.config(width=500)

    # ----------------------------------------
    # Tab 1
    def get_table_data_group(self):
        return {
            "columns": ["id", "name", "number_register", "project"],
            "rows": self.get_data_group()
        }
    
    def get_data_group(self):
        return [
            (
                group.id,
                group.name,
                len(group.accounts),
                group.project.name if group.project else "Chưa có dự án"
            ) for group in self.group_dao.get_all()
        ]
    
    # ----------------------------------------
    # Tab 2
    def get_table_data_task(self):
        return {
            "columns": ["id", "name", "description", "done", "deadline", "project", "account", "group"],
            "rows": self.get_data_task()
        }
    
    def get_data_task(self):
        return [
            (
                task.id,
                task.name,
                task.description,
                task.done,
                task.deadline,
                task.project.name if task.project else "Chưa có dự án",
                task.account.username if task.account else "Chưa có người dùng",
                task.group.name if task.group else "Chưa có nhóm"
            ) for task in self.task_dao.get_all() if task.group == self.base_master.selected_account.group
        ]
    
    def create_table_tab1(self):
        # Create Label Frame
        self.lbl_frame = tb.LabelFrame(self.srcoll_frame_right, text="Danh sách nhóm", width=500,height=350, padding=10)
        self.lbl_frame.pack(fill="x", side="top", padx=3, pady=3)
        # Build Table
        self.base_master.table_fields[1]["widget"] = TableUtil.initialize_table(self.base_master.table_fields[1]["widget"], self.lbl_frame, data=self.table_data_group)
        # Add Event for Table
        self.base_master.table_fields[1]["widget"].bind_all("<<TreeviewSelect>>", self.on_select_table)
        # Event Click
        self.base_master.table_fields[1]["widget"].bind_all("<Double-1>", self.on_double_click_table)

    def on_double_click_table(self, event):
        if self.nb_tab.index(self.nb_tab.select()) == 0:
            print("Tab 1")
            rows: list[TableRow]= self.base_master.table_fields[1]["widget"].get_rows(selected=True)
            selected_row = rows[0]._values
            self.selected_group_left = self.group_dao.get(int(selected_row[0]))
            print(self.selected_group_left)
            self.refresh_table_score_group()
            return

        if self.nb_tab.index(self.nb_tab.select()) == 1:
            print("Tab 2")
            rows: list[TableRow]= self.table_task.get_rows(selected=True)
            for row in rows:
                print(row._values)
            return

    def on_select_table(self, event):
        # if self.nb_tab.index(self.nb_tab.select()) == 0:
        #     print("Tab 1")
        #     rows: list[TableRow]= self.base_master.table_fields[1]["widget"].get_rows(selected=True)
        #     selected_row = rows[0]._values
        #     self.selected_group_left = self.group_dao.get(int(selected_row[0]))
        #     print(self.selected_group_left)
        #     return

        # if self.nb_tab.index(self.nb_tab.select()) == 1:
        #     print("Tab 2")
        #     rows: list[TableRow]= self.table_task.get_rows(selected=True)
        #     for row in rows:
        #         print(row._values)
        #     return
        ...

    def refresh_table_score_group(self):
        TableUtil.built_data_onchange(self.table_score_group, self.get_table_data_score_group())
        return

    def refresh_table(self):
        TableUtil.built_data_onchange(self.base_master.table_fields[1]["widget"], self.get_table_data_group())
        # TableUtil.built_data_onchange(self.table_task, self.get_table_data_task())