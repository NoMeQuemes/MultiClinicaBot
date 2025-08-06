from fastapi import FastAPI
from app.routers.router import router

app = FastAPI(
    title="Chatbot AI",
    description="Un bot conversacional multi-institucional con FastAPI y LangGraph.",
    version="0.1.0"
)

app.include_router(router)