import sys
from config import check_config, set_app_style
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__' :
    check_config()
    app = QApplication(sys.argv)
    set_app_style(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())