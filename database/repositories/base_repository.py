from database.connection import get_connection


class BaseRepository:

    def _execute(self, query, params=()) -> None:

        # Abre conexão com banco
        conn = get_connection()

        # Cria cursor de execução
        cursor = conn.cursor()

        # Executa query
        cursor.execute(
            query,
            params
        )

        # Confirma transação
        conn.commit()

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