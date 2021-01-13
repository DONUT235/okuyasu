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
        async with self.pool.acquire() as connection:
            return await connection.fetch(
                'SELECT value, match_type FROM banned_phrases'
                + ' WHERE discord_id = $1',
                str(server_id)
            )

    async def ban_phrase(self, server_id, phrase, match_type='word'):
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    'INSERT INTO banned_phrases (discord_id, value, match_type)'
                    + ' VALUES ($1, $2, $3)',
                    server_id, phrase, match_type
                )
        except UniqueViolationError:
            pass

    async def unban_phrase(self, server_id, phrase):
        async with self.pool.acquire() as connection:
            await connection.execute(
                'DELETE FROM banned_phrases'
                + ' WHERE discord_id = $1 AND value = $2',
                server_id, phrase
            )

    async def can_kill(self, server_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(
                'SELECT can_kill'
                + ' FROM Permissions'
                + ' WHERE discord_id = $1',
                server_id
            )
            if len(result) == 0:
                await connection.execute(
                    'INSERT INTO Permissions (discord_id, can_kill)'
                    + ' VALUES ($1, FALSE)',
                    server_id
                )
                return False
            return result[0]['can_kill']

    async def disable_kill(self, server_id):
        async with self.pool.acquire() as connection:
            await connection.execute(
                'UPDATE TABLE Permissions'
                + ' SET can_kill=FALSE'
                + ' WHERE discord_id = $1',
                server_id
            )

db = PSQLConnectionSingleton()

async def main():
    conn = PSQLConnectionSingleton()
    await conn.get_connection()
    for row in await conn.get_banned_words_for_server(123):
        print(row['value'])

if __name__ == '__main__':
    asyncio.run(main())
