from fastapi import FastAPI
#from app.routers.router import router
from app.routers.conversacionesLogs import router
import asyncio
from app.repositories.mongo_repository import MongoRepository

app = FastAPI(
    title="Chatbot AI",
    description="Un bot conversacional multi-institucional con FastAPI y LangGraph.",
    version="0.1.0"
)

#app.include_router(router)


mongo_url = "mongodb://localhost:27017"  # reemplazar si tenés usuario/pass
mongo_repo = MongoRepository(mongo_url)

@app.on_event("startup")
async def startup_event():
    await mongo_repo.initialize_collections()
    
app.include_router(router,prefix="/api")