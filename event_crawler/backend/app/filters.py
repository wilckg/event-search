def apply_filters(events, filters):
    if 'city' in filters:
        events = [event for event in events if event.city == filters['city']]
    if 'state' in filters:
        events = [event for event in events if event.state == filters['state']]
    if 'source' in filters:
        events = [event for event in events if event.source == filters['source']]
    if 'start_date' in filters:
        events = [event for event in events if event.start_date >= filters['start_date']]
    if 'end_date' in filters:
        events = [event for event in events if event.end_date <= filters['end_date']]
    return events