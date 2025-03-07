# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EventItem(scrapy.Item):
    # Informações básicas do evento
    name = scrapy.Field()
    event_id = scrapy.Field()
    event_type = scrapy.Field()
    company = scrapy.Field()
    url = scrapy.Field()

    # Datas do evento
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    start_date_formats = scrapy.Field()
    end_date_formats = scrapy.Field()

    # Localização do evento
    location_name = scrapy.Field()
    address = scrapy.Field()
    address_num = scrapy.Field()
    neighborhood = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    country = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    # Organizador do evento
    organizer_name = scrapy.Field()
    organizer_id = scrapy.Field()
    organizer_email = scrapy.Field()
    organizer_range = scrapy.Field()
    organizer_range_id = scrapy.Field()

    # Imagens do evento
    image_original = scrapy.Field()
    image_xs = scrapy.Field()
    image_lg = scrapy.Field()

    # Outros campos
    global_score_norm = scrapy.Field()
    duration_type = scrapy.Field()