# from database.connection import get_connection
from database.repositories.base_repository import BaseRepository
from domain.filters.filter_date import DateFilter
from domain.filters.filter_money import MoneyFilter
from domain.filters.filter_text import TextFilter

class TransactionRepository(BaseRepository):
    def inserir_transacao(self, conta_id, import_id, data, descricao, valor, categoria=None, observacao=None):
        db_valor = self.db_convert2_money(valor)
        if not self._exists_transaction(conta_id, import_id, data, descricao, valor):    
            self._execute("""
                INSERT INTO transacoes (conta_id, import_id, data, descricao, valor, categoria, observacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (conta_id, import_id, data, descricao, db_valor, categoria, observacao)) # converte valor para str pq SQLite não tem decimal e str é melhor que float/real.
            return self.last_id
        else:
            return None

    def listar_transacoes(self):
        return self._fetch_all("SELECT * FROM transacoes ORDER BY data DESC")

    def listar_por_conta(self, conta_id):
        return self._fetch_all("""
            SELECT * FROM transacoes
            WHERE conta_id = ?
            ORDER BY data DESC
            """, (conta_id,))

    def listar_por_periodo(self, data_inicio, data_fim):
        return self._fetch_all("""
            SELECT * FROM transacoes
            WHERE data BETWEEN ? AND ?
            ORDER BY data DESC
            """, (data_inicio, data_fim))

    def _exists_transaction(self, conta_id, import_id, data, descricao, valor):
        # Verifica se existe um ouro lançamento da mesma conta, data, descricao e valor mas de uma outro importação.
        # Permite repetições dentro da mesma importação mas se os dados se repetirem de outra importação interpreta como duplicidade.
        # Isso é para evitar que importações com dados de periodos sobrepostos dupliquem os registros.
        db_valor = self.db_convert2_money(valor)
        return self._fetch_one(
            """
            SELECT 1 FROM transacoes
            WHERE conta_id = ? AND import_id <> ? AND data = ? AND descricao = ? AND valor = ? 
            LIMIT 1
            """,
            (conta_id, import_id, data, descricao, db_valor)
        )

    def db_convert2_money(delf, valor):
        # Recebe um valor decimal e converte em inteiro com decimal!
        # Ex: recebe: 123.23 e retorna: 12323
        # Este recurso é utiliado para não ter que usar REAL no banco que pode causar 
        # implecisão de centavos pois o REAL é um float que pode interpretar valore 
        # fracionados com imprecisão algumas vezes. 
        return int(valor * 100)

    def search(self, id_account, filters):
        where_parts = ["conta_id = ?"]

        params = [id_account]

        for filtro in filters:
            if isinstance(filtro, TextFilter):
                self.filter2sql_text(where_parts, params, filtro)
                # sql, parameters = self.filter2sql_text(where_parts, params, filtro)
                # where_parts.append(sql)
                # params.append(parameters)

            if isinstance(filtro, MoneyFilter):
                self.filter2sql_money(where_parts, params, filtro)
                # sql, parameters = self.filter2sql_money(where_parts, params, filtro)
                # where_parts.append(sql)
                # params.append(parameters)

            if isinstance(filtro, DateFilter):
                self.filter2sql_date(where_parts, params, filtro)
                # sql, parameters = self.filter2sql_date(where_parts, params, filtro)
                # where_parts.append(sql)
                # params.append(parameters)

        sql = f"""
            SELECT *
            FROM transacoes
            WHERE {" AND ".join(where_parts)}
            ORDER BY data DESC
        """
        return self._fetch_all(sql, tuple(params))


    def filter2sql_date(self, where_parts, params, filtro):
        if filtro.mode == DateFilter.MODE_SINGLE:
            where_parts.append(" data = ?")
            params. append(f"{str(filtro.data)}")

        elif filtro.mode == DateFilter.MODE_RANGE:
            where_parts.append(" data BETWEEN ? AND ?")
            params.extend([str(filtro.data_inicial), str(filtro.data_final)])

        # return where_parts, params

    def filter2sql_money(self, where_parts, params, filtro):
        partes = []
        for operador, valor in filtro.conditions:
            partes.append(f"valor {operador} ?")
            params.append(self.db_convert2_money(valor))

        where_parts.append(f"({' OR '.join(partes)})")
        # return (f"({' OR '.join(partes)})", params)

    def filter2sql_text(self, where_parts, params, filtro):
        partes = []
        for operador, valor in filtro.conditions:
            if operador == TextFilter.OP_CONTAINS:
                partes.append("descricao LIKE ?")
                params.append(f"%{valor}%")

            else:
                partes.append("descricao NOT LIKE ?")
                params.append(f"%{valor}%")

        where_parts.append(f"({' OR '.join(partes)})")
        # return (f"({' OR '.join(partes)})", params)
                
