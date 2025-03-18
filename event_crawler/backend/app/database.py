import sqlite3

def get_db_connection():
    try:
        # Conecta ao banco de dados SQLite (ou cria se não existir)
        conn = sqlite3.connect('../../event_crawler/projeto_integrador.db')
        conn.row_factory = sqlite3.Row  # Configura o cursor para retornar dicionários
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None