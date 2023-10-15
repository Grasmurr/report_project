from repository.db_manager import DBManager


class Event:
    def __init__(self, name=None, nm_prime=None, nm_usual=None):
        self.name = name
        self.nm_prime = nm_prime
        self.nm_usual = nm_usual
        self.db = DBManager()

    async def save(self):
        await self.db.insert_event(self.name, self.nm_prime, self.nm_usual)

    async def load(self, name):
        data = await self.db.get_event(name)
        if data:
            self.name, self.nm_prime, self.nm_usual = data
            return self
        return None


class Ticket(Event):
    def __init__(self, name, nm_prime, nm_usual, ticket_number=None, ticket_holder_name=None,
                 ticket_holder_surname=None, ticket_type=None):
        super().__init__(name, nm_prime, nm_usual)
        self.ticket_number = ticket_number
        self.ticket_holder_name = ticket_holder_name
        self.ticket_holder_surname = ticket_holder_surname
        self.ticket_type = ticket_type
        self.db = DBManager()

    async def save(self):
        await super().save()
        await self.db.insert_ticket(self.name, self.ticket_number, self.ticket_holder_name, self.ticket_holder_surname,
                                    self.ticket_type)

    async def load(self, ticket_number):
        data = await self.db.get_ticket(ticket_number)
        if data:
            _, self.ticket_holder_name, self.ticket_holder_surname, self.ticket_type, self.name = data
            event_data = await super().load(self.name)
            if event_data:
                _, self.nm_prime, self.nm_usual = event_data
                return self
        return None
