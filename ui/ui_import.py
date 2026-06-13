import sys
from excel.excel_reader import ExcelReader
from database.repositories import RepositoryAccountLayout, RepositoryImport, RepositoryTransaction
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QSizePolicy,  QVBoxLayout,
    QWidget, QPushButton, QLabel, QMessageBox, QFileDialog
)


class UI_import(QWidget):
    def __init__(self,id_conta, apelido, banco, agencia, conta):
        super().__init__()
        self.excel_file = ""
        self.setWindowTitle("Importar Dados")

        self.conta_id = id_conta
        self.lbl_apelido = QLabel(f"<b>{apelido}</b>")
        self.lbl_apelido.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lbl_banco = QLabel(f"<b>Banco:</b> {banco}")
        self.lbl_banco.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lbl_agencia = QLabel(f"<b>Agencia:</b> {agencia}")
        self.lbl_agencia.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lbl_conta = QLabel(f"<b>Conta:</b> {conta}")
        self.lbl_conta.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        self.label = QLabel("Nenhum arquivo selecionado")
        self.btn_sel_excel = QPushButton("Selecionar arquivo Excel")
        self.btn_sel_excel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_sel_excel.clicked.connect(self.selecionar_arquivo)

        self.btn_import = QPushButton("Importar Excel")
        self.btn_import.clicked.connect(self.import_excel)


        layout_dados = QHBoxLayout()
        layout_dados.addWidget(self.lbl_apelido)
        layout_dados.addWidget(self.lbl_banco)
        layout_dados.addWidget(self.lbl_agencia)
        layout_dados.addWidget(self.lbl_conta)
        layout_dados.addStretch()
        layout_dados.setSpacing(25)

        layout_sel_excel = QHBoxLayout()
        layout_sel_excel.addWidget(self.label)
        layout_sel_excel.addStretch()  # empurra o botão pra direita
        layout_sel_excel.addWidget(self.btn_sel_excel)

        layout_import = QVBoxLayout()
        layout_import.addLayout(layout_dados)
        layout_import.addLayout(layout_sel_excel)
        layout_import.addWidget(self.btn_import)

        self.setLayout(layout_import)

        

    def selecionar_arquivo(self):
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            "Arquivos Excel (*.xlsx *.xls);;Todos os Arquivos (*.*)"
        )

        if arquivo:
            self.excel_file=arquivo
            self.label.setText(arquivo)

    def import_excel(self):
        if RepositoryAccountLayout.exists_conta_layout(self.conta_id):
            excel = ExcelReader()
            if self.excel_file:
                table = excel.load(self.conta_id, self.excel_file)
                id_import = RepositoryImport.inserir_import(self.conta_id,self.excel_file)
                
                # Inicialização de contadores para controle de registros inseridos e duplicados.
                inserted = 0                
                duplicated = 0

                for reg in table:
                    data = reg["date"]
                    desc = reg["description"]
                    valor = reg["value"]
                    categ = None
                    obs = None

                    # Insere e contabiliza inseridos e duplicados(last_id = None).
                    last_id = RepositoryTransaction.inserir_transacao(self.conta_id, id_import, data, desc, valor,categ, obs)
                    if last_id:
                        inserted += 1
                    else:
                        duplicated += 1
            else:
                QMessageBox.information(self, "Erro", "Selecione um arquivo para ser importado!")
        else:
            QMessageBox.information(self, "Erro", "Não existe configuração de layout para esta conta.")
        
        # Envia uma msg de conclusão e informação de inseridos e duplicados baseado em inserted e diplicated.
        QMessageBox.information(self, "Conclusão", f"Importação concluída!\nRegistros inseridos: {inserted}\nRegistros duplicados: {duplicated}")

        # # x1 = RepositoryTransaction.listar_transacoes()
        # # x2 = RepositoryImport.listar_imports()
        # x1=[]
        # x2=[]
        # [x1.append(dict(x)) for x in RepositoryTransaction.listar_transacoes()]
        # [x2.append(dict(x)) for x in RepositoryImport.listar_imports()]
        stop ="para"

    @classmethod
    def load(cls,id_conta, apelido, banco, agencia, conta):
        # app = QApplication(sys.argv)
        cls._janela = cls( id_conta, apelido, banco, agencia, conta)
        cls._janela.resize(600, 150)
        cls._janela.show()
        return cls._janela
        # app.exec()