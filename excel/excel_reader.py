


from openpyxl import load_workbook

from excel.excel_loader import ExcelLoader
from excel import clsDetectHeader
from excel import clsCheckColumnsValues
from database.repositories import RepositoryAccountLayout



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

            len_antes = len(table)
            # table = [x for x in table if "SALDO" not in x["description"].upper() ]
            

            aux_table = table[:] # faz uma cópia da lista para não alterar a lista enquanto pecorre a mesma.
            for row in aux_table:
                i_date = row["date"]
                i_desc = row["description"]
                i_value = row["value"]
                if "SALDO" == i_desc.strip().upper(): table.remove(row) # remove linha de SALDO
                if "SALDO ANTERIOR" == i_desc.strip().upper(): table.remove(row) # remove linha de SALDO ANTERIOR
                if "TOTAL" == i_desc.strip().upper(): table.remove(row) # Remove linha de TOTAL 
            len_depois = len(table)
            
            
            stop = 'para'
            return table



        # # SEPARAR EM UOUTRO METODO PARA SER CHAMADO PELA UI.
        # h_row = clsDetectHeader.detect_header(ws)
        # print(h_row)


        wb.close()



