
from PySide6.QtWidgets import (
    QSizePolicy, QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

class UI_AccountItem(QWidget):
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
        self.label_apelido = QLabel(apelido)
        self.label_banco = QLabel(f"Banco: {banco}")
        self.label_agencia = QLabel(f"Agência: {agencia}")
        self.label_conta = QLabel(f"Conta: {conta}")

        # Botões
        # self.btn_importar = QPushButton("Importar")
        # self.btn_detalhes = QPushButton("Detalhes")

        # Botão Hamburger
        self.btn_menu = QPushButton("☰")
        self.btn_menu.clicked.connect(self.show_menu)

        # Menu Hamburger
        self.action_importar = QAction("Importar Extrato", self)
        self.action_pesquisa = QAction("Pesquisa", self)
        self.action_layout = QAction("Configurar Layout", self)

    # --- LAYOUT
    def _create_layout(self):
        # Info (linha)
        layout_info = QHBoxLayout()
        layout_info.addWidget(self.label_banco)
        layout_info.addWidget(self.label_agencia)
        layout_info.addWidget(self.label_conta)

        # Esquerda
        layout_esquerda = QVBoxLayout()
        layout_esquerda.addWidget(self.label_apelido)
        layout_esquerda.addLayout(layout_info)
        layout_esquerda.addStretch()

        # # Botões (direita)
        # layout_botoes = QVBoxLayout()
        # # layout_botoes.addWidget(self.btn_importar)
        # # layout_botoes.addWidget(self.btn_detalhes)
        # layout_botoes.addWidget(self.btn_menu)
        # layout_botoes.addStretch()

        # Botões (direita)
        layout_botoes = QVBoxLayout()
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.btn_menu, alignment=Qt.AlignHCenter)
        layout_botoes.addStretch()

        # Principal
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(layout_esquerda, 3)
        layout_principal.addLayout(layout_botoes, 1)

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

        # self.btn_menu.setStyleSheet("""
        #         background-color: #f9f9f9;
        #         border: 1px solid #ccc;
        #         border-radius: 6px;
        #         padding: 8px;
        # """)

        self.btn_menu.setStyleSheet("""
            QPushButton {
                background-color: #f9f9f9;
                color: #000000;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
        """)




        self.label_apelido.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )

    # ---  CONFIG
    def _configure(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.adjustSize()

    def show_menu(self):
        menu = QMenu(self)

        menu.addAction(self.action_importar)
        menu.addAction(self.action_pesquisa)
        menu.addAction(self.action_layout)

        menu.exec(
            self.btn_menu.mapToGlobal(
                self.btn_menu.rect().bottomLeft()
            )
        )


            

# class UI_AccountItem(QWidget):
#     def __init__(self, id_conta, apelido, banco, agencia, conta):
#         super().__init__()
# # --- VIEW
#         # --- Dados ---
#         self.id_conta = id_conta

#         # --- INFO CONTA ---
#         self.label_apelido = QLabel(apelido)
#         self.label_banco = QLabel(f"Banco: {banco}")
#         self.label_agencia = QLabel(f"Agência: {agencia}")
#         self.label_conta = QLabel(f"Conta: {conta}")

#         # --- BOTÕES ---
#         self.btn_importar = QPushButton("Importar")
#         self.btn_detalhes = QPushButton("Detalhes")







#         # --- LAYOUT INFO (dados) ---
#         layout_info = QHBoxLayout()
#         layout_info.addWidget(self.label_banco)
#         layout_info.addWidget(self.label_agencia)
#         layout_info.addWidget(self.label_conta)
  
#         # --- LAYOUT ESQUERDO (apelido + dados) ---
#         layout_esquerda = QVBoxLayout()
#         layout_esquerda.addWidget(self.label_apelido)
#         layout_esquerda.addLayout(layout_info)
#         layout_esquerda.addStretch()

#         # --- BOTÕES (direita) ---
#         layout_botoes = QVBoxLayout()
#         layout_botoes.addWidget(self.btn_importar)
#         layout_botoes.addWidget(self.btn_detalhes)
#         layout_botoes.addStretch()

#         # --- LAYOUT PRINCIPAL ---
#         layout_principal = QHBoxLayout()
#         layout_principal.addLayout(layout_esquerda, 3)
#         layout_principal.addLayout(layout_botoes, 1)



#          # --- CONTAINER COM ESTILO ---
#         # container = QWidget()
#         self.setObjectName("card")

#         # FORÇA PINTURA DO BACKGROUND
#         self.setAttribute(Qt.WA_StyledBackground, True)

#         # container.setLayout(layout_principal)
#         self.setStyleSheet("""
#             QWidget#card{
#             background-color: #f9f9f9;
#             border: 1px solid #ccc;
#             border-radius: 6px;
#             padding: 8px;
#             }
#         """)

   
#         # --- APELIDO (estilo opcional) ---
#         self.label_apelido.setStyleSheet("font-weight: bold; font-size: 14px;")

#         self.setLayout(layout_principal)
#         # self.setLayout(layout_externo)

#         # TRAVA ALTURA NO TAMANHO DO CONTEÚDO
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

#         # força o Qt a respeitar o tamanho ideal calculado
#         self.adjustSize()