from database.connection import get_connection

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        banco TEXT NOT NULL,
        agencia TEXT,
        conta TEXT,
        apelido TEXT
    )
    """)

    # Tabela transacoes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT,
        valor REAL NOT NULL,
        categoria TEXT,
        observacao TEXT,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conta_id) REFERENCES contas(id)
    )
    """)

    # (opcional, mas recomendado)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_transacoes_conta
    ON transacoes (conta_id)
    """)

    conn.commit()
    conn.close()
