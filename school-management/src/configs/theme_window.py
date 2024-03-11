import ttkbootstrap as tb

'''
 title: str = "ttkbootstrap",
    themename: str = "litera",
    iconphoto: str = '',
    size: Any | None = None,
    position: Any | None = None,
    minsize: Any | None = None,
    maxsize: Any | None = None,
    resizable: Any | None = None,
    hdpi: bool = True,
    scaling: Any | None = None,
    transient: Any | None = None,
'''


config_window = {
    "title": "School Management System",
    "themename": "litera",
    "position": (100, 100),
    "resizable": (True, True),
    "size": (1700, 800),
}


edit_window = {
    "title": "Edit",
    "position": (100, 200),
    "resizable": (True, True),
    "size": (500, 900),
}

window = tb.Window(**config_window)