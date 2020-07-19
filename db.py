import asyncpg
import asyncio

class PSQLConnectionSingleton:
    def __init__(self):
        self.connection = None

    async def get_connection(self):
        if self.connection is None:
            self.connection = await asyncpg.connect(database='okuyasu')
            print(self.connection)

async def main():
    conn = PSQLConnectionSingleton()
    await conn.get_connection()

asyncio.run(main())
