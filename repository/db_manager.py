import asyncpg


class DBManager:
    def __init__(self):
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(
            user='admin',
            password='prod',
            database='postgres',
            host='repository'
        )

    async def close(self):
        await self.conn.close()

    async def insert_promouter(self, user_id, username, full_name):
        await self.conn.execute(
            'INSERT INTO promotors (user_id, username, full_name) VALUES ($1, $2, $3)',
            user_id, username, full_name
        )

    async def get_promouter(self, user_id):
        return await self.conn.fetchrow('SELECT * FROM promotors WHERE user_id = $1', user_id)

    async def insert_event(self, name, nm_prime, nm_usual):
        await self.conn.execute(
            'INSERT INTO events (name, nm_prime, nm_usual) VALUES ($1, $2, $3)',
            name, nm_prime, nm_usual
        )

    async def get_event(self, name):
        return await self.conn.fetchrow('SELECT * FROM events WHERE name = $1', name)

    async def insert_ticket(self, event_name, ticket_number, name, surname, ticket_type):
        await self.conn.execute(
            'INSERT INTO tickets (event_name, ticket_number, name, surname, ticket_type) VALUES ($1, $2, $3, $4, $5)',
            event_name, ticket_number, name, surname, ticket_type
        )

    async def get_ticket(self, ticket_number):
        return await self.conn.fetchrow('SELECT * FROM tickets WHERE ticket_number = $1', ticket_number)


