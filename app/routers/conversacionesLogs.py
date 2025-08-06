# routers/logs.py
from fastapi import APIRouter, Depends
from app.models.mongo_schemas import ConversacionLogSchema
from app.service.logging_service import LoggingService
from app.repositories.mongo_repository import MongoRepository
from datetime import datetime

router = APIRouter()

# Mongo config temporal para esta ruta
mongo_url = "mongodb://localhost:27017"
mongo_repo = MongoRepository(mongo_url)
logging_service = LoggingService(mongo_repo)

@router.post("/test-log",tags=["conversacionesLog"])
async def test_guardar_log(log: ConversacionLogSchema):
    return {"id_insertado": await logging_service.registrar_conversacion(log)}

@router.get("/test-log/{id_paciente}",tags=["conversacionesLog"])
async def test_buscar_logs(id_paciente: int):
    return await logging_service.consultar_logs_por_paciente(id_paciente)