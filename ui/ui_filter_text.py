from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)
from PySide6.QtCore import Signal
from domain.filters.filter_text import TextFilter


class UI_filter_text(QWidget):
    filter_created = Signal(object)
    """
    Configuração de filtro textual.

    REGRAS

    Um filtro textual possui:

        operador
            contém
            não contém

        vários valores

    Exemplo:

        operador = contém

        valores =
            mercado
            farmácia
            padaria

    Resultado:

        mercado OR farmácia OR padaria

    ------------------------------------------------------------

    IMPORTANTE

    Um filtro textual possui apenas UM operador.

    Não é permitido misturar:

        contém
        não contém

    na mesma configuração.

    Para isso o usuário deve criar outro filtro textual.

    ------------------------------------------------------------

    A lista self.values é a fonte da verdade.

    O grid é apenas visualização.

    Toda inclusão, remoção e atualização ocorre sobre:

        self.values

    e depois:

        refresh_grid()
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Filtro de Descrição")

        # ==========================================================
        # ESTADO
        # ==========================================================

        self.conditions = []

        self.current_operator = TextFilter.OP_CONTAINS

        self._changing_operator = False

        # ==========================================================
        # LAYOUT PRINCIPAL
        # ==========================================================

        layout_principal = QVBoxLayout(self)

        # ==========================================================
        # OPERADOR
        # ==========================================================

        layout_operador = QHBoxLayout()

        self.rb_contem = QRadioButton("Contém")
        self.rb_nao_contem = QRadioButton("Não contém")

        self.rb_contem.setChecked(True)

        self.group_operador = QButtonGroup(self)

        self.group_operador.addButton(self.rb_contem)
        self.group_operador.addButton(self.rb_nao_contem)

        layout_operador.addWidget(self.rb_contem)
        layout_operador.addWidget(self.rb_nao_contem)
        layout_operador.addStretch()

        layout_principal.addLayout(layout_operador)

        # ==========================================================
        # DESCRIÇÃO
        # ==========================================================

        layout_descricao = QHBoxLayout()

        layout_descricao.addWidget(
            QLabel("Descrição:")
        )

        self.cbo_descricao = QComboBox()

        self.cbo_descricao.setEditable(True)

        # ----------------------------------------------------------
        # FUTURO
        #
        # Ao digitar 3 caracteres ou mais:
        #
        # consultar banco
        #
        # SELECT DISTINCT descricao
        # WHERE descricao LIKE '%texto%'
        # LIMIT 25
        #
        # Quanto mais o usuário digita,
        # mais refinada fica a lista.
        #
        # Máximo:
        #     25 opções.
        # ----------------------------------------------------------

        layout_descricao.addWidget(
            self.cbo_descricao
        )

        layout_principal.addLayout(
            layout_descricao
        )

        # ==========================================================
        # BOTÃO ADICIONAR
        # ==========================================================

        self.btn_adicionar = QPushButton(
            "Adicionar"
        )

        layout_principal.addWidget(
            self.btn_adicionar
        )

        # ==========================================================
        # GRID
        # ==========================================================

        self.grid = QTableWidget()

        self.grid.setColumnCount(2)

        self.grid.setHorizontalHeaderLabels(
            [
                "Valor",
                "",
            ]
        )

        self.grid.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        self.grid.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        layout_principal.addWidget(
            self.grid
        )

        # ==========================================================
        # BOTÕES FINAIS
        # ==========================================================

        layout_botoes = QHBoxLayout()

        self.btn_confirmar = QPushButton(
            "Confirmar"
        )

        self.btn_cancelar = QPushButton(
            "Cancelar"
        )

        layout_botoes.addStretch()

        layout_botoes.addWidget(self.btn_confirmar)

        layout_botoes.addWidget(self.btn_cancelar)

        layout_principal.addLayout(layout_botoes)

        self.btn_confirmar.setDefault(True)
        self.btn_confirmar.setAutoDefault(True)

        self.btn_confirmar.setStyleSheet("""
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

        # ==========================================================
        # EVENTOS
        # ==========================================================

        self.rb_contem.toggled.connect(
            self.on_operator_changed
        )

        self.rb_nao_contem.toggled.connect(
            self.on_operator_changed
        )

        self.btn_adicionar.clicked.connect(
            self.adicionar
        )

        self.btn_confirmar.clicked.connect(
            self.confirmar
        )

        self.btn_cancelar.clicked.connect(
            self.close
        )

    # ==============================================================
    # OPERADOR
    # ==============================================================

    def on_operator_changed(self):

        if self._changing_operator:
            return

        novo_operador = (
            TextFilter.OP_CONTAINS
            if self.rb_contem.isChecked()
            else TextFilter.OP_NOT_CONTAINS
        )

        if novo_operador == self.current_operator:
            return

        # ----------------------------------------------------------
        # NÃO PERMITE ALTERAR SE JÁ EXISTEM ITENS
        # ----------------------------------------------------------

        if self.conditions:

            operador_atual = (
                "Contém"
                if self.current_operator
                == TextFilter.OP_CONTAINS
                else "Não contém"
            )

            operador_novo = (
                "Não contém"
                if self.current_operator
                == TextFilter.OP_CONTAINS
                else "Contém"
            )

            QMessageBox.information(
                self,
                "Operação não permitida",
                (
                    f'Os itens já cadastrados utilizam o operador '
                    f'"{operador_atual}".\n\n'
                    f'Para utilizar "{operador_novo}", '
                    f'crie uma nova configuração de texto.'
                )
            )

            self._changing_operator = True

            try:

                if (
                    self.current_operator
                    == TextFilter.OP_CONTAINS
                ):
                    self.rb_contem.setChecked(True)
                else:
                    self.rb_nao_contem.setChecked(True)

            finally:
                self._changing_operator = False

            return

        self.current_operator = novo_operador

    # ==============================================================
    # ADICIONAR
    # ==============================================================

    def adicionar(self):
        texto = (self.cbo_descricao.currentText().strip())

        if not texto:
            return

        if any(val_item == texto for _,val_item in self.conditions):
            QMessageBox.information(self,f"Aviso","Valor '{texto}' já adicionado.")
            return

        operador = (TextFilter.OP_CONTAINS if self.rb_contem.isChecked() else TextFilter.OP_NOT_CONTAINS)

        condicao = (operador, texto)
        self.conditions.append(condicao)

        self.refresh_grid()

        self.cbo_descricao.setCurrentText("")

    # ==============================================================
    # REMOVER
    # ==============================================================

    def remover(self, valor):

        resposta = QMessageBox.question(
            self,
            "Remover",
            f'Remover "{valor}"?'
        )

        if resposta != QMessageBox.Yes:
            return

        self.conditions.remove(valor)

        self.refresh_grid()

    # ==============================================================
    # GRID
    # ==============================================================

    def refresh_grid(self):

        self.grid.setRowCount(0)

        for operador, valor in self.conditions:

            row = self.grid.rowCount()

            self.grid.insertRow(row)

            texto = (f"Contém: {valor}" if operador == TextFilter.OP_CONTAINS else f"Não contém: {valor}")

            self.grid.setItem(
                row,
                0,
                QTableWidgetItem(texto)
            )

            btn_remover = QPushButton("X")

            btn_remover.clicked.connect(
                lambda _, c=(operador,valor):
                self.remover(c)
            )

            self.grid.setCellWidget(
                row,
                1,
                btn_remover
            )

    # ==============================================================
    # CONFIRMAR
    # ==============================================================

    def confirmar(self):

        if not self.conditions:

            QMessageBox.information(
                self,
                "Aviso",
                "Adicione ao menos um valor."
            )

            return

        # filtro = TextFilter(
        #     operator=self.current_operator,
        #     values=self.conditions.copy()
        # )
        
        filtro = TextFilter(conditions=self.conditions.copy())

        # ----------------------------------------------------------
        # FUTURO
        #
        # Retornar filtro para
        # UI_account_detail.
        #
        # Ex:
        #
        # self.callback(filtro)
        #
        # ou
        #
        # self.filter_created.emit(filtro)
        # ----------------------------------------------------------

        # print(filtro.chip_text)
        self.filter_created.emit(filtro)
        self.close()

    # ==============================================================
    # LOAD
    # ==============================================================

    @classmethod
    def load(cls):
        cls._janela = cls()
        cls._janela.resize( 600, 450)
        cls._janela.show()
        return cls._janela

        