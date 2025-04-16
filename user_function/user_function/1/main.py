def handler(event):
    return {"message": f"Hello, {event.get('name', 'World')}!"}
