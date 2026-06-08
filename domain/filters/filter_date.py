from domain.filters.filter_base import BaseFilter


class DateFilter(BaseFilter):
    """
    Filtro de data.

    Regras:

    - Só pode existir um por tela.
    - Pode ser data única ou período.
    """

    MODE_SINGLE = "single"
    MODE_RANGE = "range"

    def __init__(
        self,
        mode: str,
        data=None,
        data_inicial=None,
        data_final=None,
    ):
        self.mode = mode

        self.data = data

        self.data_inicial = data_inicial
        self.data_final = data_final

    @property
    def chip_text(self):

        if self.mode == self.MODE_SINGLE:
            return f"Data: {self.data}"

        return (
            f"Data: "
            f"{self.data_inicial} "
            f"até "
            f"{self.data_final}"
        )

    def match(self, registro):

        data_registro = registro.data

        if self.mode == self.MODE_SINGLE:
            return data_registro == self.data

        return (
            self.data_inicial
            <= data_registro
            <= self.data_final
        )