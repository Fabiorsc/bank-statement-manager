from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QMenu,
    QMessageBox,
)
from PySide6.QtCore import Qt

from database.repositories import RepositoryAccount
from ui.ui_filter_date import UI_filter_date
from ui.ui_filter_text import UI_filter_text
from ui.ui_filter_money import UI_filter_money
# from ui.ui_filter_selector import UI_filter_selector
from ui.ui_filter_chip import UI_filter_chip
from database.repositories import RepositoryTransaction
from domain.formatters import format_money
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHeaderView
from excel.excel_export import ExcelExport


class UI_account_detail(QWidget):
    """
    Tela de pesquisa sobre um conta.

    1) Exibir os dados principais da conta.
    2) Permitir filtros através de chips.
    3) Exibir os lançamentos encontrados.
    4) Exibir um resumo dos resultados filtrados.
    5) Exportar resultado para Excel.
    ----------------------------------------------------------------
    """

    def __init__(self, id_conta):
        super().__init__()

        self.id_conta = id_conta

        # define lista de filtros vazia para ser preenchida conforme o usuário for adicionando filtros.
        self.filters = []

        # Define a ordenação default dos dados do grid como data decrescente.
        self.order_by = "data"
        self.order_direction = "DESC"

        self.setWindowTitle("Detalhes da Conta")

        # ============================================================
        # BUSCA DADOS DA CONTA
        # ============================================================
        #
        # OPÇÃO A DEFINIDA:
        #
        # A tela recebe apenas o ID.
        # Os dados completos são carregados novamente do banco.
        #
        # Ajustar o método abaixo conforme o repositório real.
        #
        # Deve retornar:
        #
        # banco
        # agencia
        # conta
        # apelido
        #
        # ============================================================

        banco = ""
        agencia = ""
        conta = ""
        apelido = ""

        contas = RepositoryAccount.listar_contas()

        for (
            id_tmp,
            banco_tmp,
            agencia_tmp,
            conta_tmp,
            apelido_tmp,
        ) in contas:

            if id_tmp == id_conta:
                banco = banco_tmp
                agencia = agencia_tmp
                conta = conta_tmp
                apelido = apelido_tmp
                break

        # ============================================================
        # LAYOUT PRINCIPAL
        # ============================================================

        layout_principal = QVBoxLayout(self)

        # ============================================================
        # LINHA 1
        #
        # Apelido (negrito)
        # Banco
        # Agência
        # Conta
        # ============================================================

        linha_conta = QHBoxLayout()

        lbl_apelido = QLabel(apelido)
        lbl_apelido.setStyleSheet("font-weight: bold;")

        lbl_banco = QLabel(f"Banco: {banco}")
        lbl_agencia = QLabel(f"Ag: {agencia}")
        lbl_conta = QLabel(f"Conta: {conta}")

        linha_conta.addWidget(lbl_apelido)
        linha_conta.addSpacing(20)
        linha_conta.addWidget(lbl_banco)
        linha_conta.addSpacing(20)
        linha_conta.addWidget(lbl_agencia)
        linha_conta.addSpacing(20)
        linha_conta.addWidget(lbl_conta)
        linha_conta.addStretch()

        layout_principal.addLayout(linha_conta)

        # ============================================================
        # LINHA 2
        #
        # RESUMO DO MÊS ATUAL
        #
        # IMPORTANTE:
        # NÃO depende dos filtros.
        #
        # FUTURO:
        # Definir cálculo de saldo considerando saldo inicial.
        # ============================================================

        linha_resumo_mes = QHBoxLayout()

        self.lbl_mes_entrada = QLabel("Entradas: R$ 0,00")
        self.lbl_mes_saida = QLabel("Saídas: R$ 0,00")
        self.lbl_mes_saldo = QLabel("Saldo: R$ 0,00")
        self.lbl_mes_atual = QLabel("Mês Atual")

        linha_resumo_mes.addWidget(self.lbl_mes_entrada)
        linha_resumo_mes.addSpacing(20)

        linha_resumo_mes.addWidget(self.lbl_mes_saida)
        linha_resumo_mes.addSpacing(20)

        linha_resumo_mes.addWidget(self.lbl_mes_saldo)
        linha_resumo_mes.addSpacing(20)

        linha_resumo_mes.addWidget(self.lbl_mes_atual)
        linha_resumo_mes.addStretch()

        layout_principal.addLayout(linha_resumo_mes)

        # ============================================================
        # SEPARADOR
        # ============================================================

        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        layout_principal.addWidget(linha)

        # ============================================================
        # ÁREA DE CHIPS
        #
        # Aqui serão adicionados os chips dinamicamente.
        #
        # Exemplos:
        #
        # [Data: Junho/2026]
        # [Descrição contém mercado]
        # [Valor > 100]
        #
        # Ao clicar em um chip:
        #     abrir tela de edição já preenchida.
        #
        # ============================================================
        # LINHA DE FILTROS
        # ============================================================

        linha_filtros = QHBoxLayout()

        self.layout_chips = QHBoxLayout()
        self.layout_chips.setAlignment(Qt.AlignmentFlag.AlignLeft)

