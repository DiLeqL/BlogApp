from aiohttp import web
import asyncpg
import asyncio
import blog_repository
import ast
import validation
import json
import sql_contract

routes = web.RouteTableDef()


@routes.get(r'/posts')
async def get_posts(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        result = await blog_repository.get_posts(connection)
        return web.json_response(result)


@routes.get(r'/posts/{id}')
async def get_post_by_id(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        result = await blog_repository.get_post_by_id(connection, int(request.match_info['id']))
        if result is not None:
            return web.json_response(result)
        else:
            return web.Response(status=400, text='Некорректные данные')


@routes.post(r'/posts')
async def add_post(request):
    content = await request.content.read()
    if not await validation.validate_post_fields(str(content, 'UTF-8')):
        return web.Response(status=400, text='Некорректные данные')

    pool = request.app['pool']
    async with pool.acquire() as connection:
        request_body = json.loads(content)
        author_id = await blog_repository.get_author_id_by_name(connection, request_body['author'])
        post_json = await blog_repository.add_post(connection, request_body, author_id)
        return web.json_response(post_json, status=201)


@routes.put(r'/posts/{id}')
async def update_post(request):
    content = await request.content.read()
    if not await validation.validate_post_fields(str(content, 'UTF-8')):
        return web.Response(status=400, text='Некорректные данные')

    pool = request.app['pool']
    async with pool.acquire() as connection:
        request_body = json.loads(content)
        request_body['id'] = request.match_info['id']
        author_id = await blog_repository.get_author_id_by_name(connection, request_body['author'])
        result = await blog_repository.update_post(connection, request_body, author_id)
        return web.json_response(result, status=200)


async def get_app():
    app = web.Application()
    app['pool'] = await asyncpg.create_pool(sql_contract.CONNECTION_STRING)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    application = loop.run_until_complete(get_app())
    web.run_app(application)
