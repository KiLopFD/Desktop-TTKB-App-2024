from src.ui.export_module import tb
from src.ui.styles.style_window import STYLE_WINDOW


origin_window = tb.Window(**STYLE_WINDOW)

BASE_THEME = origin_window.style.theme_names()