#        layout_principal.addLayout(self.layout_chips)
        linha_filtros.addLayout(
            self.layout_chips,
            1
        )

        # ============================================================
        # BOTÃO ADICIONAR FILTRO
        #
        # FUTURO:
        #
        # Abrirá menu:
        #
        # Data
        # Descrição
        # Valor
        #
        # Regras:
        #
        # - Data pode existir apenas uma vez.
        # - Descrição pode existir várias vezes.
        # - Valor pode existir várias vezes.
        #
        # ============================================================

        self.btn_adicionar_filtro = QPushButton("+ Adicionar Filtro")




        menu_filtro = QMenu(self)

        acao_data = menu_filtro.addAction("Data")
        acao_descricao = menu_filtro.addAction("Descrição")
        acao_valor = menu_filtro.addAction("Valor")

        acao_data.triggered.connect(
            self.adicionar_filtro_data
        )

        acao_descricao.triggered.connect(
            self.adicionar_filtro_descricao
        )

        acao_valor.triggered.connect(
            self.adicionar_filtro_valor
        )

        self.btn_adicionar_filtro.setMenu(menu_filtro)



        # self.btn_adicionar_filtro.clicked.connect(self.adicionar_filtro)

#        layout_principal.addWidget(self.btn_adicionar_filtro)
        linha_filtros.addWidget(
            self.btn_adicionar_filtro
        )
        layout_principal.addLayout(
            linha_filtros
        )

        # ============================================================
        # SEPARADOR
        # ============================================================

        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        layout_principal.addWidget(linha)


        # ============================================================
        # LINHA DE STATUS
        # ============================================================
        linha_status = QHBoxLayout()

        self.lbl_status = QLabel("Pronto")
        self.btn_exportar_excel = QPushButton("Exportar Excel")

        self.btn_exportar_excel.clicked.connect(self.exportar_excel)

        linha_status.addWidget(self.lbl_status)
        linha_status.addStretch()
        linha_status.addWidget(self.btn_exportar_excel)

        layout_principal.addLayout(linha_status)

        # ============================================================
        # TABELA DE RESULTADOS
        #
        # FUTURO:
        #
        # Implementar ordenação por cabeçalho.
        #
        # Data
        # Descrição
        # Valor
        #
        # Similar ao Access.
        #
        # ============================================================
        
        self.tbl_resultados = QTableWidget()

        self.tbl_resultados.setColumnCount(3)

        self.tbl_resultados.setHorizontalHeaderLabels(
            [
                "Data",
                "Descrição",
                "Valor",
            ]
        )

        header = self.tbl_resultados.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_resultados.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.update_header_sort_indicator() # Define indicador de ordenação da coluna

        layout_principal.addWidget(self.tbl_resultados)

        # ============================================================
        # SEPARADOR
        # ============================================================

        linha = QFrame()
        linha.setFrameShape(QFrame.Shape.HLine)
        layout_principal.addWidget(linha)

        # ============================================================
        # RESUMO DOS RESULTADOS
        #
        # IMPORTANTE:
        #
        # Diferente do resumo do mês atual.
        #
        # Estes valores mudam de acordo com os filtros.
        #
        # ============================================================

        linha_resumo_resultado = QHBoxLayout()

        self.lbl_qtd_registros = QLabel("Registros: 0")
        self.lbl_total_entradas = QLabel("Entradas: R$ 0,00")
        self.lbl_total_saidas = QLabel("Saídas: R$ 0,00")
        self.lbl_total_saldo = QLabel("Saldo: R$ 0,00")

        linha_resumo_resultado.addWidget(self.lbl_qtd_registros)
        linha_resumo_resultado.addSpacing(20)

        linha_resumo_resultado.addWidget(self.lbl_total_entradas)
        linha_resumo_resultado.addSpacing(20)

        linha_resumo_resultado.addWidget(self.lbl_total_saidas)
        linha_resumo_resultado.addSpacing(20)

        linha_resumo_resultado.addWidget(self.lbl_total_saldo)
        linha_resumo_resultado.addStretch()

        layout_principal.addLayout(linha_resumo_resultado)

        # ============================================================
        # CARGA INICIAL
        #
        # FUTURO:
        #
        # Carregar lançamentos da conta.
        # Aplicar filtro padrão.
        # Atualizar resumos.
        #
        # ============================================================

        self.carregar_dados()

    # ================================================================
    # MÉTODOS
    # ================================================================

    def carregar_dados(self):
        """
        FUTURO

        Responsável por:

        1) Carregar lançamentos.
        2) Aplicar filtros.
        3) Atualizar tabela.
        4) Atualizar resumo filtrado.
        5) Atualizar resumo do mês atual.
        """
        pass




    # ================================================================
    # AÇÔES
    # ================================================================
    # def adicionar_filtro(self):
    #     UI_filter_selector.load()

    def adicionar_filtro_data(self):
       janela = UI_filter_date.load()
       janela.filter_created.connect(self.on_filter_created)

    def adicionar_filtro_descricao(self):
        janela = UI_filter_text.load()
        janela.filter_created.connect(self.on_filter_created)

    def adicionar_filtro_valor(self):
        janela = UI_filter_money.load()
        janela.filter_created.connect(self.on_filter_created)

    def on_filter_created(self, filtro):
        # Adiciona o filtro na lista de filtros.
        self.filters.append(filtro)

        # Associa o filtro ao chip
        chip = UI_filter_chip(filtro.chip_text)

        # Cria a conexção entre o X para remoção e a função de remoção.
        chip.remove_requested.connect(
            lambda: self.remove_filter(filtro, chip)
        )

        # Cria o objeto do chip
        self.layout_chips.addWidget(chip)

        # Atualiza o grid
        self.refresh_results()
        

    # Remove chip
    def remove_filter(self, filtro, chip):
        self.filters.remove(filtro)
        chip.deleteLater()

        # Atualiza o grid
        self.refresh_results()

    # Atualiza Grid confirme chips
    def refresh_results(self):

        self.lbl_status.setText( "Consultando...")
        self.repaint()

        # try: # TODO: DESCOMENTAR O TRY!

        self.carregar_resultados()

        self.atualizar_grid()

        self.atualizar_resumo()
        self.update_header_sort_indicator()

        self.lbl_status.setText(
            f"Consulta concluída. "
            # f"{qtd} filtro(s)."
        )



        # except Exception as e:

        #     self.lbl_status.setText(
        #         f"Erro: {e}"
        #     )

    def carregar_resultados(self):
        # RepositoryTransaction.search(self.id_conta, self.filters)
        self.resultados = RepositoryTransaction.search(
            self.id_conta,
            self.filters,
            self.order_by,
            self.order_direction
        )

    def atualizar_grid(self):
        self.tbl_resultados.setRowCount(0)

        for registro in self.resultados:

            row = self.tbl_resultados.rowCount()

            self.tbl_resultados.insertRow(row)

            self.tbl_resultados.setItem(
                row,
                0,
                QTableWidgetItem(str(registro[3]))
            )

            self.tbl_resultados.setItem(
                row,
                1,
                QTableWidgetItem(str(registro[4]))
            )

            # -- 
            item_valor = QTableWidgetItem(format_money(registro[5]))

            if registro[5] < 0:
                item_valor.setForeground(QColor("red"))

            self.tbl_resultados.setItem(
                row,
                2,
                item_valor
            )

            # self.tbl_resultados.setItem(
            #     row,
            #     2,
            #     QTableWidgetItem(format_money(registro[5]))
            # )
        # self.update_header_sort_indicator()

    def atualizar_resumo(self):
        qtd = len(self.resultados)
        total_entradas = sum(
            row["valor"]
            for row in self.resultados
            if row["valor"] > 0
        )
        total_saidas = sum(
            row["valor"]
            for row in self.resultados
            if row["valor"] < 0
        )
        saldo = sum(
            row["valor"]
            for row in self.resultados
        )

        self.lbl_qtd_registros.setText(
            f"Registros: {qtd}"
        )

        self.lbl_total_entradas.setText(
            f"Entradas: {format_money(total_entradas)}"
        )

        self.lbl_total_saidas.setText(
            f"Saídas: {format_money(total_saidas)}"
        )

        self.lbl_total_saldo.setText(
            f"Saldo: {format_money(saldo)}"
        )

        self.lbl_total_saidas.setStyleSheet(
            "color: red;"
        )

        if saldo < 0:
            self.lbl_total_saldo.setStyleSheet("color: red;")
        else:
            self.lbl_total_saldo.setStyleSheet("")

    ### EXPORTA DADOS DA PESQUISA PARA EXCEL
    def exportar_excel(self):

        rows = []

        for registro in self.resultados:
            rows.append([
                registro[3],  # data
                registro[4],  # descrição
                registro[5] / 100,  # valor
            ])

        file_path = ExcelExport.export(
            rows=rows,
            headers=["Data", "Descrição", "Valor"],
            file_prefix="pesquisa"
        )

        QMessageBox.information(
            self,
            "Exportação",
            f"Arquivo exportado com sucesso:\n\n{file_path}"
        )

    def on_header_clicked(self, column):

        columns = {
            0: "data",
            1: "descricao",
            2: "valor",
        }

        selected_column = columns[column]

        if self.order_by == selected_column:
            self.order_direction = "ASC" if self.order_direction == "DESC" else "DESC"
        else:
            self.order_by = selected_column
            self.order_direction = "ASC"

        self.update_header_sort_indicator()
        self.refresh_results()


    def update_header_sort_indicator(self):

        headers = ["Data", "Descrição", "Valor"]

        columns = {
            "data": 0,
            "descricao": 1,
            "valor": 2,
        }

        idx = columns[self.order_by]

        arrow = "▲" if self.order_direction == "ASC" else "▼"

        headers[idx] = f"{headers[idx]} {arrow}"

        self.tbl_resultados.setHorizontalHeaderLabels(headers)
        
    # ================================================================
    # LOAD
    # ================================================================
    @classmethod
    def load(cls, id_conta):
        cls._janela = cls(id_conta)
        cls._janela.resize(1024, 768)
        cls._janela.show()
        return cls._janela