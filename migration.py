import asyncio
import asyncpg
import sql_contract


async def init_db():
    conn = await asyncpg.connect(sql_contract.CONNECTION_STRING)

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
                    INSERT INTO author(name) VALUES($1)
                ''', 'Автор 2')

    await conn.execute('''
        INSERT INTO blog(title, body, author_id, created_at) VALUES($1, $2, $3, CURRENT_TIMESTAMP)
    ''', 'Заголовок 1', 'Тело поста 1', 1)

    await conn.execute('''
        INSERT INTO blog(title, body, author_id, created_at) VALUES($1, $2, $3, CURRENT_TIMESTAMP)
        ''', 'Заголовок 2', 'Тело поста 2', 1)

    await conn.execute('''
            INSERT INTO blog(title, body, author_id, created_at) VALUES($1, $2, $3, CURRENT_TIMESTAMP)
            ''', 'Заголовок 3', 'Тело поста 3', 2)

    await conn.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init_db())

