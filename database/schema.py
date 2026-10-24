from database.connection import get_connection

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    # CRIA TABELA CONTAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        banco TEXT NOT NULL,
        agencia TEXT,
        conta TEXT,
        apelido TEXT,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # cursor.execute("DROP TABLE transacoes")
    # CRIA TABELA TRANSAÇÕES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta_id INTEGER NOT NULL,
        import_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT,
        valor INTEGER NOT NULL, 
        categoria TEXT,
        observacao TEXT,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conta_id) REFERENCES contas(id)
    )
    """)

    # CRIA TABELA CONTA_LAYOUT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conta_layout (
        id INTEGER PRIMARY KEY,
        conta_id INTEGER NOT NULL,
        layout_tipo TEXT NOT NULL,
        linha_header INTEGER NOT NULL,
        col_data INTEGER,
        col_descricao INTEGER,
        col_valor INTEGER,
        col_credito INTEGER,
        col_debito INTEGER,
        col_indicador INTEGER,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conta_id) REFERENCES contas(id)
    )
    """)

    # cursor.execute("DROP TABLE import")
    # CRIA TABELA IMPORT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS import (
        id INTEGER PRIMARY KEY,
        conta_id INTEGER NOT NULL,
        arquivo TEXT NOT NULL,
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

def remover_tabelas():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS transacoes")
        cursor.execute("DROP TABLE IF EXISTS conta_layout")
        cursor.execute('DROP TABLE IF EXISTS "import"')
        cursor.execute("DROP TABLE IF EXISTS contas")

        conn.commit()

    finally:
        conn.close()