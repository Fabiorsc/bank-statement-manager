# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class TransactionRepository(BaseRepository):
    def inserir_transacao(self, conta_id, import_id, data, descricao, valor, categoria=None, observacao=None):
   
        if not self._exists_transaction(conta_id, import_id, data, descricao, valor):    
            self._execute("""
                INSERT INTO transacoes (conta_id, import_id, data, descricao, valor, categoria, observacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (conta_id, import_id, data, descricao, str(valor), categoria, observacao)) # converte valor para str pq SQLite não tem decimal e str é melhor que float/real.
            return self.last_id
        else:
            return None

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

    def _exists_transaction(self, conta_id, import_id, data, descricao, valor):
        # Verifica se existe um ouro lançamento da mesma conta, data, descricao e valor mas de uma outro importação.
        # Permite repetições dentro da mesma importação mas se os dados se repetirem de outra importação interpreta como duplicidade.
        # Isso é para evitar que importações com dados de periodos sobrepostos dupliquem os registros.
        return self._fetch_one(
            """
            SELECT 1 FROM transacoes
            WHERE conta_id = ? AND import_id <> ? AND data = ? AND descricao = ? AND valor = ? 
            LIMIT 1
            """,
            (conta_id, import_id, data, descricao, str(valor))
        )
        # return cursor.fetchone() is not None