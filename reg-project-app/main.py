from app.layouts.main import main_ui
from app.db.setup import create_connections

if __name__ == '__main__':
    create_connections()
    main_ui()