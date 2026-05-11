from enum import Enum

class AccountLayoutType(Enum):
    VALOR_UNICO = "valor único"
    CRED_DEB = "valor crédito + valor débito"
    VALOR_IND = "valor + indicador créd./déb."