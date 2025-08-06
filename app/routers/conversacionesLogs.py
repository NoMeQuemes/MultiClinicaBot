# routers/logs.py
from typing import List
from fastapi import APIRouter, Depends
from app.models.mongo_schemas import ConversacionLogSchema
from app.models.mongo_schemas import IaFeedbackSchema
from app.models.mongo_schemas import IntencionEntrenamientoSchema
from app.service.logging_service import LoggingService
from app.service.logging_service import IaFeedback
from app.repositories.mongo_repository import MongoRepository
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter()

# Mongo config temporal para esta ruta
mongo_url = "mongodb://localhost:27017"
mongo_repo = MongoRepository(mongo_url)
logging_service = LoggingService(mongo_repo)
Ia_Feedback = IaFeedback(mongo_repo)


# ---------------------------- Conversaciones Logs
@router.post("/test-log",tags=["conversacionesLog"])
async def test_guardar_log(log: ConversacionLogSchema):
    return {"id_insertado": await logging_service.registrar_conversacion(log)}

@router.get("/test-log/{id_paciente}",tags=["conversacionesLog"], response_model=List[ConversacionLogSchema])
async def test_buscar_logs(id_paciente: int):
    return await logging_service.consultar_logs_por_paciente(id_paciente)


# ---------------------------- Feedback
@router.post("/iaFeedback",tags=["Feedback IA"])
async def guardar_feedback(log: IaFeedbackSchema):
    return {"id_insertado": await Ia_Feedback.registrar_feedback(log)}

@router.get("/iaFeedback/{id_paciente}",tags=["Feedback IA"], response_model=List[IaFeedbackSchema])
async def buscar_feedback(id_paciente: int):
    return await Ia_Feedback.consultar_logs_feedback_por_paciente(id_paciente)