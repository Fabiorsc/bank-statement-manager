import sys
from PySide6.QtWidgets import QApplication

from ui.ui_main import UI_main
# from openpyxl import load_workbook
from database.schema import criar_tabelas, remover_tabelas
from infra.logging_config import configure_logging
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # window = UI_main()
    # UI_main.load
    # window

    configure_logging()

    logger.info("Sistema iniciado")
    # remover_tabelas()
    criar_tabelas()
    app = QApplication(sys.argv)
    UI_main.load()
    app.exec()
    logger.info("Sistema encerrado")
    