async def get_posts(con):
    posts = []
    async with con.transaction():
        async for record in con.cursor(
                'SELECT * FROM blog inner join author a on blog.author_id = a.id'):
            posts.append(dict(record))
    return posts


async def get_post_by_id(con, post_id):
    async with con.transaction():
        stmt = await con.prepare('SELECT * FROM blog inner join author a on blog.author_id = a.id where blog.id = $1')
        post = await stmt.fetchrow(post_id)
        return dict(post)

