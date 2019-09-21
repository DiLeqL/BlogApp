async def get_posts(con):
    rows = await con.fetchrow('SELECT * FROM blog left join author a on blog.author_id = a.id')
    return dict(rows)
