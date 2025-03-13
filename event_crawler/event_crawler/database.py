import mysql.connector

def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="wilck",
        password="3696",
        database="projeto_integrador"
    )
    return conn

def insert_event(conn, event):
    cursor = conn.cursor()
    query = """
    INSERT IGNORE INTO events (
        title, event_id, event_type, url, start_date, end_date, place_name, address, city, state, 
        image_url, image_thumb_url, synopsis, duration, purchase_url, source
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        event['title'], event['event_id'], event['event_type'], event['url'], event['start_date'],
        event['end_date'], event['place_name'], event['address'], event['city'], event['state'],
        event['image_url'], event['image_thumb_url'], event['synopsis'], event['duration'],
        event['purchase_url'], event['source']
    ))
    conn.commit()
    cursor.close()