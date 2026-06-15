import sqlite3
from infra.app_paths import change_root_folder

DB_NAME = "dados.db"

def get_connection():
    db_path = change_root_folder(DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn