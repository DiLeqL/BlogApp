import pytest
from aiohttp import web
import main
import asyncpg
import testing.postgresql


def setUp():
    postgresql = testing.postgresql.Postgresql(port=7654)
    # Get the url to connect to with psycopg2 or equivalent
    print(postgresql.url())


async def test_get_posts(aiohttp_client):
    app = web.Application()
    app.add_routes([web.get('/posts', main.get_posts)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    print(type(aiohttp_client))
    resp = await client.get(r'/posts')
    assert resp.status == 200


async def test_get_post_by_id(aiohttp_client):
    app = web.Application()
    app.add_routes([web.get('/posts/1', main.get_post_by_id)])
    app['pool'] = await asyncpg.create_pool('postgresql://admin:postgres@localhost/blog_db')
    client = await aiohttp_client(app)
    print(type(aiohttp_client))
    resp = await client.get(r'/posts/1')
    assert resp.status == 200


def tearDown():
    postgresql.stop()
