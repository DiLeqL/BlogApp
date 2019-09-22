from aiohttp import web
import asyncpg
import asyncio
import blog_repository
import ast
import validation

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


@routes.post(r'/posts')
async def add_post(request):

    content = await request.content.read()
    if not await validation.validate_post_fields(str(content, 'UTF-8')):
        return web.Response(status=400, text='Некорректные данные')

    pool = request.app['pool']
    async with pool.acquire() as connection:
        async with connection.transaction():
            request_body = ast.literal_eval(str(content, 'UTF-8'))
            author_id = await blog_repository.get_author_id_by_name(connection, request_body['author'])
            post_json = await blog_repository.add_post(connection, request_body, author_id)
            return web.Response(status=201, text=str(post_json))


@routes.put(r'/posts/{id}')
async def update_post(request):

    content = await request.content.read()
    if not await validation.validate_post_fields(str(content, 'UTF-8')):
        return web.Response(status=400, text='Некорректные данные')

    pool = request.app['pool']
    async with pool.acquire() as connection:
        async with connection.transaction():
            request_body = ast.literal_eval(str(content, 'UTF-8'))
            request_body['id'] = request.match_info['id']
            author_id = await blog_repository.get_author_id_by_name(connection, request_body['author'])
            result = await blog_repository.update_post(connection, request_body, author_id)
            return web.Response(status=200, text=str(result))


async def init_app():
    app = web.Application()
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    app.add_routes(routes)
    return app


loop = asyncio.get_event_loop()
application = loop.run_until_complete(init_app())
web.run_app(application)
