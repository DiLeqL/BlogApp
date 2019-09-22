from datetime import datetime


async def get_posts(con):
    posts = []
    async with con.transaction():
        async for record in con.cursor(
                'SELECT blog.id, title, body, a.name, created_at '
                'FROM blog inner join author a on blog.author_id = a.id'):
            post = dict(record)
            post['created_at'] = str(post['created_at'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]) + 'Z'
            posts.append(post)
    return posts


async def get_post_by_id(con, post_id):
    async with con.transaction():
        stmt = await con.prepare('SELECT blog.id, title,'
                                 'body, a.name, created_at FROM blog inner join author a on blog.author_id = a.id '
                                 'where blog.id = $1')
        post_record = await stmt.fetchrow(post_id)
        # reformat date
        if post_record is not None:
            post = dict(post_record)
            post['created_at'] = str(post['created_at'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]) + 'Z'
            return dict(post)
        else:
            return None


async def get_author_id_by_name(con, name):
    async with con.transaction():
        stmt = await con.prepare('SELECT id FROM author  where name = $1')
        author_id = await stmt.fetchrow(name)
        if not author_id:
            stmt = await con.prepare('INSERT INTO author (name) VALUES($1) '
                                     'returning id')
            author_id = await stmt.fetchval(name)
            return author_id
        else:
            return author_id['id']


async def add_post(con, post_json, author_id):
    async with con.transaction():
        stmt = await con.prepare('INSERT INTO blog (title, body, author_id, created_at) VALUES($1, $2, $3, $4) '
                                 'RETURNING id')
        post_id = await stmt.fetchval(post_json['title'],
                                      post_json['body'],
                                      author_id,
                                      datetime.strptime(post_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        post_json['id'] = post_id
        return post_json


async def update_post(con, post_json, author_id):
    async with con.transaction():
        stmt = await con.prepare('UPDATE blog SET title=$1, body=$2, author_id=$3,'
                                 ' created_at=$4 WHERE id=$5 RETURNING id')
        post_id = await stmt.fetchval(post_json['title'],
                                      post_json['body'],
                                      author_id,
                                      datetime.strptime(post_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                      int(post_json['id']))
        post_json['id'] = post_id
        return post_json
