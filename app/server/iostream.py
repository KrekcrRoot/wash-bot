from aiohttp import web

async def handle_notification(request):
    data = await request.json()
    
    # Make something with data
    print(data)

    return web.Response()

async def machine_break(request):
    data = await request.json()
    
    # Make something with data
    print(data)

    return web.Response()


app = web.Application()

app.add_routes([
    web.post('/notification', handler=handle_notification),
    web.post('/machine/break', handler=machine_break)
])
