import scrapy
from event_crawler.ingressos_items import EventItem
import json
import logging
from event_crawler.database import connect_to_db, create_table, insert_event

class IngressosSpider(scrapy.Spider):
    name = "ingressos_spider"
    api_url = "https://www.ingresso.com/api/events?event_type=&per_page=99999"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 10,
    }

    def __init__(self, *args, **kwargs):
        super(IngressosSpider, self).__init__(*args, **kwargs)
        self.conn = connect_to_db()
        create_table(self.conn)

    def close(self, reason):
        self.conn.close()

    def start_requests(self):
        headers = {
            'Accept': 'application/json',
            'User-Agent': self.settings.get('USER_AGENT'),
        }
        yield scrapy.Request(url=self.api_url, headers=headers, callback=self.parse)

    def check_event_exists(self, conn, event_id):
        cursor = conn.cursor()
        query = "SELECT id FROM events WHERE event_id = ?"
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def parse(self, response):
        logging.info(f"Requisição para: {response.url}")
        logging.info(f"Status da resposta: {response.status}")

        if response.status != 200:
            logging.error(f"Erro na requisição: Status {response.status}")
            return

        if not response.text:
            logging.error("Resposta vazia recebida.")
            return
        
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            logging.error(f"Resposta recebida: {response.text}")
            return

        if 'events' in data and isinstance(data['events'], list):
            for event in data['events']:
                item = EventItem()
                
                event_id = event.get('id')
                
                if self.check_event_exists(self.conn, event_id):
                    logging.info(f"Evento {event_id} já existe no banco de dados. Ignorando.")
                    continue
                
                try:
                    item['title'] = event.get('title', '').strip()
                    item['event_id'] = event.get('id')
                    item['event_type'] = event.get('event_type', {}).get('name', '').strip()
                    item['url'] = event.get('url', '').strip()
                    item['start_date'] = event.get('start_date', '').strip()
                    item['end_date'] = event.get('end_date', '').strip()
                    item['place_name'] = event.get('place', {}).get('name', '').strip()
                    item['address'] = event.get('place', {}).get('full_address', '').strip()
                    item['city'] = event.get('place', {}).get('city', {}).get('name', '').strip()
                    item['state'] = event.get('place', {}).get('state', {}).get('name', '').strip()
                    item['image_url'] = event.get('image', {}).get('url', '').strip()
                    item['image_thumb_url'] = event.get('image', {}).get('thumb', {}).get('url', '').strip()
                    item['synopsis'] = event.get('synopsis', '').strip()
                    item['duration'] = event.get('duration', '').strip()
                    item['purchase_url'] = event.get('purchase_url', '').strip()
                    item['source'] = "ingressos"  # Identifica a fonte dos dados

                    # Salvar no banco de dados
                    insert_event(self.conn, item)
                except Exception as e:
                    logging.error(f"Erro ao processar evento: {e}")
        else:
            logging.error(f"Resposta da API inválida: {data}")