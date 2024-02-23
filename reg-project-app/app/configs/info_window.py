'''
    AUTH_UI_WINDOW: This is the authentication window's configuration.
    SRC: app/configs/info_window.py
    UI: AuthUI (app/layouts/auth_ui.py)
    LOGIC: 
        - PageLog (app/pages/auth_ui/page_log.py)
        - PageReg (app/pages/auth_ui/page_reg.py)
'''
AUTH_UI_WINDOW = {
    'title': 'Authentication',
    'themename': 'cyborg',
    'iconphoto': '',
    'size': (500, 900),
    'position': (400, 50),
    'resizable': (True, True),
}
# After authentification, the user will be redirected to the main window
'''
    MAIN_UI_WINDOW: This is the main window's configuration.
    SRC: app/configs/info_window.py
    UI: MainUI (app/layouts/main_ui.py)
    LOGIC: 
        - PageMain (app/pages/main_ui/page_main.py)
        - PageAccount (app/pages/main_ui/page_account.py)
        - PageStudent (app/pages/main_ui/page_student.py)
        - PageTeacher (app/pages/main_ui/page_teacher.py)
'''
MAIN_UI_WINDOW = {
    'title': 'Main Window',
    'iconphoto': '',
    'size': (1500, 800),
    'position': (300, 50),
    'resizable': (True, True),
}



