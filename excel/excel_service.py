from openpyxl import load_workbook

from excel.excel_reader import encontrar_cabecalho

def iniciar_leitura(caminho_arquivo, colunas):
    wb = load_workbook(caminho_arquivo)
    sheet = wb.active

    linha_idx, linha = encontrar_cabecalho(
        sheet,
        col_data=colunas["data"],
        col_desc=colunas["descricao"],
        col_valor=colunas["valor"]
    )

    print("Cabeçalho encontrado na linha:", linha_idx)

    return linha_idx, linha


