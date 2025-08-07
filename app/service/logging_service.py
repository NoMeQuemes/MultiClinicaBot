from app.models.mongo_schemas import ConversacionLogSchema
from app.models.mongo_schemas import IaFeedbackSchema
from app.models.mongo_schemas import IntencionEntrenamientoSchema
from app.repositories.mongo_repository import MongoRepository
from datetime import datetime

class LoggingService:
    def __init__(self, mongo_repo: MongoRepository):
        self.collection = mongo_repo.get_collection("conversaciones_logs")

    async def registrar_conversacion(self, log: ConversacionLogSchema):
        log_dict = log.dict()
        result = await self.collection.insert_one(log_dict)
        return str(result.inserted_id)

    async def consultar_logs_por_paciente(self, id_paciente: int):
        cursor = self.collection.find({"id_paciente": id_paciente})
        return [doc async for doc in cursor]
    

class IaFeedback:
    def __init__(self, mongo_repo: MongoRepository):
        self.collection = mongo_repo.get_collection("ia_feedback")

    async def registrar_feedback(self, log: IaFeedbackSchema):
        log_dict = log.dict()
        result = await self.collection.insert_one(log_dict)
        return str(result.inserted_id)

    async def consultar_logs_feedback_por_paciente(self, id_paciente: int):
        cursor = self.collection.find({"id_paciente": id_paciente})
        return [doc async for doc in cursor]

class IntencionEntrenamiento:
    def __init__(self, mongo_repo: MongoRepository):
        self.collection = mongo_repo.get_collection("intenciones_entrenamiento")

    async def registrar_intencion(self, log: IntencionEntrenamientoSchema):
        log_dict = log.dict()
        result = await self.collection.insert_one(log_dict)
        return str(result.inserted_id)

    # async def consultar_intenciones_por_paciente(self, id_paciente: int):
    #     cursor = self.collection.find({"id_paciente": id_paciente})
    #     return [doc async for doc in cursor]