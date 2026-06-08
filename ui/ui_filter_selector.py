from ui.ui_filter_date import UI_filter_date
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)


class UI_filter_selector(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adicionar Filtro")

        layout = QVBoxLayout(self)

        self.btn_data = QPushButton("DATA")
        self.btn_descricao = QPushButton("DESCRIÇÃO")
        self.btn_valor = QPushButton("VALOR")

        layout.addWidget(self.btn_data)
        layout.addWidget(self.btn_descricao)
        layout.addWidget(self.btn_valor)

        self.btn_data.clicked.connect(self.abrir_data)
        self.btn_descricao.clicked.connect(self.abrir_descricao)
        self.btn_valor.clicked.connect(self.abrir_valor)

    # ----------------------------------------------------
    # AÇÕES
    # ----------------------------------------------------

    def abrir_data(self):

        # FUTURO:
        # abrir UI_filter_date
        UI_filter_date.load()

        print("Abrir filtro DATA")

    def abrir_descricao(self):

        # FUTURO:
        # abrir UI_filter_text

        print("Abrir filtro DESCRIÇÃO")

    def abrir_valor(self):

        # FUTURO:
        # abrir UI_filter_money

        print("Abrir filtro VALOR")

    # ----------------------------------------------------
    # LOAD
    # ----------------------------------------------------

    @classmethod
    def load(cls):
        cls._janela = cls()
        cls._janela.resize(300, 200)
        cls._janela.show()