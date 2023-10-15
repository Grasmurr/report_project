from repository.db_manager import DBManager


class PromouterModel:
    def __init__(self, user_id=None, username=None, full_name=None):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.db = DBManager()

    async def save(self):
        await self.db.insert_promouter(self.user_id, self.username, self.full_name)

    async def load(self, user_id):
        data = await self.db.get_promouter(user_id)
        if data:
            self.user_id, self.username, self.full_name = data
            return self
        return None



