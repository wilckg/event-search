import sqlite3

# Função para conectar ao banco de dados SQLite
def connect_to_db():
    conn = sqlite3.connect('projeto_integrador.db')
    return conn

# Função para criar a tabela (executa apenas na primeira vez)
def create_table(conn):
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        event_id TEXT UNIQUE,
        event_type TEXT,
        url TEXT,
        start_date TEXT,
        end_date TEXT,
        place_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        image_url TEXT,
        image_thumb_url TEXT,
        synopsis TEXT,
        duration TEXT,
        purchase_url TEXT,
        source TEXT
    )
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()

# Função para inserir um evento
def insert_event(conn, event):
    cursor = conn.cursor()
    query = """
    INSERT OR IGNORE INTO events (
        title, event_id, event_type, url, start_date, end_date, place_name, address, city, state, 
        image_url, image_thumb_url, synopsis, duration, purchase_url, source
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        event['title'], event['event_id'], event['event_type'], event['url'], event['start_date'],
        event['end_date'], event['place_name'], event['address'], event['city'], event['state'],
        event['image_url'], event['image_thumb_url'], event['synopsis'], event['duration'],
        event['purchase_url'], event['source']
    ))
    conn.commit()
    cursor.close()
