from decimal import Decimal, InvalidOperation
from PySide6.QtCore import Signal
from domain.filters.filter_money import MoneyFilter
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)


class UI_filter_money(QWidget):
    filter_created = Signal(object)
    """
    Filtro monetário.

    REGRAS

    Um filtro monetário pode possuir
    uma ou mais condições.

    Exemplos:

        > 100

        < 500

        = 300

    Internamente:

        valor > 100
        OR
        valor < 500
        OR
        valor = 300

    IMPORTANTE

    Não existe operador faixa.

    Faixas são obtidas por combinação
    de filtros diferentes.

    Exemplo:

        valor > 100
        AND
        valor < 500
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Filtro de Valor")

        # =====================================================
        # FONTE DA VERDADE
        # =====================================================

        self.conditions = []

        # =====================================================
        # LAYOUT PRINCIPAL
        # =====================================================

        layout_principal = QVBoxLayout(self)

        # =====================================================
        # OPERADOR
        # =====================================================

        layout_operador = QHBoxLayout()

        layout_operador.addWidget(
            QLabel("Operador:")
        )

        self.cbo_operador = QComboBox()

        self.cbo_operador.addItems(
            [
                "=",
                ">",
                ">=",
                "<",
                "<=",
            ]
        )

        layout_operador.addWidget(
            self.cbo_operador
        )

        layout_operador.addStretch()

        layout_principal.addLayout(
            layout_operador
        )

        # =====================================================
        # VALOR
        # =====================================================

        layout_valor = QHBoxLayout()

        layout_valor.addWidget(
            QLabel("Valor:")
        )

        self.edt_valor = QLineEdit()

        layout_valor.addWidget(
            self.edt_valor
        )

        layout_principal.addLayout(
            layout_valor
        )

        # =====================================================
        # ADICIONAR
        # =====================================================

        self.btn_adicionar = QPushButton(
            "Adicionar"
        )

        layout_principal.addWidget(
            self.btn_adicionar
        )

        # =====================================================
        # GRID
        # =====================================================

        self.grid = QTableWidget()

        self.grid.setColumnCount(3)

        self.grid.setHorizontalHeaderLabels(
            [
                "Operador",
                "Valor",
                "",
            ]
        )

        self.grid.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        self.grid.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.grid.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        layout_principal.addWidget(
            self.grid
        )

        # =====================================================
        # BOTÕES FINAIS
        # =====================================================

        layout_botoes = QHBoxLayout()

        self.btn_confirmar = QPushButton(
            "Confirmar"
        )

        self.btn_cancelar = QPushButton(
            "Cancelar"
        )

        layout_botoes.addStretch()

        layout_botoes.addWidget(
            self.btn_confirmar
        )

        layout_botoes.addWidget(
            self.btn_cancelar
        )

        layout_principal.addLayout(
            layout_botoes
        )

        # =====================================================
        # EVENTOS
        # =====================================================

        self.btn_adicionar.clicked.connect(
            self.adicionar
        )

        self.btn_confirmar.clicked.connect(
            self.confirmar
        )

        self.btn_cancelar.clicked.connect(
            self.close
        )

    # =====================================================
    # ADICIONAR
    # =====================================================

    def adicionar(self):

        texto_valor = (self.edt_valor.text().strip().replace(",", "."))

        if not texto_valor:
            QMessageBox.information(self, "Aviso", "Informe um valor.")
            return

        try:
            valor = Decimal(texto_valor)

        except InvalidOperation:
            QMessageBox.information(self, "Aviso", "Valor inválido." )
            return

        operador = (self.cbo_operador.currentText())
        condicao = (operador, valor)

        if condicao in self.conditions:
            QMessageBox.information(self, "Aviso", "Condição já adicionada.")
            return

        self.conditions.append(condicao)

        self.refresh_grid()

        self.edt_valor.clear()

        self.edt_valor.setFocus()

    # =====================================================
    # REMOVER
    # =====================================================

    def remover(self, condicao):

        operador, valor = condicao

        resposta = QMessageBox.question(
            self,
            "Remover",
            f'Remover "{operador} {valor}"?'
        )

        if resposta != QMessageBox.Yes:
            return

        self.conditions.remove(
            condicao
        )

        self.refresh_grid()

    # =====================================================
    # GRID
    # =====================================================

    def refresh_grid(self):

        self.grid.setRowCount(0)

        for operador, valor in self.conditions:

            row = self.grid.rowCount()

            self.grid.insertRow(row)

            self.grid.setItem(
                row,
                0,
                QTableWidgetItem(operador)
            )

            self.grid.setItem(
                row,
                1,
                QTableWidgetItem(str(valor))
            )

            btn_remover = QPushButton("X")

            btn_remover.clicked.connect(
                lambda _, c=(operador, valor):
                self.remover(c)
            )

            self.grid.setCellWidget(
                row,
                2,
                btn_remover
            )

    # =====================================================
    # CONFIRMAR
    # =====================================================

    def confirmar(self):

        # if not self.conditions:
        #     QMessageBox.information(
        #         self,
        #         "Aviso",
        #         "Adicione ao menos uma condição."
        #     )
        #     return
        # else:


        #     filtro = MoneyFilter(
        #         # mode=MoneyFilter.MODE_RANGE,
        #         operator=self.cbo_operador().value   #.edt_inicio.date().toPython(),
        #         data_final=self.edt_valor().value  #.edt_fim.date().toPython(),
        #     )




        # -------------------------------------------------
        # FUTURO
        #
        # Criar MoneyFilter
        #
        # Exemplo:
        #
        # MoneyFilter(
        #     conditions=self.conditions.copy()
        # )
        #
        # Retornar para a
        # UI_account_detail.
        # -------------------------------------------------

        if not self.conditions:
            QMessageBox.information(self, "Aviso", "Adicione ao menos uma condição.")
            return

        filtro = MoneyFilter(conditions=self.conditions.copy())

        # print(self.conditions)
        self.filter_created.emit(filtro)
        self.close()

    # =====================================================
    # LOAD
    # =====================================================

    @classmethod
    def load(cls):
        cls._janela = cls()
        cls._janela.resize( 600,450)
        cls._janela.show()
        return cls._janela