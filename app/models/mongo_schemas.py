from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ConversacionLogSchema(BaseModel):
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
