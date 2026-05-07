from openpyxl import load_workbook


class Excel_reader():
    def __init__(self, excel_path: str):
        # self.path = excel_path

        wb = load_workbook(excel_path, data_only=True)
        ws = wb.active

        h_row = self.detect_header(ws)
        print(h_row)
        # ws.close

    def detect_header(self, ws)-> int:
        scores = []

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            scores.append(self.analyze_row(row))

        header_row = max(range(len(scores)), key=lambda i: scores[i])
        return header_row


    def analyze_row(self, row):
        total = len(row)

        qtd_strings = sum(isinstance(c, str) for c in row if c is not None)
        qtd_numbers = sum(isinstance(c, (int, float)) for c in row if c is not None)
        filled = sum(c not in (None, "") for c in row)

        text_ratio = qtd_strings / total if total else 0
        number_ratio = qtd_numbers / total if total else 0
        completeness = filled / total if total else 0

        keywords = ["valor", "credito", "debito", "saldo", "descricao", "historico"]

        keyword_hits = 0
        for c in row:
            if isinstance(c, str):
                for k in keywords:
                    if k in c.lower():
                        keyword_hits += 1
                        break

        score = (
            text_ratio * 2.0
            - number_ratio * 2.0
            + keyword_hits * 3.0
            + completeness * 1.5
        )

        return score



# import unicodedata


# def normalizar(texto):
#     if texto is None:
#         return ""

#     texto = str(texto).strip().lower()

#     # remove acentos
#     texto = unicodedata.normalize('NFKD', texto)
#     texto = ''.join(c for c in texto if not unicodedata.combining(c))

#     return texto




# def encontrar_cabecalho(sheet, col_data, col_desc, col_valor):
#     alvo = {
#         normalizar(col_data),
#         normalizar(col_desc),
#         normalizar(col_valor)
#     }

#     for idx_linha, linha in enumerate(sheet.iter_rows(values_only=True)):
#         valores = [normalizar(cel) for cel in linha if cel is not None]

#         if not valores:
#             continue

#         encontrados = set(valores)

#         if alvo.issubset(encontrados):
#             return idx_linha, linha  # achou!

#     raise Exception(
#         f"Não foi possível localizar as colunas: "
#         f"{col_data}, {col_desc}, {col_valor}"
#     )


