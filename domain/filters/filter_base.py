from abc import ABC, abstractmethod


class BaseFilter(ABC):
    """
    Classe base para todos os filtros.

    Responsabilidades:

    - Armazenar o tipo do filtro.
    - Gerar texto para exibição no chip.
    - Avaliar se um registro atende ao filtro.
    """

    @property
    @abstractmethod
    def chip_text(self) -> str:
        """
        Texto exibido no chip.
        """
        pass

    @abstractmethod
    def match(self, registro) -> bool:
        """
        Retorna True se o registro atende ao filtro.
        """
        pass