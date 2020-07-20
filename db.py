import asyncpg
from asyncpg.exceptions import UniqueViolationError
import asyncio

class PSQLConnectionSingleton:
    def __init__(self):
        self.connection = None

    async def get_connection(self):
        if self.connection is None:
            self.connection = await asyncpg.connect(database='okuyasu')
            print('Connected')

    async def get_banned_phrases_for_server(self, server_id):
        return await self.connection.fetch(
            'SELECT value FROM banned_phrases'
            + 'WHERE banned_phrases.discord_id = $1',
            server_id
        )

    async def ban_phrase(self, server_id, phrase):
        try:
            await self.connection.execute(
                'INSERT INTO banned_phrases (discord_id, value)'
                + ' VALUES ($1, $2)',
                server_id, phrase
            )
        except UniqueViolationError:
            pass

    async def unban_phrase(self, server_id, phrase):
        await self.connection.execute(
            'DELETE FROM banned_phrases'
            + ' WHERE discord_id = $1 AND value = $2',
            server_id, phrase)

db = PSQLConnectionSingleton()

async def main():
    conn = PSQLConnectionSingleton()
    await conn.get_connection()
    for row in await conn.get_banned_words_for_server('123'):
        print(row['value'])

if __name__ == '__main__':
    asyncio.run(main())
