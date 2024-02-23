import ttkbootstrap as tb
from app.pages.main_ui.page_project import PageProject
from app.db.main import ProjectDao



class CompBody(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master # Self@MainUI
        # Variables
        self.table_fields = [
            {
                "label": "project_table_db",
                "name": "Tên Dự Án",
                "widget": None,
                "master": None,
            },
            {
                "label": "task_table_db",
                "name": "Tên Công Việc",
                "widget": None,
                "master": None,
            },
            {
                "label": "account_table_db",
                "name": "Người Dùng",
                "widget": None,
                "master": None,
            }
        ]
        #-----------------------------------------------------------------------
        self.pack(expand=True, fill="both")
        # Project Dao
        self.project_dao = ProjectDao()
        # Create widgets
        self.create_widgets()
        # Overide Style
        self.overide_style()

    def create_widgets(self):
        self.create_left_bar()
        self.create_main_content()

    def create_left_bar(self):
        self.left_bar = tb.Frame(self, bootstyle="dark", width=300)
        self.left_bar.pack(fill="y", side="left")
        tb.Separator(self, orient="vertical").pack(fill="y", side="left")
        # Create Widgets for action
        self.list_action = ["Projects", "Taks", "People", "File", "Info"]
        self.create_action_widgets()
    
    def create_action_widgets(self):
        first_row = tb.Frame(self.left_bar, bootstyle="dark")
        first_row.pack(fill="x", side="top")
        for action in self.list_action[:3]:
            btn = tb.Button(first_row, text=action, bootstyle="dark", width=20, command=lambda index=self.list_action.index(action):self.nb_main_content.select(index))
            btn.pack(pady=3, fill="x")
        second_row = tb.Frame(self.left_bar, bootstyle="dark")
        second_row.pack(fill="x", side="bottom")
        for action in self.list_action[3:]:
            btn = tb.Button(second_row, text=action, bootstyle="info", width=20, command=lambda index=self.list_action.index(action):self.nb_main_content.select(index))
            btn.pack(pady=3, fill="x")

    # create main content
    def create_main_content(self):
        self.main_content = tb.Frame(self, bootstyle="dark")
        self.main_content.pack(fill="both", side="right", expand=True)
        self.nb_main_content = tb.Notebook(self.main_content, bootstyle="dark")
        self.nb_main_content.pack(fill="both", expand=True)
        # Create tab
        self.create_tab_projects()
        self.create_tab_tasks()
        self.create_tab_people()
        self.create_tab_files()
        self.create_tab_info()

    def overide_style(self):
        self.config(bootstyle="secondary")

    def create_tab_projects(self):
        tab_projects = tb.Frame(self.nb_main_content, bootstyle="dark")
        self.nb_main_content.add(tab_projects, text="Projects")
        '''PageProject(master: Frame, base_master: Self@CompBody, **kwargs)'''
        PageProject(tab_projects, self)

    def create_tab_tasks(self):
        tab_tasks = tb.Frame(self.nb_main_content, bootstyle="dark")
        self.nb_main_content.add(tab_tasks, text="Tasks")

    def create_tab_people(self):
        tab_people = tb.Frame(self.nb_main_content, bootstyle="dark")
        self.nb_main_content.add(tab_people, text="People")

    def create_tab_files(self):
        tab_files = tb.Frame(self.nb_main_content, bootstyle="dark")
        self.nb_main_content.add(tab_files, text="Files")

    def create_tab_info(self):
        tab_info = tb.Frame(self.nb_main_content, bootstyle="dark")
        self.nb_main_content.add(tab_info, text="Info")

    def get_table_fields(self, label: str):
        return list(filter(lambda x: x['label'] == label, self.table_fields))[0]