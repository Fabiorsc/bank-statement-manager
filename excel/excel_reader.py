# from openpyxl import load_workbook

from excel.excel_loader import ExcelLoader
from excel import clsDetectHeader
from excel import clsCheckColumnsValues
from database.repositories import RepositoryAccountLayout
import logging

logger = logging.getLogger(__name__)



class ExcelReader():
    def __init__(self):
        pass

    # Lê a planilha Excel com os dados, identifica os dados conforme pré configuração e elimina linhas inúteis.
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

            table = self.final_cleanup(table)
            
            stop = 'para'
            return table


        # # SEPARAR EM UOUTRO METODO PARA SER CHAMADO PELA UI.
        # h_row = clsDetectHeader.detect_header(ws)
        # print(h_row)

        wb.close()

    def final_cleanup(self, table):
        len_antes = len(table)
        aux_table = table[:] # faz uma cópia da lista para não alterar a lista enquanto pecorre a mesma.
        for i, row in enumerate(aux_table):
            i_excel_row = row["excel_row"]
                # i_date = row["date"]
            i_desc = row["description"]
                # i_value = row["value"]
            if "SALDO" == i_desc.replace(" ", "").upper(): 
                table.remove(row) # remove linha de SALDO
                logger.info(f"Removida linha {i_excel_row} - com descrição '{i_desc}' (SALDO)")
            if "SALDOANTERIOR" == i_desc.replace(" ", "").upper(): 
                table.remove(row) # remove linha de SALDO ANTERIOR
                logger.info(f"Removida linha {i_excel_row} - com descrição '{i_desc}' (SALDO ANTERIOR)")
            if "TOTAL" == i_desc.replace(" ", "").upper(): 
                table.remove(row) # Remove linha de TOTAL 
                logger.info(f"Removida linha {i_excel_row} - com descrição '{i_desc}' (TOTAL)")
        len_depois = len(table)
        return table


