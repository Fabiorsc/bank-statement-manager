from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget
)

from ui.ui_table_manager import UI_table_manager


class UI_table_selector(QMainWindow):
    TABLES = [
        "contas",
        "conta_layout",
        "import",
        "transacoes",
    ]

    # TABLES = [
    #     "account",
    #     "account_layout",
    #     "import",
    #     "transaction",
    # ]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabelas")

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.lista = QListWidget()

        for tabela in self.TABLES:
            self.lista.addItem(tabela)

        self.lista.itemDoubleClicked.connect(
            self.abrir_tabela
        )

        layout.addWidget(self.lista)

    def abrir_tabela(self, item):
        nome_tabela = item.text()

        # print(f"Abrir tabela: {nome_tabela}")
        UI_table_manager.load(nome_tabela)


    @classmethod
    def load(cls):
        cls._janela = cls()
        cls._janela.resize(400, 500)
        cls._janela.show()
        return cls._janela