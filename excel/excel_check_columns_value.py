
from datetime import datetime, date
import decimal
import re

from domain.account_layout_type import AccountLayoutType


MESES = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12
}

# Esta classe Além de verificar se o valor de cada coluna está correto, tb deve montar uma lista com os valores corretos
# convertendo date-string para datetime, por exemplo; Int e Floats para Decimal, ...
#completar o exemplo com a data e seguir para os outros tipos!

class CheckColumnsValues():
    def __init__(self):
        self.list_col_data = {}
        self.list_col_descricao = {}
        self.list_col_valor = {}
        self.list_col_credito = {}
        self.list_col_debito = {}
        self.list_col_indicador = {}

    def check_columns_values(self, ws, layout):
        layout_tipo = layout["layout_tipo"]
        linha_header = layout["linha_header"]
        col_data = layout["col_data"]
        col_descricao = layout["col_descricao"]
        col_valor = layout["col_valor"]
        col_credito = layout["col_credito"]
        col_debito = layout["col_debito"]
        col_indicador = layout["col_indicador"]

        # num_data = 
        # num_lin = linha_header + 1
        self.check_col_date(ws, self.excel_column_to_number(col_data), linha_header + 1)
        self.check_col_texto(ws, self.excel_column_to_number(col_descricao), linha_header + 1)

        if layout_tipo == AccountLayoutType.VALOR_UNICO.value:
            self.check_col_valor(ws, self.excel_column_to_number(col_valor),linha_header + 1)

        elif layout_tipo == AccountLayoutType.VALOR_IND.value:
            self.check_col_valor(ws, self.excel_column_to_number(col_valor),linha_header + 1)
            self.check_col_texto(ws, self.excel_column_to_number(col_indicador),linha_header + 1)

        elif layout_tipo == AccountLayoutType.CRED_DEB.value:
            self.check_col_valor(ws, self.excel_column_to_number(col_credito), linha_header + 1)
            self.check_col_valor(ws, self.excel_column_to_number(col_debito), linha_header + 1)

    def check_col_date(self,ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        for ch, value in enumerate(coluna):
            new_date = self.convert_to_datetime(value)
            if new_date:
                # CADASTRA EM UMA LISTA (linha + valor correto)
                ...
                ret[ch]=new_date
            else:
                print(f"Erro: valor {str(value)} não é uma data!")
                validado = False
                break

            # if not isinstance(value, (datetime, date)):
            #     print(f"Erro: valor {str(value)} não é uma data!")
            #     validado = False
            #     break
            
        return validado
    
    def check_col_texto(self, ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        for ch, value in enumerate(coluna):
            # new_money = self.convert_to_money(value)
            if isinstance(value, str):
                ret[ch]=value
            else:
                print(f"Erro: valor {str(value)} não é um texto!")
                validado = False
                break
        return validado
    
    def check_col_valor(self, ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        for ch, value in enumerate(coluna):
            new_money = self.convert_to_money(value)
            if new_money:
                ret[ch]=new_money

            else:
                print(f"Erro: valor {str(value)} não é um texto!")
                validado = False
                break
        return validado



        #     if isinstance(valor, (int,float)):
        #         continue
        #     elif self.is_money(valor):
        #         continue
        #     else:
        #         print(f"Erro: valor {str(valor)} não é um número!")
        #         validado = False
        #         break
        # return validado    

    def get_col(self, ws, col_number, line_number)-> tuple:
        return next(ws.iter_cols(min_col=col_number, max_col=col_number, min_row=line_number, values_only=True))


    def convert_to_money(self, value):
        if isinstance(value, (int, float)):
            return decimal(value)
        elif isinstance(value, str):
            return self.parse_money(value)

    def convert_to_datetime(self, value):
        if isinstance(value, (datetime, date)):
            return value
        elif isinstance(value, str):
            return self.parse_date_in_full(value)

            
    def excel_column_to_number(self, value):
        # Já é número
        if isinstance(value, int):
            return value

        # Garantir string
        if isinstance(value, str):
            value = value.strip().upper()

            resultado = 0

            for char in value:
                if ('A' <= char <= 'Z'):
                    resultado = resultado * 26 + (ord(char) - ord('A') + 1)
                else:    
                    raise ValueError(f"Coluna inválida: {value}")
        else:
            raise TypeError("Valor deve ser int ou str")
        
        return resultado
    
    # def is_money(self, value) -> bool:
    #     if isinstance(value, (int,float)):


    #     if not isinstance(value, str):
    #         return False

    #     pattern = r'^(R\$)?\s?[+-]?[0-9,.]+$'

    #     return bool(re.fullmatch(pattern, value.strip()))
    

    def parse_money(self, value):
        if not isinstance(value, str):
            return None

        value = value.strip().upper()

        pattern = r'^(R\$)?\s?[+-]?[0-9,.]+$'
        match = re.match(pattern, value)

        if not match:
            return None
        
        value = value.replace(' ', '')
        value = value.replace('R$', '')

        decimal_sep = None 
        # verifica terceira posição da direita 
        if len(value) >= 3 and value[-3] in '.,': 
            decimal_sep = value[-3] 
            
        value.replace(",","").replace(".","") 
        if decimal_sep:
            value = value[:-2] + '.' + value[-2:]

        return value


    def parse_date_in_full(self, value):

        if not isinstance(value, str):
            return None

        pattern = r'^\w+,?\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})$'
        match = re.match(pattern, value.strip().lower())

        if not match:
            return None

        dia = int(match.group(1))
        mes_nome = match.group(2)
        ano = int(match.group(3))

        mes = MESES.get(mes_nome)

        if not mes:
            return None

        return datetime(ano, mes, dia)