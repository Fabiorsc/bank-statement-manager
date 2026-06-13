def format_money(value):
    """
    Converte valor inteiro em centavos para moeda brasileira.

    Exemplos:
        410948   -> R$ 4.109,48
        315      -> R$ 3,15
        -132090  -> -R$ 1.320,90
    """
    # verifica se o número é negativo
    negativo = value < 0
    # retira o negativo, se houver, para ser tratado separadamente.
    value = abs(value)
    # retoma as duas casas decimais. Definição de banco! Armazenamento de centavos como inteiro.
    reais = value / 100
    # Define numero com duas casas decimais e separador de milhar: Ex: 123 -> 123.00; 345.5 -> 345.50;...
    # Obs: Python trabalha com separador de milhar (,) e separador de decimal (.)
    texto = f"{reais:,.2f}"

    # Inverte pontos por virgulas e virgulas por pontos
    texto = texto.replace(",", "§")
    texto = texto.replace(".", ",")
    texto = texto.replace("§", ".")

    if negativo:
        return f"-R$ {texto}"

    return f"R$ {texto}"