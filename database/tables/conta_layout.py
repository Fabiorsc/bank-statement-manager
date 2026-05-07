from database.connection import get_connection

def inserir_conta_layout(conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conta_layout 
        (conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (conta_id, layout_tipo, linha_header, col_data, col_descricao, col_valor, col_credito, col_debito, col_indicador)
    )

    conn.commit()
    conn.close()




