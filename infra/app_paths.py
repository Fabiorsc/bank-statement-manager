from pathlib import Path
import os
import sys


APP_NAME = "BSM"


def get_app_data_folder() -> Path:
    """
    Retorna a pasta de dados da aplicação.

    Exemplo:
    C:\\Users\\Fabio\\AppData\\Local\\BSM
    """

    local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home()))

    app_folder = local_app_data / APP_NAME

    app_folder.mkdir(parents=True, exist_ok=True)

    return app_folder

def change_root_folder(path_name):
    """
        path_name: str - nome do arquivo, pasta ou ambos a ser utilizada (parte fiz do sistema, ex: "dados.db", "logs\\application.log", etc.)
        Retorna o caminho completo para o arquivo ou pasta, considerando o ambiente de execução (PyInstaller ou VS Code/Python).
        Quando estiver executando via PyInstaller, o caminho será relativo à pasta de dados da aplicação (ex: "C:\\Users\\Fabio\\AppData\\Local\\BSM\\" + "dados.db" ou "logs\\application.log").
        Quando estiver executando pelo VS Code ou Python, o caminho será relativo ao diretório atual, ou seja, retorna o que foi passado em path_name (ex: "dados.db" ou "logs\\application.log").
    """
    # Executando via PyInstaller
    if getattr(sys, "frozen", False):
        return get_app_data_folder() / path_name

    # Executando pelo VS Code / Python
    return Path(path_name)