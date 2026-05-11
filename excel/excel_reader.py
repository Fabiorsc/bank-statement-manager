


from openpyxl import load_workbook

from excel.excel_loader import ExcelLoader
from excel import clsDetectHeader
from excel import clsCheckColumnsValues
from database.repositories import RepositoryAccountLayout



class ExcelReader():
    def __init__(self):
        pass


    def load(self, conta_id,  excel_path: str):
        # RepositoryAccountLayout._print_table("conta_layout")
        # RepositoryAccountLayout._print_table("contas")
        excel = ExcelLoader()
        wb = excel.load(excel_path)

        ws = wb.active

#---------------------------------------------
        layout = RepositoryAccountLayout.get_conta_layout(conta_id)
        if layout:

# *** Pensar se retorno 1 lsita para cada coluna (ex: data, descrição, crdito. debito, ...) ou 
#     se já trago as listas refrentes a tabela (data, descrição, valor(+ e -)) ou 
#     se já trago uma estrutura pronta. (opção 2 e 3 não são muito diferentes!)
            clsCheckColumnsValues.check_columns_values(ws, layout)
            # self.check_columns_values(ws, layout)

        h_row = clsDetectHeader.detect_header(ws)
        print(h_row)
        wb.close()


