# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class ImportRepository(BaseRepository):
    def inserir_import(self, conta_id, arquivo):
        self._execute("""
            INSERT INTO import (conta_id, arquivo)
            VALUES (?, ?)
            """, (conta_id, arquivo))
        return self.last_id

    def listar_imports(self):

        return self._fetch_all("SELECT * FROM import ORDER BY data_criacao DESC")

    def listar_por_conta(self, conta_id):
        return self._fetch_all("""
        SELECT * FROM import
        WHERE conta_id = ?
        ORDER BY data DESC
        """, (conta_id,))


    def listar_por_periodo(self, data_inicio, data_fim):
        return self._fetch_all("""
        SELECT * FROM import
        WHERE data_criacao BETWEEN ? AND ?
        ORDER BY data DESC
        """, (data_inicio, data_fim))
