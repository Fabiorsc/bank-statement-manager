from database.connection import get_connection


def inserir_transacao(conta_id, data, descricao, valor, categoria=None, observacao=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transacoes (conta_id, data, descricao, valor, categoria, observacao)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (conta_id, data, descricao, valor, categoria, observacao))


def listar_transacoes():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transacoes ORDER BY data DESC")
        return cursor.fetchall()


def listar_por_conta(conta_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM transacoes
        WHERE conta_id = ?
        ORDER BY data DESC
        """, (conta_id,))

        return cursor.fetchall()


def listar_por_periodo(data_inicio, data_fim):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM transacoes
        WHERE data BETWEEN ? AND ?
        ORDER BY data DESC
        """, (data_inicio, data_fim))

        return cursor.fetchall()