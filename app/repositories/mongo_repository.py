from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
import os

class MongoRepository:
    def __init__(self, mongo_url: str, db_name: str = "bot_multi_clinica"):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]

    async def initialize_collections(self):
        # Conversaciones
        await self.db.conversaciones_logs.create_index(
            [("id_clinica", ASCENDING), ("fecha_hora", ASCENDING), ("canal", ASCENDING)]
        )
        await self.db.conversaciones_logs.create_index("sesion_id")
        await self.db.conversaciones_logs.create_index("id_paciente")

        # TTL index para borrar documentos después de 1 año (365 días)
        await self.db.conversaciones_logs.create_index(
            "fecha_hora", expireAfterSeconds=60 * 60 * 24 * 365
        )

    def get_collection(self, name: str):
        return self.db[name]