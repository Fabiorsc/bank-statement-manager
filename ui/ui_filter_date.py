from datetime import date
import calendar

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QLabel,
    QPushButton,
    QDateEdit,
    QComboBox,
)

from domain.filters.filter_date import DateFilter


class UI_filter_date(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Filtro de Data")

        layout_principal = QVBoxLayout(self)

        # ============================================================
        # OPÇÕES
        # ============================================================

        self.rb_data_unica = QRadioButton("Data única")
        self.rb_mes = QRadioButton("Selecionar mês")
        self.rb_periodo = QRadioButton("Selecionar período")

        self.rb_data_unica.setChecked(True)

        self.grupo = QButtonGroup(self)

        self.grupo.addButton(self.rb_data_unica)
        self.grupo.addButton(self.rb_mes)
        self.grupo.addButton(self.rb_periodo)

        # ============================================================
        # DATA ÚNICA
        # ============================================================

        self.grp_data_unica = QGroupBox()

        layout_data = QHBoxLayout(self.grp_data_unica)

        layout_data.addWidget(QLabel("Data:"))

        self.edt_data = QDateEdit()
        self.edt_data.setCalendarPopup(True)
        self.edt_data.setDate(QDate.currentDate())

        layout_data.addWidget(self.edt_data)

        layout_principal.addWidget(self.rb_data_unica)
        layout_principal.addWidget(self.grp_data_unica)

        # ============================================================
        # MÊS
        # ============================================================

        self.grp_mes = QGroupBox()

        layout_mes = QHBoxLayout(self.grp_mes)

        layout_mes.addWidget(QLabel("Mês:"))

        self.cbo_mes = QComboBox()

        self.cbo_mes.addItems([
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ])

        layout_mes.addWidget(self.cbo_mes)

        layout_mes.addWidget(QLabel("Ano:"))

        self.cbo_ano = QComboBox()

        ano_atual = date.today().year

        for ano in range(
            ano_atual - 10,
            ano_atual + 11
        ):
            self.cbo_ano.addItem(str(ano))

        self.cbo_ano.setCurrentText(str(ano_atual))

        layout_mes.addWidget(self.cbo_ano)

        layout_principal.addWidget(self.rb_mes)
        layout_principal.addWidget(self.grp_mes)

        # ============================================================
        # PERÍODO
        # ============================================================

        self.grp_periodo = QGroupBox()

        layout_periodo = QHBoxLayout(self.grp_periodo)

        layout_periodo.addWidget(QLabel("De:"))

        self.edt_inicio = QDateEdit()
        self.edt_inicio.setCalendarPopup(True)
        self.edt_inicio.setDate(QDate.currentDate())

        layout_periodo.addWidget(self.edt_inicio)

        layout_periodo.addWidget(QLabel("Até:"))

        self.edt_fim = QDateEdit()
        self.edt_fim.setCalendarPopup(True)
        self.edt_fim.setDate(QDate.currentDate())

        layout_periodo.addWidget(self.edt_fim)

        layout_principal.addWidget(self.rb_periodo)
        layout_principal.addWidget(self.grp_periodo)

        # ============================================================
        # BOTÕES
        # ============================================================

        layout_botoes = QHBoxLayout()

        self.btn_confirmar = QPushButton("Confirmar")
        self.btn_cancelar = QPushButton("Cancelar")

        layout_botoes.addStretch()
        layout_botoes.addWidget(self.btn_confirmar)
        layout_botoes.addWidget(self.btn_cancelar)

        layout_principal.addLayout(layout_botoes)

        # ============================================================
        # EVENTOS
        # ============================================================

        self.rb_data_unica.toggled.connect(
            self.atualizar_estado_controles
        )

        self.rb_mes.toggled.connect(
            self.atualizar_estado_controles
        )

        self.rb_periodo.toggled.connect(
            self.atualizar_estado_controles
        )

        self.btn_confirmar.clicked.connect(
            self.confirmar
        )

        self.btn_cancelar.clicked.connect(
            self.close
        )

        self.atualizar_estado_controles()

    # ============================================================
    # HABILITA/DESABILITA CONTROLES
    # ============================================================

    def atualizar_estado_controles(self):

        self.grp_data_unica.setEnabled(
            self.rb_data_unica.isChecked()
        )

        self.grp_mes.setEnabled(
            self.rb_mes.isChecked()
        )

        self.grp_periodo.setEnabled(
            self.rb_periodo.isChecked()
        )

    # ============================================================
    # CONFIRMAR
    # ============================================================

    def confirmar(self):

        filtro = None

        # --------------------------------------------------------
        # DATA ÚNICA
        # --------------------------------------------------------

        if self.rb_data_unica.isChecked():

            filtro = DateFilter(
                mode=DateFilter.MODE_SINGLE,
                data=self.edt_data.date().toPython(),
            )

        # --------------------------------------------------------
        # MÊS
        #
        # Facilita a entrada.
        #
        # Internamente retorna RANGE.
        # --------------------------------------------------------

        elif self.rb_mes.isChecked():

            mes = self.cbo_mes.currentIndex() + 1

            ano = int(
                self.cbo_ano.currentText()
            )

            ultimo_dia = calendar.monthrange(
                ano,
                mes
            )[1]

            filtro = DateFilter(
                mode=DateFilter.MODE_RANGE,
                data_inicial=date(
                    ano,
                    mes,
                    1
                ),
                data_final=date(
                    ano,
                    mes,
                    ultimo_dia
                ),
            )

        # --------------------------------------------------------
        # PERÍODO
        # --------------------------------------------------------

        elif self.rb_periodo.isChecked():

            filtro = DateFilter(
                mode=DateFilter.MODE_RANGE,
                data_inicial=self.edt_inicio.date().toPython(),
                data_final=self.edt_fim.date().toPython(),
            )

        # ========================================================
        # FUTURO
        #
        # Aqui será devolvido para a UI_account_detail.
        #
        # Ex:
        #
        # self.callback(filtro)
        #
        # ou
        #
        # self.filter_created.emit(filtro)
        # ========================================================

        print(filtro.chip_text)

        self.close()

    # ============================================================
    # LOAD
    # ============================================================

    @classmethod
    def load(cls):

        cls._janela = cls()

        cls._janela.resize(450, 250)

        cls._janela.show()