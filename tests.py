from aiohttp import web
import main
import asyncpg


# def setUp(self):
#     self.postgresql = testing.postgresql.Postgresql(port=7654)
#     # Get the url to connect to with psycopg2 or equivalent
#     print(self.postgresql.url())


async def test_get_posts_status_200(aiohttp_client):
    app = web.Application()
    app.add_routes([web.get('/posts', main.get_posts)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    resp = await client.get(r'/posts')
    assert resp.status == 200


async def test_get_post_by_id_200(aiohttp_client):
    app = web.Application()
    app.add_routes([web.get('/posts/{id}', main.get_post_by_id)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    resp = await client.get(r'/posts/1')
    assert resp.status == 200


async def test_get_post_by_id_status_500(aiohttp_client):
    app = web.Application()
    app.add_routes([web.get('/posts/{id}', main.get_post_by_id)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    resp = await client.get(r'/posts/100')
    assert resp.status == 500


async def test_add_post_status_201(aiohttp_client):
    app = web.Application()
    app.add_routes([web.post('/posts', main.add_post)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    post_info = '{"title": "Заголовок 7", "body": "Тело поста 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client.post(r'/posts', data=post_info)
    assert resp.status == 201


async def test_add_post_status_400_no_title(aiohttp_client):
    app = web.Application()
    app.add_routes([web.post('/posts', main.add_post)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    post_info = '{"body" : "Тело поста 54","author" : "Автор 51","created_at" : "2019-10-21T15:39:14.342Z"}'
    resp = await client.post(r'/posts', data=post_info)
    assert resp.status == 400


async def test_update_post_status_200(aiohttp_client):
    app = web.Application()
    app.add_routes([web.put('/posts/{id}', main.update_post)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    post_info = '{"title": "Заголовок 7", "body": "Тело поста 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client.put(r'/posts/1', data=post_info)
    assert resp.status == 200


async def test_update_post_status_400_no_body(aiohttp_client):
    app = web.Application()
    app.add_routes([web.put('/posts/{id}', main.update_post)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    post_info = '{"title": "Заголовок 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client.put(r'/posts/1', data=post_info)
    assert resp.status == 400

# def tearDown(self):
#     self.postgresql.stop()
