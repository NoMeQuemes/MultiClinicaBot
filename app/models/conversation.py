from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IncomingMessage(BaseModel):
    """
    Mensaje recibido desde el webhook (ej. Chattigo / WhatsApp)
    """
    phone: str = Field(..., description="Número de teléfono del paciente")
    text: str = Field(..., description="Texto del mensaje recibido")
    did: str = Field(..., description="DID de la clínica")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class OutgoingMessage(BaseModel):
    """
    Mensaje que el bot enviará como respuesta
    """
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationEntry(BaseModel):
    """
    Un mensaje en el historial de conversación
    """
    sender: str = Field(..., description="Quién envió el mensaje (user/bot)")
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistory(BaseModel):
    """
    Historial completo de un paciente
    """
    paciente_id: str
    messages: List[ConversationEntry]
