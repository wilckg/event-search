import scrapy
from event_crawler.ingressos_items import EventItem
import json
import logging

class IngressosSpider(scrapy.Spider):
    name = "ingressos_spider"
    api_url = "https://www.ingresso.com/api/events?event_type=&per_page=99999"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 10,  # Aumente o delay entre as requisições
    }

    def start_requests(self):
        # Inicia as requisições para a API
        headers = {
            'Accept': 'application/json',
            'User-Agent': self.settings.get('USER_AGENT'),  # Usa o USER_AGENT do custom_settings
        }
        yield scrapy.Request(url=self.api_url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Processar a resposta da API
        logging.info(f"Requisição para: {response.url}")
        logging.info(f"Status da resposta: {response.status}")
        logging.info(f"Resposta bruta: {response.text}")  # Log da resposta bruta

        if response.status != 200:
            logging.error(f"Erro na requisição: Status {response.status}")
            return

        if not response.text:
            logging.error("Resposta vazia recebida.")
            return
        
        try:
            data = json.loads(response.text)  # Converte a resposta JSON em um dicionário Python
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            logging.error(f"Resposta recebida: {response.text}")
            return

        # Extrair eventos da resposta
        if 'events' in data and isinstance(data['events'], list):
            for event in data['events']:
                item = EventItem()
                
                try:
                    # Informações básicas do evento
                    item['title'] = event.get('title', '').strip()
                    item['event_id'] = event.get('id')  # Não usar .strip() para números
                    item['event_type'] = event.get('event_type', {}).get('name', '').strip()
                    item['url'] = event.get('url', '').strip()

                    # Datas do evento
                    item['start_date'] = event.get('start_date', '').strip()
                    item['end_date'] = event.get('end_date', '').strip()

                    # Localização do evento
                    place = event.get('place', {})
                    item['place_name'] = place.get('name', '').strip()
                    item['address'] = place.get('full_address', '').strip()
                    item['city'] = place.get('city', {}).get('name', '').strip()
                    item['state'] = place.get('state', {}).get('name', '').strip()

                    # Imagens do evento
                    image = event.get('image', {})
                    item['image_url'] = image.get('url', '').strip()
                    item['image_thumb_url'] = image.get('thumb', {}).get('url', '').strip()

                    # Outros campos
                    item['synopsis'] = event.get('synopsis', '').strip()
                    item['duration'] = event.get('duration', '').strip()
                    item['purchase_url'] = event.get('purchase_url', '').strip()

                    yield item
                except Exception as e:
                    logging.error(f"Erro ao processar evento: {e}")
        else:
            logging.error(f"Resposta da API inválida: {data}")