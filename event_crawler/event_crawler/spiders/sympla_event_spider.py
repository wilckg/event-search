import scrapy
from event_crawler.items import EventItem
import json
import logging

class SymplaSpider(scrapy.Spider):
    name = "sympla_spider"
    api_url = "https://www.sympla.com.br/api/discovery-bff/search-closed/event?page={page}"
    start_page = 1  # Começa na página 1
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOAD_DELAY': 10,  # Aumente o delay entre as requisições
    }

    def start_requests(self):
        # Inicia as requisições para a API
        headers = {
            'Accept': 'application/json',
            'Referer': 'https://www.sympla.com.br/',
            'Origin': 'https://www.sympla.com.br',
            'User-Agent': self.settings.get('USER_AGENT'),  # Usa o USER_AGENT do custom_settings
        }
        url = self.api_url.format(page=self.start_page)
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

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
        if 'data' in data and isinstance(data['data'], list):
            for event in data['data']:
                item = EventItem()
                
                try:
                    # Informações básicas do evento
                    item['name'] = event.get('name', '').strip()
                    item['event_id'] = event.get('id')  # Não usar .strip() para números
                    item['event_type'] = event.get('event_type', '').strip()
                    item['company'] = event.get('company', '').strip()
                    item['url'] = event.get('url', '').strip()

                    # Datas do evento
                    item['start_date'] = event.get('start_date', '').strip()
                    item['end_date'] = event.get('end_date', '').strip()
                    item['start_date_formats'] = event.get('start_date_formats', {})
                    item['end_date_formats'] = event.get('end_date_formats', {})

                    # Localização do evento
                    location = event.get('location', {})
                    item['location_name'] = location.get('name', '').strip()
                    item['address'] = location.get('address', '').strip()
                    item['address_num'] = location.get('address_num', '').strip()
                    item['neighborhood'] = location.get('neighborhood', '').strip()
                    item['city'] = location.get('city', '').strip()
                    item['state'] = location.get('state', '').strip()
                    item['zip_code'] = location.get('zip_code', '').strip()
                    item['country'] = location.get('country', '').strip()
                    item['latitude'] = location.get('lat')  # Não usar .strip() para números
                    item['longitude'] = location.get('lon')  # Não usar .strip() para números

                    # Organizador do evento
                    organizer = event.get('organizer', {})
                    item['organizer_name'] = organizer.get('name', '').strip()
                    item['organizer_id'] = organizer.get('id')  # Não usar .strip() para números
                    item['organizer_email'] = organizer.get('email', '').strip()
                    item['organizer_range'] = organizer.get('organizer_range', '').strip()
                    item['organizer_range_id'] = organizer.get('organizer_range_id')  # Não usar .strip() para números

                    # Imagens do evento
                    images = event.get('images', {})
                    item['image_original'] = images.get('original', '').strip()
                    item['image_xs'] = images.get('xs', '').strip()
                    item['image_lg'] = images.get('lg', '').strip()

                    # Outros campos
                    item['global_score_norm'] = event.get('global_score_norm')  # Não usar .strip() para números
                    item['duration_type'] = event.get('duration_type', '').strip()

                    yield item
                except Exception as e:
                    logging.error(f"Erro ao processar evento: {e}")

            # Verificar se há mais páginas
            current_page = int(response.url.split('page=')[-1])  # Extrai o número da página atual
            next_page = current_page + 1  # Incrementa para a próxima página

            # Verificar se há mais eventos (supondo que a API retorne uma lista vazia quando não há mais eventos)
            if data['data']:  # Se houver eventos na página atual
                next_page_url = self.api_url.format(page=next_page)
                logging.info(f"Próxima página: {next_page_url}")
                headers = {
                    'Accept': 'application/json',
                    'Referer': 'https://www.sympla.com.br/',
                    'Origin': 'https://www.sympla.com.br',
                    'User-Agent': self.settings.get('USER_AGENT'),  # Usa o USER_AGENT do custom_settings
                }
                yield scrapy.Request(url=next_page_url, headers=headers, callback=self.parse)
            else:
                logging.info("Não há mais páginas ou a resposta está vazia.")
        else:
            logging.error(f"Resposta da API inválida: {data}")