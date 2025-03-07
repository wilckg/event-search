import scrapy

class EventItem(scrapy.Item):
    title = scrapy.Field()
    event_id = scrapy.Field()
    event_type = scrapy.Field()
    url = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    place_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    image_url = scrapy.Field()
    image_thumb_url = scrapy.Field()
    synopsis = scrapy.Field()
    duration = scrapy.Field()
    purchase_url = scrapy.Field()