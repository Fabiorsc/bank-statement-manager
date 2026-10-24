# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)

class AccountRepository(BaseRepository):
    def inserir_conta(self, banco, agencia, conta, apelido):
        self._execute("""
        INSERT INTO contas (banco, agencia, conta, apelido)
        VALUES (?, ?, ?, ?)
        """, (banco, agencia, conta, apelido))

        logger.info(f"Conta criada | id={self.last_id} | banco={banco} | agencia={agencia} | conta={conta}")

        return self.last_id

    def listar_contas(self):
        return self._fetch_all("SELECT id, banco, agencia, conta, apelido FROM contas")


#TODO: Criar metodo para remoção de contas.

