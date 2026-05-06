import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QScrollArea, QMainWindow
)

from ui.components.ui_account_crud_list import UI_AccountCrudList
from database.tables.conta import inserir_conta, listar_contas


class UI_account_manager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerência de Contas")

        # --- CENTRAL WIDGET (obrigatório no QMainWindow) ---
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)

# ---------- FORMULÁRIO ----------
        form_layout = QHBoxLayout()

        self.input_apelido = QLineEdit()
        self.input_apelido.setPlaceholderText("Apelido")

        self.input_banco = QLineEdit()
        self.input_banco.setPlaceholderText("Banco")

        self.input_agencia = QLineEdit()
        self.input_agencia.setPlaceholderText("Agência")

        self.input_conta = QLineEdit()
        self.input_conta.setPlaceholderText("Conta")

        self.btn_criar = QPushButton("Criar")
        self.btn_criar.clicked.connect(self.criar_conta)

        form_layout.addWidget(self.input_apelido)
        form_layout.addWidget(self.input_banco)
        form_layout.addWidget(self.input_agencia)
        form_layout.addWidget(self.input_conta)
        form_layout.addWidget(self.btn_criar)

        layout_principal.addLayout(form_layout)

# ---------- LISTA (SCROLL) ----------
        self.container = QWidget()
        self.layout_contas = QVBoxLayout(self.container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)

        layout_principal.addWidget(scroll)

# ---------- CARREGAR DADOS ----------
        self.carregar_contas()

# ---------- MÉTODOS ----------

    def carregar_contas(self):
        # limpa layout
        for i in reversed(range(self.layout_contas.count())):
            widget = self.layout_contas.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        contas = listar_contas()

        for id_conta, banco, agencia, conta, apelido in contas:
            item = UI_AccountCrudList(id_conta, apelido, banco, agencia, conta)

            # conectar botões
            item.btn_remover.clicked.connect(
                lambda _, id=id_conta: self.remover_conta(id)
            )

            item.btn_editar.clicked.connect(
                lambda _, id=id_conta: self.editar_conta(id)
            )

            self.layout_contas.addWidget(item)

    def criar_conta(self):
        apelido = self.input_apelido.text()
        banco = self.input_banco.text()
        agencia = self.input_agencia.text()
        conta = self.input_conta.text()

        if not apelido or not banco:
            print("Apelido e Banco são obrigatórios")
            return

        inserir_conta(banco, agencia, conta, apelido)

        self.limpar_inputs()
        self.carregar_contas()

    def limpar_inputs(self):
        self.input_apelido.clear()
        self.input_banco.clear()
        self.input_agencia.clear()
        self.input_conta.clear()

    def remover_conta(self, id_conta):
        print(f"Remover conta ID: {id_conta}")
        # próximo passo: implementar delete no banco
        # depois:
        # self.carregar_contas()

    def editar_conta(self, id_conta):
        print(f"Editar conta ID: {id_conta}")
        # próximo passo: tela de edição

# ---------- LOAD ----------

    @classmethod
    def load(cls):
        # app = QApplication(sys.argv)
        janela = cls()
        janela.resize(900, 500)
        janela.show()
        # app.exec()