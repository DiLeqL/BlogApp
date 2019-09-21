from aiohttp import web
import asyncpg
import asyncio
import blog_repository

routes = web.RouteTableDef()


@routes.get(r'/post')
async def get_posts(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            # Run the query passing the request argument.
            result = await blog_repository.get_posts(connection)
            return web.Response(text=str(result))


async def init_app():
    app = web.Application()
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    app.add_routes(routes)
    return app

loop = asyncio.get_event_loop()
application = loop.run_until_complete(init_app())
web.run_app(application)
