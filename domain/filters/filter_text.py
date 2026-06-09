from domain.filters.filter_base import BaseFilter


class TextFilter(BaseFilter):
    """
    Filtro textual.

    Cada chip representa um grupo.

    Exemplo:

    Contém:
        mercado
        farmacia

    Significa:

        mercado OR farmacia

    Entre chips:
        AND
    """

    OP_CONTAINS = "contains"
    OP_NOT_CONTAINS = "not_contains"

    def __init__(
        self,
        operator: str,
        values: list[str],
    ):
        self.operator = operator
        self.values = values

    @property
    def chip_text(self):

        valores = ", ".join(self.values)

        if self.operator == self.OP_CONTAINS:
            return f"Contém: {valores}"

        return f"Não contém: {valores}"

    def match(self, registro):

        texto = registro.descricao.lower()

        valores = [
            valor.lower()
            for valor in self.values
        ]

        if self.operator == self.OP_CONTAINS:

            return any(
                valor in texto
                for valor in valores
            )

        return all(
            valor not in texto
            for valor in valores
        )