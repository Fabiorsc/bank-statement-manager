# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository

class AccountLayoutRepository(BaseRepository):
    def inserir_conta_layout(self, conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador):
        # conn = get_connection()
        # cursor = conn.cursor()

        self._execute("""
            INSERT INTO conta_layout 
                (conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador)
            )
        return self.last_id
        # conn.commit()
        # conn.close()
    def get_conta_layout(self, conta_id):
        return self._fetch_one("""
        SELECT * FROM conta_layout WHERE conta_id = ?
        """, (conta_id,)
        )
    
    def exists_conta_layout(self, conta_id):
        result = self._fetch_one("""
        SELECT EXISTS(
            SELECT 1
            FROM conta_layout
            WHERE conta_id = ?
        )
        """, (conta_id,)
        )
        return bool(result[0])



