from domain.filters.filter_base import BaseFilter


class MoneyFilter(BaseFilter):
    """
    Filtro monetário.

    Exemplos:

    Valor > 100

    Valor <= 500

    Valor entre 100 e 500

    Um chip representa uma condição.
    Chips são ligados por AND.
    """

    OP_EQUAL = "="
    OP_GREATER = ">"
    OP_GREATER_EQUAL = ">="
    OP_LESS = "<"
    OP_LESS_EQUAL = "<="
    # OP_RANGE = "range"

    def __init__(self, conditions):
        self.conditions = conditions

    @property
    def chip_text(self):
        partes = []

        for operador, valor in self.conditions:
            partes.append(f"{operador} {valor}")

        return " OR ".join(partes)


    def match(self, registro):
        valor_registro = registro.valor

        for operador, valor in self.conditions:

            if operador == self.OP_EQUAL and valor_registro == valor:
                return True

            if operador == self.OP_GREATER and valor_registro > valor:
                return True

            if operador == self.OP_GREATER_EQUAL and valor_registro >= valor:
                return True

            if operador == self.OP_LESS and valor_registro < valor:
                return True

            if operador == self.OP_LESS_EQUAL and valor_registro <= valor:
                return True

        return False