from openpyxl import load_workbook
import re
import unicodedata
from excel.excel_loader import ExcelLoader

class ExcelReader():
    def __init__(self):
        pass


    def load(self, excel_path: str):
        excel = ExcelLoader()
        wb=excel.load(excel_path)

        # wb = load_workbook(excel_path, data_only=True)
        ws = wb.active

        h_row = self.detect_header(ws)
        print(h_row)
        wb.close()

    def detect_header(self, ws)-> int:
        scores = []

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            scores.append(self._analyze_row(row))

        header_row = max(range(len(scores)), key=lambda i: scores[i])
        return header_row + 1


    def _analyze_row(self, row):
        total = len(row)

        qtd_strings = sum(isinstance(c, str) for c in row if c is not None)
        qtd_numbers = sum(isinstance(c, (int, float)) for c in row if c is not None)
        filled = sum(c not in (None, "") for c in row)

        text_ratio = qtd_strings / total if total else 0
        number_ratio = qtd_numbers / total if total else 0
        completeness = filled / total if total else 0

        keyword_hits = self._keywords_score(row)

        score = (
            text_ratio * 2.0
            - number_ratio * 2.0
            + keyword_hits * 3.0
            + completeness * 1.5
        )

        return score

    def _keywords_score(self,row)-> int:
        keywords = {"valor", "credito", "debito", "saldo", "descricao", "historico", "data", "lancamento", "saldo", "movimento"}

        keyword_hits = 0

        # Percorre cada célula da linha.
        for c in row:
            # Verifica se é uma string.
            if isinstance(c, str):

                normalized = self._normalize_text(c)
                # Usa regex para extrair palavras do texto e "SET" elimina duplicidades. (obs: talvez não precisasse disso mas evita coisas estranhas como "valor valor valor")
                words = set(re.findall(r"\w+", normalized))

                # Verifica se alguma das palavras da célula (words) existe na lista (keywords).
                if keywords.intersection(words):
                    keyword_hits += 1
        return keyword_hits
    
    # recebe um texto e retorna o mesmo texto sem acento em minúsculo.
    # Exemplo: recebe "CRÉDITO(r$)", retorna "credito(r$)"
    def _normalize_text(self,text):
        # Separa letra de acento: "crédito" vira "cre´dito".
        text = unicodedata.normalize("NFKD", text)
        # Remove os acentos do texto: "cre´dito" vira "credito".
        text = "".join(c for c in text if not unicodedata.combining(c))
        return text.lower()






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


