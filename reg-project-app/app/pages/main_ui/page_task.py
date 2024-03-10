import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from app.utils.main import TableUtil
from app.db.main import GroupDao, Group




class PageTask(tb.Panedwindow):
    def __init__(self, master, base_master, **kwargs):
        super().__init__(master, **kwargs, bootstyle="info", orient="horizontal")
        self.master = master
        self.base_master = base_master
        #----------------------------------------
        # DAO
        self.group_dao = GroupDao()
        # Variables
        self.table_data = self.get_table_data()
        #----------------------------------------
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.overide_style()

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
        
        
    def implemenet_frame_right(self):
        self.srcoll_frame_right = ScrolledFrame(self.frame_right, bootstyle="dark")
        self.srcoll_frame_right.pack(fill="both", expand=True)
        self.create_table()


    def overide_style(self):
        ...

    def get_table_data(self):
        return {
            "columns": ["id", "name", "number_register"],
            "rows": self.get_data_group()
        }
    
    def get_data_group(self):
        return [
            (
                group.id,
                group.name,
                len(group.accounts)
            ) for group in self.group_dao.get_all()
        ]
    
    def create_table(self):
        # Create Label Frame
        self.lbl_frame = tb.LabelFrame(self.srcoll_frame_right, text="Danh sách nhóm", width=500,height=350, padding=10)
        self.lbl_frame.pack(fill="x", side="top", padx=5, pady=5)
        # Build Table
        self.base_master.table_fields[1]["widget"] = TableUtil.initialize_table(self.base_master.table_fields[1]["widget"], self.lbl_frame, data=self.table_data)
        # Add Event for Table
        self.base_master.table_fields[1]["widget"].bind_all("<<TreeviewSelect>>", self.on_select_table)

    def on_select_table(self, event):
        pass