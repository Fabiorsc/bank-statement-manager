from database.connection import get_connection

def inserir_conta(banco, agencia, conta, apelido):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contas (banco, agencia, conta, apelido)
    VALUES (?, ?, ?, ?)
    """, (banco, agencia, conta, apelido))

    conn.commit()
    conn.close()


def listar_contas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contas")
    resultados = cursor.fetchall()

    conn.close()
    return resultados