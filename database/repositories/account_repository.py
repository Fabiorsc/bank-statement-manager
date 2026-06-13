# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class AccountRepository(BaseRepository):
    def inserir_conta(self, banco, agencia, conta, apelido):
        self._execute("""
        INSERT INTO contas (banco, agencia, conta, apelido)
        VALUES (?, ?, ?, ?)
        """, (banco, agencia, conta, apelido))

        return self.last_id

    def listar_contas(self):
        return self._fetch_all("SELECT * FROM contas")
