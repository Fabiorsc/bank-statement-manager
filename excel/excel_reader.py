import unicodedata


def normalizar(texto):
    if texto is None:
        return ""

    texto = str(texto).strip().lower()

    # remove acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))

    return texto




def encontrar_cabecalho(sheet, col_data, col_desc, col_valor):
    alvo = {
        normalizar(col_data),
        normalizar(col_desc),
        normalizar(col_valor)
    }

    for idx_linha, linha in enumerate(sheet.iter_rows(values_only=True)):
        valores = [normalizar(cel) for cel in linha if cel is not None]

        if not valores:
            continue

        encontrados = set(valores)

        if alvo.issubset(encontrados):
            return idx_linha, linha  # achou!

    raise Exception(
        f"Não foi possível localizar as colunas: "
        f"{col_data}, {col_desc}, {col_valor}"
    )


