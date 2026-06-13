from database.connection import get_connection
import sqlite3

class BaseRepository:
    def __init__(self):
        self.last_id = None
        self.row_cont = None

    def _execute(self, query, params=()) -> None:
        # Abre conexão com banco
        conn = get_connection()

        # Cria cursor de execução
        cursor = conn.cursor()

        # Executa query
        cursor.execute(query, params)

        # Confirma transação
        conn.commit()
        
        self.last_id = cursor.lastrowid
        self.row_cont = cursor.rowcount

        # Fecha conexão
        conn.close()

    def _fetch_all(self, query, params=()):

        # Abre conexão com banco
        conn = get_connection()

        # Cria cursor de execução
        cursor = conn.cursor()

        # Executa query
        cursor.execute(
            query,
            params
        )

        # Obtém todos os resultados
        results = cursor.fetchall()

        # Fecha conexão
        conn.close()

        # Retorna resultados
        return results

    def _fetch_one(self, query, params=()):

        # Abre conexão com banco
        conn = get_connection()

        # Cria cursor de execução
        cursor = conn.cursor()

        # Executa query
        cursor.execute(
            query,
            params
        )

        # Obtém primeiro resultado
        result = cursor.fetchone()

        # Fecha conexão
        conn.close()

        # Retorna resultado
        return result
    
    def _print_table(self, table_name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")

        for tabela in cursor.fetchall():
            print(dict(tabela))

        conn.close()

    def pragma_table(self, table_name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")

        for row in cursor.fetchall():
            print(dict(row))
        conn.close()
    
    def pragma_field(self, table_name, field_name):
        conn = get_connection()
        cursor = conn.cursor()

        sql = f"""
            SELECT {field_name}, typeof({field_name})
            FROM {table_name}
            LIMIT 20;
            """

        cursor.execute(sql)

        for row in cursor.fetchall():
            print(dict(row))
        conn.close()
