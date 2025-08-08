from app.utils import message_processor
from app.database import mongo
from app.services import conversation_service

async def handle_webhook(msg):
    # 1. Identificar clínica por DID
    clinic = await message_processor.identify_clinic(msg.did)

    # 2. Autenticar o registrar paciente
    paciente = await message_processor.get_or_create_patient(msg.phone)

    # 3. Procesar mensaje con IA
    intent = await message_processor.classify_intent(msg.text)

    # 4. Ejecutar flujo correspondiente
    response = await message_processor.execute_flow(intent, paciente, msg.text)

    # 5. Guardar en historial
    await conversation_service.save_message(paciente.id, msg.text, response)

    # 6. Retornar respuesta para enviar por WhatsApp
    return response

async def process_message(msg):
    return await handle_webhook(msg)

async def save_feedback(data):
    return await mongo.db["ia_feedback"].insert_one(data.dict())
