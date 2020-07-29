import asyncpg
from asyncpg.exceptions import UniqueViolationError
import asyncio

class PSQLConnectionSingleton:
    def __init__(self):
        self.pool = None

    async def get_connection(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(database='okuyasu')

    async def get_banned_phrases_for_server(self, server_id):
        async with pool.acquire() as connection:
            return await connection.fetch(
                'SELECT value, match_type FROM banned_phrases'
                + ' WHERE discord_id = $1',
                server_id
            )

    async def ban_phrase(self, server_id, phrase, match_type='word'):
        try:
            async with pool.acquire() as connection:
                await self.connection.execute(
                    'INSERT INTO banned_phrases (discord_id, value, match_type)'
                    + ' VALUES ($1, $2, $3)',
                    server_id, phrase, match_type
                )
        except UniqueViolationError:
            pass

    async def unban_phrase(self, server_id, phrase):
        async with pool.acquire() as connection:
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
