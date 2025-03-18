import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor

# Configurações do banco de dados (pode ser movido para variáveis de ambiente ou um arquivo de configuração)
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'postgres')  # Padrão: SQLite
POSTGRES_CONFIG = {
    'dbname': 'projeto_integrador_wg99',
    'user': 'projeto_integrador',
    'password': 'X1XeqRPEMUCAlF4AmWSYviFGclSQZ9tP',
    'host': 'dpg-cvcc60ij1k6c73c0o1jg-a',
    'port': '5432'
}
SQLITE_PATH = '../../event_crawler/projeto_integrador.db'

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados, dependendo da configuração.
    """
    if DATABASE_TYPE == 'postgres':
        try:
            # Conecta ao banco de dados PostgreSQL
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            conn.cursor_factory = DictCursor  # Configura o cursor para retornar dicionários
            return conn
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
            return None
    else:
        try:
            # Conecta ao banco de dados SQLite (ou cria se não existir)
            conn = sqlite3.connect(SQLITE_PATH)
            conn.row_factory = sqlite3.Row  # Configura o cursor para retornar dicionários
            return conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados SQLite: {e}")
            return None