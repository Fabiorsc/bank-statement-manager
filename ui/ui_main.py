import sys

from PySide6.QtWidgets import (
    QApplication, QScrollArea, QWidget, QVBoxLayout,
    QMainWindow
)
from PySide6.QtCore import Qt

from database.tables.conta import listar_contas
from ui.ui_import import UI_import
from ui.components.ui_account_item import UI_AccountItem
from ui.ui_account_manager import UI_account_manager
from ui.ui_account_layout import UI_account_layout

class UI_main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bank Statement Manager")

# ---------- CENTRAL WIDGET ----------
        # Obrigatório par ao usu de QMainWindow! Todo Windows precisa contaer um Widget central para conter os Layouts!
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

# ---------- MENU ----------
        menubar = self.menuBar()

        menu_conta = menubar.addMenu("Conta")

        acao_inserir = menu_conta.addAction("Inserir Conta")
        acao_inserir.triggered.connect(self.inserir_conta)

# ---------- CONTAINER DAS CONTAS ----------
        self.container = QWidget()
        self.layout_contas = QVBoxLayout(self.container)

        # 🔒 trava itens no topo
        self.layout_contas.setAlignment(Qt.AlignTop)

        # 🔒 remove distribuição vertical automática
        self.layout_contas.setSpacing(10)
        self.layout_contas.setContentsMargins(0, 0, 0, 0)

# ---------- CRIA ITENS ----------
        contas = listar_contas()
        for id_conta, banco, ag, conta, apelido in contas:
            item = UI_AccountItem(id_conta, apelido, banco, ag, conta)

            item.btn_importar.clicked.connect(
                lambda _, id=id_conta, b=banco, a=ag, c=conta, ap=apelido: self.importar(id, b, a, c,ap)
            )

            item.btn_detalhes.clicked.connect(
                lambda _, id=id_conta, b=banco, a=ag, c=conta, ap=apelido: self.detalhes(id, b, a, c,ap)
            )
            self.layout_contas.addWidget(item)

# ---------- SCROLL ----------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)

        layout.addWidget(scroll)

# ---------- AÇÕES ----------

    def importar(self, id, banco, ag, conta, apelido):
        # self.janela_importa = UI_select_file()
        # self.janela_importa.show()
        UI_import.load(id, apelido, banco, ag, conta)

        print(f"Importar -> {id} / {banco} / {ag} / {conta}")

    def detalhes(self, id, banco, ag, conta, apelido):
        UI_account_layout.load(id)

        print(f"Detalhes -> {id} / {banco} / {ag} / {conta}")

    def inserir_conta(self):
        self.janela_contas = UI_account_manager()
        self.janela_contas.show()

# ---------- LOAD ----------

    @classmethod
    def load(cls):
        cls._janela = cls()
        cls._janela.resize(800, 400)
        cls._janela.show()
