from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ConversacionLogSchema(BaseModel):
    _id: Any
    fecha_hora: datetime
    id_paciente: Optional[int]
    id_clinica: int
    canal: str  # "whatsapp", "web", "voz"
    entrada: str
    respuesta: str
    intencion: Optional[str] = None
    confianza: float
    entidades: Dict[str, Any]
    feedback: bool = False
    sesion_id: str

class IaFeedbackSchema(BaseModel):
    fecha_hora: datetime
    id_paciente: Optional[int]
    id_clinica: int
    sesion_id: str
    entrada_usuario: str
    respuesta_bot: str
    intencion_detectada: str
    entidades_detectadas: Dict[str, str]
    calificacion_usuario: str  # correcta | incorrecta | incompleta
    comentario_usuario: Optional[str] = None
    procesado: bool = False


class IntencionEntrenamientoSchema(BaseModel):
    texto: str
    intencion: str
    entidades: Dict[str, str]
    etiquetado_por: str  # usuario que lo clasificó
    origen: str  # ejemplo: 'manual', 'feedback', 'histórico'
    fecha_registro: datetime
    usado_en_modelo: bool = False
