import asyncio
import asyncpg


async def init_db():
    conn = await asyncpg.connect('postgresql://admin:postgres@localhost/blog_db')

    await conn.execute('''
                CREATE TABLE author(
                    id serial PRIMARY KEY,
                    name text
                )
            ''')

    await conn.execute('''
        CREATE TABLE blog(
            id serial PRIMARY KEY,
            title text,
            body text,
            author_id int,
            created_at timestamp,
            
            FOREIGN KEY (author_id) REFERENCES author (id)
        )
    ''')

    await conn.execute('''
                INSERT INTO author(name) VALUES($1)
            ''', 'Джон Федор')

    await conn.execute('''
        INSERT INTO blog(title, body, author_id, created_at) VALUES($1, $2, $3, CURRENT_TIMESTAMP)
    ''', 'Заголовок 1', 'Тело поста 1', 1)

    # Select a row from the table.
    # row = await conn.fetchrow(
    #     'SELECT * FROM users WHERE name = $1', 'Bob')
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))

    # Close the connection.
    await conn.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init_db())

