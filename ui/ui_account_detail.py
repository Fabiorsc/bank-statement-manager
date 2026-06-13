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


class UI_account_detail(QWidget):
    """
    *****   ESTOU NO PONTO DE FAZER OS CHIPS DE FILTRO FUNCIONAREM.


    Tela de visualização e análise de uma conta.

    OBJETIVOS DA TELA

    1) Exibir os dados principais da conta.
    2) Exibir um resumo do mês atual.
    3) Permitir filtros através de chips.
    4) Exibir os lançamentos encontrados.
    5) Exibir um resumo dos resultados filtrados.

    ----------------------------------------------------------------

    REGRAS DEFINIDAS

    CABEÇALHO

    Linha 1:
        - Apelido (negrito)
        - Banco
        - Agência
        - Conta

    Linha 2:
        - Entradas do mês atual
        - Saídas do mês atual
        - Saldo do mês atual
        - Mês atual

    IMPORTANTE:
        Este resumo SEMPRE representa o mês atual.
        Nunca deve ser afetado pelos filtros.

    ----------------------------------------------------------------

    FILTROS

    Existem apenas 3 tipos de filtros:

        DATA
        DESCRIÇÃO
        VALOR

    DATA
        - Permite apenas 1 chip.
        - Data única OU período.

    DESCRIÇÃO
        - Permite vários chips.
        - Chips usam AND.
        - Valores internos usam OR.

    Exemplo:

        [Contém: mercado, farmácia]
        AND
        [Não contém: extra]

    VALOR
        - Permite vários chips.
        - Chips usam AND.
        - Valores internos usam OR.

    Exemplo:

        [Valor = 100 ou 200]
        AND
        [Valor > 50]

    ----------------------------------------------------------------

    ORDENAÇÃO

    Futuramente será implementada no cabeçalho da tabela.

    Comportamento planejado:

        Sem ordenação
            ↓
        Crescente
            ↓
        Decrescente
            ↓
        Sem ordenação

    Semelhante ao Access e Excel.
    """

    def __init__(self, id_conta):
        super().__init__()

        self.id_conta = id_conta

        self.filters = []

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
        # Label STATUS
        # ============================================================
        self.lbl_status = QLabel("Pronto")
        layout_principal.addWidget(self.lbl_status)


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


        # =====================================
        # FUTURO
        # Chamada RepositoryTransaction
        # =====================================

        # qtd = len(self.filters)

        self.carregar_resultados()

        self.atualizar_grid()

        self.atualizar_resumo()
        
        self.lbl_status.setText(
            f"Consulta concluída. "
            # f"{qtd} filtro(s)."
        )



        # except Exception as e:

        #     self.lbl_status.setText(
        #         f"Erro: {e}"
        #     )

    def carregar_resultados(self):
        self.resultados = RepositoryTransaction.search(self.id_conta, self.filters)
        # print (self.resultados)
        # RepositoryTransaction.pragma_table("transacoes")
        # RepositoryTransaction.pragma_field("transacoes", "valor")

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

            self.tbl_resultados.setItem(
                row,
                2,
                QTableWidgetItem(format_money(registro[5]))
            )


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



    # ================================================================
    # LOAD
    # ================================================================
    @classmethod
    def load(cls, id_conta):
        cls._janela = cls(id_conta)
        cls._janela.resize(1024, 768)
        cls._janela.show()
        return cls._janela