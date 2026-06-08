from domain.filters.base_filter import BaseFilter


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
    OP_RANGE = "range"

    def __init__(
        self,
        operator: str,
        value=None,
        min_value=None,
        max_value=None,
    ):
        self.operator = operator

        self.value = value

        self.min_value = min_value
        self.max_value = max_value

    @property
    def chip_text(self):

        if self.operator == self.OP_RANGE:
            return (
                f"Valor entre "
                f"{self.min_value} "
                f"e "
                f"{self.max_value}"
            )

        return (
            f"Valor "
            f"{self.operator} "
            f"{self.value}"
        )

    def match(self, registro):

        valor = registro.valor

        if self.operator == self.OP_EQUAL:
            return valor == self.value

        if self.operator == self.OP_GREATER:
            return valor > self.value

        if self.operator == self.OP_GREATER_EQUAL:
            return valor >= self.value

        if self.operator == self.OP_LESS:
            return valor < self.value

        if self.operator == self.OP_LESS_EQUAL:
            return valor <= self.value

        if self.operator == self.OP_RANGE:
            return (
                self.min_value
                <= valor
                <= self.max_value
            )

        return False