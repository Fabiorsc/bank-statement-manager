# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class TransactionRepository(BaseRepository):
    def inserir_transacao(self, conta_id, data, descricao, valor, categoria=None, observacao=None):


            self._execute("""
            INSERT INTO transacoes (conta_id, data, descricao, valor, categoria, observacao)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (conta_id, data, descricao, valor, categoria, observacao))


    def listar_transacoes(self):
        # with get_connection() as conn:
        #     cursor = conn.cursor()

        #     cursor.execute("SELECT * FROM transacoes ORDER BY data DESC")
        #     return cursor.fetchall()
        return self._fetch_all("SELECT * FROM transacoes ORDER BY data DESC")

    def listar_por_conta(self, conta_id):
        # with get_connection() as conn:
        #     cursor = conn.cursor()

            return self._fetch_all("""
            SELECT * FROM transacoes
            WHERE conta_id = ?
            ORDER BY data DESC
            """, (conta_id,))

            # return cursor.fetchall()


    def listar_por_periodo(self, data_inicio, data_fim):
        # with get_connection() as conn:
        #     cursor = conn.cursor()

            return self._fetch_all("""
            SELECT * FROM transacoes
            WHERE data BETWEEN ? AND ?
            ORDER BY data DESC
            """, (data_inicio, data_fim))

            # return cursor.fetchall()