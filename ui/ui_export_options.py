from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)


class UI_export_options(QDialog):

    export_requested = Signal(bool, bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Opções de Exportação")
        self.setModal(True)

        # OPÇÕES DE EXPORTAÇÃO
        self.chk_sumarizar_dia = QCheckBox("SUMARIZAR POR DIA")
        self.chk_sumarizar_entrada = QCheckBox("SUMARIZAR POR ENTRADA")

        # BOTÕES
        self.btn_exportar = QPushButton("Exportar")
        self.btn_cancelar = QPushButton("Cancelar")

        self.btn_exportar.clicked.connect(self.exportar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        self.btn_exportar.setDefault(True)
        self.btn_exportar.setAutoDefault(True)

        self.btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border: 1px solid #1D4ED8;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                padding: 6px 16px;
            }
        """)


        # LAYOUT DOS BOTÕES
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.btn_exportar)
        layout_botoes.addWidget(self.btn_cancelar)

        # LAYOUT PRINCIPAL
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.chk_sumarizar_dia)
        layout_principal.addWidget(self.chk_sumarizar_entrada)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)

    def exportar(self):
        self.export_requested.emit(
            self.chk_sumarizar_dia.isChecked(),
            self.chk_sumarizar_entrada.isChecked()
        )
        self.accept()

    def cancelar(self):
        self.reject()
