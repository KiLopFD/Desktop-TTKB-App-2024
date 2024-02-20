from app.layouts.main import main_ui
from app.db.setup import create_conections

if __name__ == '__main__':
    create_conections()
    main_ui()