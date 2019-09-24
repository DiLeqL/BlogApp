import pytest
import main

@pytest.fixture
async def client_fixture(aiohttp_client):
    app = await main.get_app()
    return await aiohttp_client(app)


async def test_get_posts_status_200(client_fixture):
    resp = await client_fixture.get(r'/posts')
    assert resp.status == 200


async def test_get_post_by_id_200(client_fixture):
    resp = await client_fixture.get(r'/posts/1')
    assert resp.status == 200


async def test_get_post_by_id_status_400(client_fixture):
    resp = await client_fixture.get(r'/posts/100')
    assert resp.status == 400


async def test_add_post_status_201(client_fixture):
    post_info = '{"title": "Заголовок 7", "body": "Тело поста 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client_fixture.post(r'/posts', data=post_info)
    assert resp.status == 201


async def test_add_post_status_400_no_title(client_fixture):
    post_info = '{"body" : "Тело поста 54","author" : "Автор 51","created_at" : "2019-10-21T15:39:14.342Z"}'
    resp = await client_fixture.post(r'/posts', data=post_info)
    assert resp.status == 400


async def test_update_post_status_200(client_fixture):
    post_info = '{"title": "Заголовок 7", "body": "Тело поста 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client_fixture.put(r'/posts/1', data=post_info)
    assert resp.status == 200


async def test_update_post_status_400_no_body(client_fixture):
    post_info = '{"title": "Заголовок 7", "author": "Автор 7", "created_at": ' \
                '"2019-09-22T15:40:14.341Z"}'
    resp = await client_fixture.put(r'/posts/1', data=post_info)
    assert resp.status == 400
