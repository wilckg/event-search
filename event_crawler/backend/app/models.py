class Event:
    def __init__(self, id, title, event_id, event_type, url, start_date, end_date, place_name, address, city, state, country, image_url, image_thumb_url, synopsis, duration, purchase_url, source):
        self.id = id
        self.title = title
        self.event_id = event_id
        self.event_type = event_type
        self.url = url
        self.start_date = start_date
        self.end_date = end_date
        self.place_name = place_name
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.image_url = image_url
        self.image_thumb_url = image_thumb_url
        self.synopsis = synopsis
        self.duration = duration
        self.purchase_url = purchase_url
        self.source = source