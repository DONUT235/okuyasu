import asyncpg
import asyncio

class PSQLConnectionSingleton:
    def __init__(self):
        self.connection = None

    async def get_connection(self):
        if self.connection is None:
            self.connection = await asyncpg.connect(database='okuyasu')
            print(self.connection)

    async def get_banned_words_for_server(self, server_id):
        return await self.connection.fetch(
            'SELECT * FROM banned_phrases'
            + ' JOIN servers ON banned_phrases.discord_id = $1',
            server_id
        )

    async def ban_phrase(self, server_id, phrase):
        await self.connection.execute(
            'INSERT INTO banned_phrases (discord_id, value)'
            + ' VALUES ($1, $2)',
            server_id, phrase
        )

    async def create_server(server_id):
        await self.connection.execute(
            'INSERT INTO servers (discord_id) VALUES ($1)',
            server_id
        )

db = PSQLConnectionSingleton()

async def main():
    conn = PSQLConnectionSingleton()
    await conn.get_connection()
    for row in await conn.get_banned_words_for_server('123'):
        print(row['value'])

if __name__ == '__main__':
    asyncio.run(main())
