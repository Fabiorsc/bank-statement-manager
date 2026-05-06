
from PySide6.QtWidgets import (
    QSizePolicy, QWidget, QLabel, QPushButton, 
    QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt

class UI_AccountCrudList(QWidget):
    def __init__(self, id_conta, apelido, banco, agencia, conta):
        super().__init__()

        # --- DATA ---
        self.id_conta = id_conta

        # --- BUILD ---
        self._create_widgets(apelido, banco, agencia, conta)
        self._create_layout()
        self._apply_style()
        self._configure()


    # --- VIEW
    def _create_widgets(self, apelido, banco, agencia, conta):
        # Labels
        self.lbl_apelido = QLabel(apelido)
        self.lbl_banco = QLabel(f"Banoc: {banco}")
        self.lbl_agencia = QLabel(f"Agência: {agencia}")
        self.lbl_conta = QLabel(f"Conta: {conta}")
        
        # Botões
        self.btn_editar = QPushButton("Editar")
        self.btn_remover = QPushButton("Remover")

    # --- LAYOUT
    def _create_layout(self):

        # Info (linha)
        layout_dados = QHBoxLayout()
        layout_dados.addWidget(self.lbl_apelido)
        layout_dados.addWidget(self.lbl_banco)
        layout_dados.addWidget(self.lbl_agencia)
        layout_dados.addWidget(self.lbl_conta)
        layout_dados.addStretch()

        # Botôes (ações)
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.btn_editar)
        layout_botoes.addWidget(self.btn_remover)
        # layout_botoes.addStretch()

        # Principal
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_dados)
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)


    # --- STYLE
    def _apply_style(self):
        self.setObjectName("card")

        # força pintura
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget#card {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        self.btn_editar.setStyleSheet("""
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px;                             
        """)

        self.btn_remover.setStyleSheet("""
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px;
        """)

        # self.setStyleSheet("""
        #     QWidget#card {
        #         background-color: #f9f9f9;
        #         border: 1px solid #ccc;
        #         border-radius: 6px;
        #         padding: 8px;
        #     }
        # """)

        self.lbl_apelido.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )

    # ---  CONFIG
    def _configure(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.adjustSize()


