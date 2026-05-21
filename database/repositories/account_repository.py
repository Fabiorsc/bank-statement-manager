# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class AccountRepository(BaseRepository):
    def inserir_conta(self, banco, agencia, conta, apelido):
        # conn = get_connection()
        # cursor = conn.cursor()

        self._execute("""
        INSERT INTO contas (banco, agencia, conta, apelido)
        VALUES (?, ?, ?, ?)
        """, (banco, agencia, conta, apelido))

        # conn.commit()
        # conn.close()
        return self.last_id

    def listar_contas(self):
        # conn = get_connection()
        # cursor = conn.cursor()

        return self._fetch_all("SELECT * FROM contas")
        resultados = cursor.fetchall()

        # conn.close()
        # return resultados