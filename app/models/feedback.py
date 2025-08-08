from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Feedback(BaseModel):
    """
    Feedback del usuario sobre la respuesta de la IA
    """
    paciente_id: str
    conversation_id: Optional[str] = Field(None, description="ID de la conversación")
    rating: int = Field(..., ge=1, le=5, description="Valoración de 1 a 5")
    comment: Optional[str] = Field(None, description="Comentario opcional")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
