import sys
from PySide6.QtWidgets import QApplication

from ui.ui_main import UI_main
from openpyxl import load_workbook
from database.schema import criar_tabelas

if __name__ == "__main__":
    # window = UI_main()
    # UI_main.load
    # window

    criar_tabelas()
    app = QApplication(sys.argv)
    UI_main.load()
    app.exec()
    