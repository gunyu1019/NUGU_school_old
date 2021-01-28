from sanic import response

async def health(requests):
    return response.text('OK',status=200)