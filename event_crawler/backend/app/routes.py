# -*- coding: utf-8 -*-
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

    cursor = conn.cursor(dictionary=True)

    # Consulta SQL com paginação
    offset = (page - 1) * per_page
    query = "SELECT * FROM events LIMIT %s OFFSET %s"
    cursor.execute(query, (per_page, offset))
    events_data = cursor.fetchall()

    # Contar o total de eventos (para calcular o total de páginas)
    cursor.execute("SELECT COUNT(*) as total FROM events")
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
            country=event['country'],
            image_url=event['image_url'],
            image_thumb_url=event['image_thumb_url'],
            synopsis=event['synopsis'],
            duration=event['duration'],
            purchase_url=event['purchase_url'],
            source=event['source']
        ) for event in events_data
    ]

    # Aplicar filtros (se necessário)
    filters = request.args.to_dict()
    filtered_events = apply_filters(events, filters)

    # Converter os eventos filtrados em JSON
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
        } for event in filtered_events
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