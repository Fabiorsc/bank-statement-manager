import json
import os
import uuid


ARQUIVO_CONFIG = "config.json"

def carregar_config():
    if not os.path.exists(ARQUIVO_CONFIG):
        return {"bancos": []}

    with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_config(dados):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def adicionar_conta(nome_banco, agencia, conta, apelido):
    dados = carregar_config()

    # procura banco
    banco = next((b for b in dados["bancos"] if b["nome"] == nome_banco), None)

    if not banco:
        banco = {"nome": nome_banco, "contas": []}
        dados["bancos"].append(banco)

    banco["contas"].append({
        "id": str(uuid.uuid4()),
        "agencia": agencia,
        "conta": conta,
        "apelido": apelido
    })

    salvar_config(dados)

