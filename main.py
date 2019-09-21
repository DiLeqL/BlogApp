from aiohttp import web
import asyncpg
import asyncio
import blog_repository

routes = web.RouteTableDef()


@routes.get(r'/posts')
async def get_posts(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await blog_repository.get_posts(connection)
            return web.Response(text=str(result))


@routes.get(r'/posts/{id}')
async def get_post_by_id(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await blog_repository.get_post_by_id(connection, int(request.match_info['id']))
            return web.Response(text=str(result))


async def init_app():
    app = web.Application()
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    app.add_routes(routes)
    return app

loop = asyncio.get_event_loop()
application = loop.run_until_complete(init_app())
web.run_app(application)
