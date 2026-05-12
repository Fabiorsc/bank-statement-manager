


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

            # Verifica os dados das colunas relevantes e traz uma tabela(lista de dict) com os dados convertidos e transformados para as colunas necesárias.
            table = clsCheckColumnsValues.check_n_extract_columns(ws, layout)

            for row in table:
                i_date = row["date"]
                i_desc = row["description"]
                i_value = row["value"]
                if "SALDO" in i_desc.upper():
                    #remover linha!

                # if "TOTAL" in (i_date.upper(), i_desc, i_value) and "" in (i_date, i_desc, i_value):
            # TENHO QUE TIRAR O TOTAL ANTES DE CONVERTER POIS O TOTAL PODE ESTAR EM UMA COLUNA DATE OU MONY QUE VAI DAR ERRO AO CONVERTER E INVALIDAR A EXTRAÇÂO.

        # SEPARAR EM UOUTRO METODO PARA SER CHAMADO PELA UI.
        h_row = clsDetectHeader.detect_header(ws)
        print(h_row)
        wb.close()


