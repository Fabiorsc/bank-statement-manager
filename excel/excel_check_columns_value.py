
from datetime import datetime, date
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
import re

from domain.account_layout_type import AccountLayoutType
from excel.excel_service import datetime_from_excel


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

class DateFormat(Enum):
    DD_MM_YYYY = 1
    DD_MM_YY = 2
    MM_DD_YYYY = 3
    MM_DD_YY = 4
    FLOAT = 5

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

    def check_n_extract_columns(self, ws, layout):
        layout_tipo = layout["layout_tipo"]
        linha_header = layout["linha_header"]
        col_data = layout["col_data"]
        col_descricao = layout["col_descricao"]
        col_valor = layout["col_valor"]
        col_credito = layout["col_credito"]
        col_debito = layout["col_debito"]
        col_indicador = layout["col_indicador"]

        table = []

        verificado,self.list_col_data = self.check_col_date(ws, self.excel_column_to_number(col_data), linha_header + 1)
        verificado, self.list_col_descricao = self.check_col_texto(ws, self.excel_column_to_number(col_descricao), linha_header + 1)

        if layout_tipo == AccountLayoutType.VALOR_UNICO.value:
            verificado, self.list_col_valor = self.check_col_valor(ws, self.excel_column_to_number(col_valor),linha_header + 1)
            for ch in self.list_col_data:
                row = {
                    'date': self.list_col_data.get(ch),
                    'description': self.list_col_descricao.get(ch),
                    'value': self.list_col_valor.get(ch)
                }
                table.append(row)

        elif layout_tipo == AccountLayoutType.VALOR_IND.value:
            verificado, self.list_col_valor = self.check_col_valor(ws, self.excel_column_to_number(col_valor),linha_header + 1)
            verificado, self.list_col_indicador = self.check_col_texto(ws, self.excel_column_to_number(col_indicador),linha_header + 1)
            for ch in self.list_col_data:
                value = self.list_col_valor.get(ch)
                indic = self.list_col_indicador.get(ch).upper()
                if indic == "D":
                    value = value * -1
                    row = {
                        'date': self.list_col_data.get(ch),
                        'description': self.list_col_descricao.get(ch),
                        'value': value
                    }
                    table.append(row)
                elif indic == "C":
                    value = value
                    row = {
                        'date': self.list_col_data.get(ch),
                        'description': self.list_col_descricao.get(ch),
                        'value': value
                    }
                    table.append(row)

        elif layout_tipo == AccountLayoutType.CRED_DEB.value:
            verificado, self.list_col_credito = self.check_col_valor(ws, self.excel_column_to_number(col_credito), linha_header + 1)
            verificado, self.list_col_debito = self.check_col_valor(ws, self.excel_column_to_number(col_debito), linha_header + 1)
            for ch in self.list_col_data:
                if self.list_col_credito.get(ch) != 0:
                    value = self.list_col_credito.get(ch)
                elif self.list_col_debito.get(ch) != 0:
                    value = self.list_col_debito.get(ch) * -1
                row = {
                    'date': self.list_col_data.get(ch),
                    'description': self.list_col_descricao.get(ch),
                    'value': value
                }
                table.append(row)

        return table


    def check_col_date(self,ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        short_data_type = self.check_short_date(coluna)
        for ch, value in enumerate(coluna):
            new_date = self.parse_date(value,short_data_type)
            if new_date is None and isinstance(value, str) and value == "":
                ret[ch] = ""
            if new_date is not None:
                ret[ch] = new_date
            else:
                print(f"Erro: Na linha {ch}, o valor '{str(value)}' não é uma data!")
                validado = False
                break           
        return (validado, ret)
    
    
    def check_col_texto(self, ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        for ch, value in enumerate(coluna):
            # new_money = self.convert_to_money(value)
            if isinstance(value, str):
                ret[ch]=value
            else:
                print(f"Erro: Na linha {ch}, o valor '{str(value)}' não é um texto!")
                validado = False
                break
        return (validado, ret)
    
    def check_col_valor(self, ws, col_number, line_number):
        ret = {}
        coluna = self.get_col(ws, col_number, line_number)
        validado = True
        for ch, value in enumerate(coluna):
            new_money = self.parse_money(value)
            
            if new_money is not None:
                ret[ch]=new_money
            else:
                print(f"Erro: Na linha {ch}, o valor '{str(value)}' não é um tipo moeda!")
                validado = False
                break
        return (validado, ret)


    def check_short_date(self, coluna):
        # Procura os valores de "coluna" até achar algum que consiga definir o formato da data.
        # Achando o primeiro que defina o formta, retorna o formato encontrado.
        # Baseado na suposição que todas as datas estão no mesmo formato.

        count_float = 0
        for ch, value in enumerate(coluna):
        
            # if isinstance(value,float):
            #     # Percorre todos os itens de "coluna" e conta quantos floats existem.
            #     count_float += 1

            # else: # Se for string...
            if isinstance(value, str):
                # Extrai as partes de uma data no tipo string.
                part1, part2, ano, _ = self.extract_date_parts(value)
                if part1 is None:
                    return None
                
                if not(part1.isdigit() and part2.isdigit() and ano.isdigit()):
                    return None

                if int(part1) > 12 and len(ano) == 2: 
                    return DateFormat.DD_MM_YY
                elif int(part1) > 12 and len(ano) == 4:
                    return DateFormat.DD_MM_YYYY
                elif int(part2) > 12 and len(ano) == 2:
                    return DateFormat.MM_DD_YY
                elif int(part2) > 12 and len(ano) == 4:
                    return DateFormat.MM_DD_YYYY
            # count_nao_float += 1

        # # Para garantir que não vai pegar um campo isolado por engano, 
        # # calcula se a quantidade de float é de 80% e 100% dos valores da coluna.
        # if 0.8 <= count_float / len(coluna) <= 1:
        #     return DateFormat.FLOAT

        return None
    
    def extract_date_parts(self, dat_str):
        # Extrai partes de uma data considernado NN-NN-NN ou NN-NN-NNNN, onde
        # N = qualquer número e "-" = qualquer caractere.
        # Onde 01-02-1900, parte1=01; parte2=02; parte3=1900 e parte4="-"
        pattern = r'^(\d{2})(.)(\d{2})\2(\d{2}|\d{4})$'
        match = re.match(pattern, dat_str)
        if match:
            return match.group(1), match.group(3), match.group(4), match.group(2)
        return None, None, None, None


    # def convert_to_money(self, value):
    #     if isinstance(value, (int, float)):
    #         return Decimal(value)
    #     elif isinstance(value, str):
    #         return self.parse_money(value)
    #     return None
    
    # def convert_to_datetime(self, value):
    #     if isinstance(value, (datetime, date)):
    #         return value
    #     elif isinstance(value, str):
    #         return self.parse_date_in_full(value)
    #     return None
            

    def parse_money(self, value):
        # Os tipos aceitos para o valor de moeda são int, float e str. Se for outro tipo, retorna None e gera erro.
        if not isinstance(value, (str,int,float)):
            return None
        
        # É melhor converter string para decimal do que float para decimal, e int não faz diferença, então converte tudo para string.
        value = str(value)

        # Remove espaços e coloca em maiusculo para facilitar tratamento e higienização da variável.
        value = value.strip().upper()
        value = value.replace(" ","")  # Remove espaços.
        value = value.replace("(","").replace(")","") # Remove parênteses. Alguns bancos usam parenteses para indicar negativo.
        value = value.replace("*","")                 # Remove Asterisco. Alguns bancos usam asterisco para indicar valores especiais, como valores bloquados em conta, por exemplo.

        if value == "": return Decimal('0.00') # retorno padrão = 2 casas decimais.

        pattern = r'^(R\$)?\s?[+-]?[0-9,.]+$'
        match = re.match(pattern, value)

        # Verifica se condiz com uma mascara esérada de valor monetário.
        if not match:
            return None # Se não coincidir retorna None e gera erro.
        
        # Remove espaços e indicação monetária.
        value = value.replace(' ', '')
        value = value.replace('R$', '')

        # Normaliza numero sem separador de milhar e separador de decimal = "."
        decimal_sep = None 
        # verifica separador de decimal na terceira posição da direita 
        if len(value) >= 3 and value[-3] in '.,': 
            decimal_sep = value[-3] 
        
        # remove todos separadores de milhar e decimal (, e .)
        value = value.replace(",","").replace(".","") 
        # Se existia separador de decimal, recoloca-o como ponto (.)
        if decimal_sep:
            value = value[:-2] + '.' + value[-2:]

        # Força conversão para decimal com 2 casas.
        return Decimal(str(value)).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        # return value

    def parse_date(self, value, short_date_type):
        ret = None
        if isinstance(value, (datetime, date)):
            return value
        if isinstance(value, str):
            value = value.strip()
            if ret := self.parse_date_in_full(value):
                return ret
            if ret := self.parse_short_date(value, short_date_type):
                return ret
        if isinstance(value, float):
            return datetime_from_excel(value)

    def parse_short_date(self, value, short_date_type):
        
        match short_date_type:
            case DateFormat.DD_MM_YY:
                part1, part2, ano, _ = self.extract_date_parts(value)
                ano = self.normalize_year(ano)
                dia = part1
                mes = part2
                # return date(ano, part2, part1)
            
            case DateFormat.DD_MM_YYYY:
                part1, part2, ano, _ = self.extract_date_parts(value)
                dia = part1
                mes = part2
                # return date(ano, part2, part1)
            
            case DateFormat.MM_DD_YY:
                part1, part2, ano, _ = self.extract_date_parts(value)
                ano = self.normalize_year(ano)
                dia = part2
                mes = part1
                # return date(ano, part1, part2)
            
            case DateFormat.MM_DD_YYYY:
                part1, part2, ano, _ = self.extract_date_parts(value)
                dia = part2
                mes = part1
                # return date( ano, part1, part2)

        if dia.isdigit() and mes.isdigit() and ano.isdigit():
            ano = int(ano)
            dia = int(dia)
            mes = int(mes)  
            return date( ano, mes, dia)
        else:
            raise ValueError(f"A data '{value}' não corresponde a um short date em nenhum formato conhecido(dd-mm-yyyy; dd-mm-yy; mm-dd-yyyy; mm-dd-yy).")
            
            # case DateFormat.FLOAT:
            #     return 

    def parse_date_in_full(self, value):
        # Verifica e converte data por extenso tipo "Quarta, 05 de Maio de 2010"
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

    def normalize_year(self, ano):
        CURRENT_YY = datetime.now().year % 100
        def normalize_year(year):
            if year >= 100:
                return year

            if year <= CURRENT_YY:
                return 2000 + year
            return 1900 + year




    def get_col(self, ws, col_number, line_number)-> tuple:
        return next(ws.iter_cols(min_col=col_number, max_col=col_number, min_row=line_number, values_only=True))

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