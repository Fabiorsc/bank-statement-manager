import sys
from database.repositories import RepositoryAccountLayout
from domain.account_layout_type import AccountLayoutType
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QComboBox
)


class UI_account_layout(QWidget):

    def __init__(self, conta_id):
        super().__init__()

        layout_tipo=""
        linha_header=""
        col_data=""
        col_descricao=""
        col_valor=""
        col_credito=""
        col_debito=""
        col_indicador=""
        
        self.conta_id = conta_id

        layout=RepositoryAccountLayout.get_conta_layout(conta_id)
        if layout:
            #  _, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador=layout
            layout_tipo = layout["layout_tipo"]
            linha_header = layout["linha_header"]
            col_data = layout["col_data"]
            col_descricao = layout["col_descricao"]
            col_valor = layout["col_valor"]
            col_credito = layout["col_credito"]
            col_debito = layout["col_debito"]
            col_indicador = layout["col_indicador"]

        self.setWindowTitle("Configuração de Layout")

        # CAMPOS
        # self.txt_conta_id = QLineEdit(str(conta_id))
        # self.txt_conta_id.setReadOnly(True)
        # self.txt_conta_id=conta_id

        self.cmb_layout_tipo = QComboBox()
        self.cmb_layout_tipo.addItems([
            AccountLayoutType.VALOR_UNICO.value,
            AccountLayoutType.CRED_DEB.value,
            AccountLayoutType.VALOR_IND.value
        ])
        # Define valor selecionado
        self.cmb_layout_tipo.setCurrentText(layout_tipo)

        self.txt_linha_header = QLineEdit(str(linha_header))

        self.txt_col_data = QLineEdit(col_data)
        self.txt_col_descricao = QLineEdit(col_descricao)

        self.txt_col_valor = QLineEdit(col_valor)

        self.txt_col_credito = QLineEdit(col_credito)
        self.txt_col_debito = QLineEdit(col_debito)

        self.txt_col_indicador = QLineEdit(col_indicador)

        # FORM
        form = QFormLayout()

        # form.addRow("Conta ID:", self.txt_conta_id)
        form.addRow("Layout Tipo:", self.cmb_layout_tipo)

        form.addRow("Linha Header:", self.txt_linha_header)

        form.addRow("Coluna Data:", self.txt_col_data)
        form.addRow("Coluna Descrição:", self.txt_col_descricao)

        form.addRow("Coluna Valor:", self.txt_col_valor)

        form.addRow("Coluna Crédito:", self.txt_col_credito)
        form.addRow("Coluna Débito:", self.txt_col_debito)

        form.addRow("Coluna Indicador:", self.txt_col_indicador)

        # BOTÕES
        self.btn_salvar = QPushButton("Salvar / Atualizar")
        self.btn_cancelar = QPushButton("Cancelar")

        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        layout_botoes.addWidget(self.btn_cancelar)
        layout_botoes.addWidget(self.btn_salvar)

        # LAYOUT PRINCIPAL
        layout_principal = QVBoxLayout()

        layout_principal.addLayout(form)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)

        # EVENTOS
        self.cmb_layout_tipo.currentTextChanged.connect(
            self.update_fields
        )

        self.update_fields()

    # ==========================================================
    # UPDATE FIELDS
    def update_fields(self):

        layout = self.cmb_layout_tipo.currentText()

        # limpa obrigatoriedade visual
        self.enable_all()

        if layout == AccountLayoutType.VALOR_UNICO.value:

            self.txt_col_valor.setEnabled(True)

            self.txt_col_credito.setEnabled(False)
            self.txt_col_debito.setEnabled(False)
            self.txt_col_indicador.setEnabled(False)

            self.txt_col_credito.clear()
            self.txt_col_debito.clear()
            self.txt_col_indicador.clear()

        elif layout == AccountLayoutType.CRED_DEB.value:

            self.txt_col_credito.setEnabled(True)
            self.txt_col_debito.setEnabled(True)

            self.txt_col_valor.setEnabled(False)
            self.txt_col_indicador.setEnabled(False)

            self.txt_col_valor.clear()
            self.txt_col_indicador.clear()

        elif layout == AccountLayoutType.VALOR_IND.value:

            self.txt_col_valor.setEnabled(True)
            self.txt_col_indicador.setEnabled(True)

            self.txt_col_credito.setEnabled(False)
            self.txt_col_debito.setEnabled(False)

            self.txt_col_credito.clear()
            self.txt_col_debito.clear()

    # ==========================================================
    # ENABLE ALL
    def enable_all(self):

        self.txt_col_valor.setEnabled(True)

        self.txt_col_credito.setEnabled(True)
        self.txt_col_debito.setEnabled(True)

        self.txt_col_indicador.setEnabled(True)

    # ==========================================================
    # VALIDAR
    def validar(self):

        if not self.txt_linha_header.text().strip():
            return "Linha Header é obrigatório."

        if not self.txt_col_data.text().strip():
            return "Coluna Data é obrigatório."

        if not self.txt_col_descricao.text().strip():
            return "Coluna Descrição é obrigatório."

        layout = self.cmb_layout_tipo.currentText()

        # VALOR ÚNICO
        if layout == AccountLayoutType.VALOR_UNICO.value:

            if not self.txt_col_valor.text().strip():
                return "Coluna Valor é obrigatório."

        # CRÉDITO / DÉBITO
        elif layout == AccountLayoutType.CRED_DEB.value:

            if not self.txt_col_credito.text().strip():
                return "Coluna Crédito é obrigatório."

            if not self.txt_col_debito.text().strip():
                return "Coluna Débito é obrigatório."

        # VALOR + INDICADOR
        elif layout == AccountLayoutType.VALOR_IND.value:

            if not self.txt_col_valor.text().strip():
                return "Coluna Valor é obrigatório."

            if not self.txt_col_indicador.text().strip():
                return "Coluna Indicador é obrigatório."

        return None

    # ==========================================================
    # SALVAR
    def salvar(self):

        erro = self.validar()

        if erro:
            QMessageBox.warning(
                self,
                "Erro",
                erro
            )
            return

        RepositoryAccountLayout.inserir_conta_layout(
            self.conta_id,
            self.cmb_layout_tipo.currentText(),
            self.txt_linha_header.text(),
            self.txt_col_data.text(),
            self.txt_col_descricao.text(),
            self.txt_col_valor.text(),
            self.txt_col_credito.text(),
            self.txt_col_debito.text(),
            self.txt_col_indicador.text(),
        )

        dados = {
            "conta_id": self.conta_id,
            "layout_tipo": self.cmb_layout_tipo.currentText(),
            "linha_header": self.txt_linha_header.text(),

            "col_data": self.txt_col_data.text(),
            "col_descricao": self.txt_col_descricao.text(),

            "col_valor": self.txt_col_valor.text(),

            "col_credito": self.txt_col_credito.text(),
            "col_debito": self.txt_col_debito.text(),

            "col_indicador": self.txt_col_indicador.text(),
        }

        print(dados)

        QMessageBox.information(
            self,
            "Sucesso",
            "Configuração salva."
        )

        self.close()

    # ==========================================================
    # CANCELAR
    def cancelar(self):
        self.close()

    # ==========================================================
    # LOAD
    @classmethod
    def load(cls, conta_id):
        cls._janela = cls(conta_id)
        cls._janela.resize(500, 350)
        cls._janela.show()
        return cls._janela

