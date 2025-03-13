import scrapy

class EventItem(scrapy.Item):
    # Informações básicas do evento
    title = scrapy.Field()  # Nome do evento
    event_id = scrapy.Field()  # ID único do evento
    event_type = scrapy.Field()  # Tipo de evento (ex: show, festival, etc.)
    url = scrapy.Field()  # URL do evento
    start_date = scrapy.Field()  # Data de início do evento
    end_date = scrapy.Field()  # Data de término do evento
    place_name = scrapy.Field()  # Nome do local do evento
    address = scrapy.Field()  # Endereço completo do local
    city = scrapy.Field()  # Cidade do evento
    state = scrapy.Field()  # Estado do evento
    image_url = scrapy.Field()  # URL da imagem principal do evento
    image_thumb_url = scrapy.Field()  # URL da miniatura da imagem
    synopsis = scrapy.Field()  # Sinopse ou descrição do evento
    duration = scrapy.Field()  # Duração do evento
    purchase_url = scrapy.Field()  # URL para compra de ingressos
    source = scrapy.Field()  # Fonte dos dados (ex: "ingressos")