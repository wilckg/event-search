import scrapy
from event_crawler.ticketmaster_items import EventItem
import json
import logging
from event_crawler.database import connect_to_db, insert_event

class TicketmasterSpider(scrapy.Spider):
    name = "ticketmaster_spider"
    api_url = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=BR&stateCode=SP&page={page}&apikey=9sI236RAIqgNVvklkw8c1kxTPo7jBBEX"
    start_page = 0
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 10,
    }

    def __init__(self, *args, **kwargs):
        super(TicketmasterSpider, self).__init__(*args, **kwargs)
        self.conn = connect_to_db()

    def close(self, reason):
        self.conn.close()

    def start_requests(self):
        headers = {
            'Accept': 'application/json',
            'User-Agent': self.settings.get('USER_AGENT'),
        }
        url = self.api_url.format(page=self.start_page)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def check_event_exists(self, conn, event_id):
        cursor = conn.cursor()
        query = "SELECT id FROM events WHERE event_id = %s"
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

        if '_embedded' in data and 'events' in data['_embedded']:
            for event in data['_embedded']['events']:
                item = EventItem()
                
                event_id = event.get('id', '').strip()
                
                if self.check_event_exists(self.conn, event_id):
                    logging.info(f"Evento {event_id} já existe no banco de dados. Ignorando.")
                    continue
                
                try:
                    # Informações básicas do evento
                    item['title'] = event.get('name', '').strip()
                    item['event_id'] = event.get('id', '').strip()
                    item['event_type'] = event.get('type', '').strip()
                    item['url'] = event.get('url', '').strip()

                    # Datas do evento
                    dates = event.get('dates', {})
                    start = dates.get('start', {})
                    item['start_date'] = start.get('localDate', '').strip()
                    item['end_date'] = start.get('localDate', '').strip()  # Ticketmaster geralmente não fornece end_date

                    # Localização do evento
                    venues = event.get('_embedded', {}).get('venues', [])
                    if venues:
                        venue = venues[0]
                        item['place_name'] = venue.get('name', '').strip()
                        item['address'] = venue.get('address', {}).get('line1', '').strip()
                        item['city'] = venue.get('city', {}).get('name', '').strip()
                        item['state'] = venue.get('state', {}).get('name', '').strip()
                        item['country'] = venue.get('country', {}).get('name', '').strip()

                    # Imagens do evento
                    images = event.get('images', [])
                    if images:
                        item['image_url'] = images[0].get('url', '').strip()
                        item['image_thumb_url'] = images[0].get('url', '').strip()  # Usando a mesma URL para thumb

                    # Outros campos
                    item['synopsis'] = event.get('info', '').strip()  # Campo 'info' pode ser usado como sinopse
                    item['duration'] = ''  # Ticketmaster não fornece duração diretamente
                    item['purchase_url'] = event.get('url', '').strip()
                    item['source'] = "ticketmaster"  # Identifica a fonte dos dados

                    # Salvar no banco de dados
                    insert_event(self.conn, item)
                except Exception as e:
                    logging.error(f"Erro ao processar evento: {e}")

            # Verificar se há mais páginas
            current_page = int(response.url.split('page=')[-1].split('&')[0])
            next_page = current_page + 1

            # Verificar se há mais eventos
            if data['_embedded']['events']:
                next_page_url = self.api_url.format(page=next_page)
                logging.info(f"Próxima página: {next_page_url}")
                headers = {
                    'Accept': 'application/json',
                    'User-Agent': self.settings.get('USER_AGENT'),
                }
                yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse)
            else:
                logging.info("Não há mais páginas ou a resposta está vazia.")
        else:
            logging.error(f"Resposta da API inválida: {data}")