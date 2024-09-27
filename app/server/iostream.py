from aiohttp import web

async def handle_notification(request):
    data = await request.json()
    
    # Make something with data

    return web.Response()


app = web.Application()

app.add_routes([
    web.post('/notification', handler=handle_notification)
])
