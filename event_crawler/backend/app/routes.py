from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import get_db_connection
from .models import Event
from .filters import apply_filters

app = Flask(__name__)
CORS(app)

@app.route('/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    # Parâmetros de paginação
    page = int(request.args.get('page', 1))  # Página atual (padrão: 1)
    per_page = int(request.args.get('per_page', 10))  # Itens por página (padrão: 10)

    # Filtros
    filters = request.args.to_dict()
    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if 'city' in filters:
        query += " AND city LIKE %s"
        params.append(f"%{filters['city']}%")  # Adiciona % para busca parcial
    if 'state' in filters:
        query += " AND state LIKE %s"
        params.append(f"%{filters['state']}%")  # Adiciona % para busca parcial
    if 'source' in filters:
        query += " AND source LIKE %s"
        params.append(f"%{filters['source']}%")  # Adiciona % para busca parcial
    if 'start_date' in filters:
        query += " AND start_date >= %s"
        params.append(filters['start_date'])
    if 'end_date' in filters:
        query += " AND end_date <= %s"
        params.append(filters['end_date'])

    # Paginação
    offset = (page - 1) * per_page
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    print("Essa é a query executada: ", query)

    cursor = conn.cursor()
    cursor.execute(query, params)
    events_data = cursor.fetchall()

    # Contar o total de eventos (para calcular o total de páginas)
    count_query = "SELECT COUNT(*) as total FROM events WHERE 1=1"
    count_params = []

    if 'city' in filters:
        count_query += " AND city LIKE %s"
        count_params.append(f"%{filters['city']}%")  # Adiciona % para busca parcial
    if 'state' in filters:
        count_query += " AND state LIKE %s"
        count_params.append(f"%{filters['state']}%")  # Adiciona % para busca parcial
    if 'source' in filters:
        count_query += " AND source LIKE %s"
        count_params.append(f"%{filters['source']}%")  # Adiciona % para busca parcial
    if 'start_date' in filters:
        count_query += " AND start_date >= %s"
        count_params.append(filters['start_date'])
    if 'end_date' in filters:
        count_query += " AND end_date <= %s"
        count_params.append(filters['end_date'])

    cursor.execute(count_query, count_params)
    total_events = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    # Converter os dados em objetos Event
    events = [
        Event(
            id=event['id'],
            title=event['title'],
            event_id=event['event_id'],
            event_type=event['event_type'],
            url=event['url'],
            start_date=event['start_date'],
            end_date=event['end_date'],
            place_name=event['place_name'],
            address=event['address'],
            city=event['city'],
            state=event['state'],
            country=event.get('country', ''),  # Use .get() para campos opcionais
            image_url=event['image_url'],
            image_thumb_url=event['image_thumb_url'],
            synopsis=event['synopsis'],
            duration=event['duration'],
            purchase_url=event['purchase_url'],
            source=event['source']
        ) for event in events_data
    ]

    # Converter os eventos em JSON
    events_json = [
        {
            "id": event.id,
            "title": event.title,
            "event_id": event.event_id,
            "event_type": event.event_type,
            "url": event.url,
            "start_date": event.start_date,
            "end_date": event.end_date,
            "place_name": event.place_name,
            "address": event.address,
            "city": event.city,
            "state": event.state,
            "country": event.country,
            "image_url": event.image_url,
            "image_thumb_url": event.image_thumb_url,
            "synopsis": event.synopsis,
            "duration": event.duration,
            "purchase_url": event.purchase_url,
            "source": event.source
        } for event in events
    ]

    # Calcular o total de páginas
    total_pages = (total_events + per_page - 1) // per_page

    # Retornar os eventos com informações de paginação
    return jsonify({
        "events": events_json,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_events": total_events,
            "total_pages": total_pages
        }
    })