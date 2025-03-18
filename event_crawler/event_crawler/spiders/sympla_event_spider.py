import scrapy
from event_crawler.items import EventItem
import json
import logging
from event_crawler.database import connect_to_db, create_table, insert_event

class SymplaSpider(scrapy.Spider):
    name = "sympla_spider"
    api_url = "https://www.sympla.com.br/api/discovery-bff/search-closed/event?page={page}"
    start_page = 1
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 10,
    }

    def __init__(self, *args, **kwargs):
        super(SymplaSpider, self).__init__(*args, **kwargs)
        self.conn = connect_to_db()
        create_table(self.conn)

    def close(self, reason):
        self.conn.close()

    def start_requests(self):
        headers = {
            'Accept': 'application/json',
            'Referer': 'https://www.sympla.com.br/',
            'Origin': 'https://www.sympla.com.br',
            'User-Agent': self.settings.get('USER_AGENT'),
        }
        url = self.api_url.format(page=self.start_page)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def check_event_exists(self, conn, event_id):
        cursor = conn.cursor()
        query = "SELECT id FROM events WHERE event_id = %s"
        cursor.execute(query, (str(event_id),))
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

        if 'data' in data and isinstance(data['data'], list):
            for event in data['data']:
                item = EventItem()
                
                event_id = event.get('id')
                
                if self.check_event_exists(self.conn, event_id):
                    logging.info(f"Evento {event_id} já existe no banco de dados. Ignorando.")
                    continue
                
                try:
                    item['title'] = event.get('name', '').strip()
                    item['event_id'] = event.get('id')
                    item['event_type'] = event.get('event_type', '').strip()
                    item['url'] = event.get('url', '').strip()
                    item['start_date'] = event.get('start_date', '').strip()
                    item['end_date'] = event.get('end_date', '').strip()
                    item['place_name'] = event.get('location', {}).get('name', '').strip()
                    item['address'] = event.get('location', {}).get('address', '').strip()
                    item['city'] = event.get('location', {}).get('city', '').strip()
                    item['state'] = event.get('location', {}).get('state', '').strip()
                    item['image_url'] = event.get('images', {}).get('original', '').strip()
                    item['image_thumb_url'] = event.get('images', {}).get('xs', '').strip()
                    item['synopsis'] = event.get('synopsis', '').strip()
                    item['duration'] = event.get('duration', '').strip()
                    item['purchase_url'] = event.get('purchase_url', '').strip()
                    item['source'] = "sympla"  # Identifica a fonte dos dados

                    # Salvar no banco de dados
                    insert_event(self.conn, item)
                except Exception as e:
                    logging.error(f"Erro ao processar evento: {e}")

            # Verificar se há mais páginas
            current_page = int(response.url.split('page=')[-1])
            next_page = current_page + 1

            if data['data']:
                next_page_url = self.api_url.format(page=next_page)
                logging.info(f"Próxima página: {next_page_url}")
                headers = {
                    'Accept': 'application/json',
                    'Referer': 'https://www.sympla.com.br/',
                    'Origin': 'https://www.sympla.com.br',
                    'User-Agent': self.settings.get('USER_AGENT'),
                }
                yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse)
            else:
                logging.info("Não há mais páginas ou a resposta está vazia.")
        else:
            logging.error(f"Resposta da API inválida: {data}")