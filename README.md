
# Bank Statement Manager (BSM)

![Python](https://img.shields.io/badge/Python-3-blue)
![PySide6](https://img.shields.io/badge/Interface-PySide6-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Devbrax](https://img.shields.io/badge/Developed%20by-Devbrax-orange)

**Bank Statement Manager (BSM)** é uma aplicação desktop desenvolvida em Python para ler, importar e armazenar informações de extratos bancários com formatos variados.

Seu objetivo é consolidar as movimentações de diferentes contas bancárias em uma base de dados local, permitindo realizar consultas, analisar dados consolidados e verificar lançamentos financeiros de maneira organizada, independentemente da estrutura original dos extratos.

---

## Download do Executável (.exe)

Se você deseja utilizar o BSM no Windows sem precisar instalar Python ou configurar dependências:

[**Clique aqui para baixar o executável (.exe) na seção de Releases**](../../releases)

O executável será disponibilizado nessa seção após a publicação da primeira versão.

---

## Funcionalidades

- **Gerenciamento de Contas Bancárias:** cadastro e organização de múltiplas contas bancárias.
- **Importação de Extratos Excel:** leitura de arquivos nos formatos `.xls` e `.xlsx`.
- **Layouts Configuráveis:** configuração das estruturas dos extratos para identificar corretamente datas, descrições e valores, mesmo quando os bancos utilizam formatos diferentes.
- **Controle de Duplicidade:** identificação de lançamentos já importados, evitando duplicações entre importações de períodos sobrepostos.
- **Consolidação de Dados:** armazenamento padronizado das movimentações importadas em uma base de dados local.
- **Consultas e Pesquisas:** visualização das movimentações financeiras de cada conta.
- **Filtros Dinâmicos:** pesquisas por data, descrição e valor, com possibilidade de combinar diferentes condições.
- **Ordenação de Resultados:** organização dos lançamentos pelas colunas da consulta.
- **Resumos Financeiros:** apresentação de entradas, saídas e resultados consolidados.
- **Exportação para Excel:** geração de planilhas com os resultados das pesquisas.
- **Armazenamento Local:** utilização de SQLite, sem necessidade de servidor de banco de dados.

---

## Tecnologias e Bibliotecas Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica:** PySide6 (Qt)
- **Banco de Dados:** SQLite
- **Leitura e Exportação de Excel:** openpyxl
- **Leitura de Arquivos XLS:** xlrd
- **Compilação do Executável:** PyInstaller

---

## Como Executar o Código-Fonte

Caso queira executar o BSM diretamente pelo código-fonte:

### Pré-requisitos

- Python 3 instalado.
- Git para clonar o repositório, ou download do código-fonte em ZIP.

### Passo a passo

**1. Clone o repositório:**

```bash
git clone https://github.com/Fabiorsc/bank-statement-manager.git
```

**2. Acesse a pasta do projeto:**

```bash
cd bank-statement-manager
```

**3. Crie um ambiente virtual:**

```bash
python -m venv .venv
```

**4. Ative o ambiente virtual no Windows:**

```powershell
.venv\Scripts\activate
```

**5. Instale as dependências:**

```bash
python -m pip install -r requirements.txt
```

**6. Execute a aplicação:**

```bash
python main.py
```

O banco de dados SQLite será criado automaticamente na primeira execução, caso ainda não exista.

---

## Como Gerar o Executável (.exe)

O BSM pode ser compilado para Windows utilizando o PyInstaller.

**1. Instale o PyInstaller:**

```bash
python -m pip install pyinstaller
```

**2. Na raiz do projeto, execute:**

```bash
python -m PyInstaller --onefile --windowed --name BSM main.py
```

**3. Localize o executável:**

O arquivo será gerado em:

```text
dist/BSM.exe
```

O PyInstaller também gera um arquivo `BSM.spec`, que pode ser utilizado para personalizar e reproduzir futuras compilações.

---

## Estrutura do Projeto

```text
bank-statement-manager/
├── database/          # Banco de dados e repositórios
├── domain/            # Regras de domínio e filtros
│   └── filters/       # Filtros de consulta
├── excel/             # Leitura, importação e exportação Excel
├── infra/             # Caminhos e configuração de logs
├── ui/                # Interface gráfica e componentes
├── main.py            # Ponto de entrada da aplicação
├── requirements.txt   # Dependências Python
├── README.md          # Documentação do projeto
└── LICENSE            # Licença MIT
```

---

## Licença

Este projeto está licenciado sob a **MIT License**.

Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

---

## Contato e Suporte

Desenvolvido por **Devbrax**.

- **E-mail:** devbrax.software@gmail.com
- **GitHub:** https://github.com/Fabiorsc
