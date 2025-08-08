from fastapi import APIRouter, BackgroundTasks
from app.service import bot_service, conversation_service
from app.models.conversation import IncomingMessage, Feedback

router = APIRouter(prefix="/api/v1/bot", tags=["Bot"])

@router.post("/webhook")
async def webhook(msg: IncomingMessage, background_tasks: BackgroundTasks):
    # Procesar mensaje en segundo plano
    background_tasks.add_task(bot_service.handle_webhook, msg)
    return {"status": "received"}

@router.post("/proceso-mensaje")
async def procesar_mensaje(msg: IncomingMessage):
    return await bot_service.process_message(msg)

@router.get("/conversacion/{paciente_id}")
async def historial(paciente_id: str):
    return await conversation_service.get_history(paciente_id)

@router.post("/feedback")
async def feedback(data: Feedback):
    return await bot_service.save_feedback(data)
