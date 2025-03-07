import scrapy

class EventItem(scrapy.Item):
    # Informações básicas do evento
    name = scrapy.Field()  # Nome do evento
    event_id = scrapy.Field()  # ID do evento
    event_type = scrapy.Field()  # Tipo do evento (ex: "event")
    url = scrapy.Field()  # URL do evento
    locale = scrapy.Field()  # Localização do evento (ex: "en-br")

    # Datas do evento
    start_date = scrapy.Field()  # Data de início (ex: "2025-03-09")
    start_time = scrapy.Field()  # Hora de início (ex: "17:00:00")
    timezone = scrapy.Field()  # Fuso horário (ex: "America/Sao_Paulo")

    # Localização do evento
    location_name = scrapy.Field()  # Nome do local (ex: "Tokio Marine Hall")
    city = scrapy.Field()  # Cidade (ex: "São Paulo")
    state = scrapy.Field()  # Estado (ex: "São Paulo")
    country = scrapy.Field()  # País (ex: "Brazil")
    address = scrapy.Field()  # Endereço (ex: "R. Bragança Paulista 1281")
    postal_code = scrapy.Field()  # Código postal (ex: "04727-002")
    latitude = scrapy.Field()  # Latitude do local (ex: "-23.63847000")
    longitude = scrapy.Field()  # Longitude do local (ex: "-46.71997470")

    # Imagens do evento
    images = scrapy.Field()  # Lista de URLs das imagens

    # Classificações do evento
    segment = scrapy.Field()  # Segmento (ex: "Music")
    genre = scrapy.Field()  # Gênero (ex: "Classical")
    sub_genre = scrapy.Field()  # Subgênero (ex: "Classical/Vocal")