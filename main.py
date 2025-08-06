from fastapi import FastAPI

app = FastAPI(
    title="Chatbot AI",
    description="Un bot conversacional multi-institucional con FastAPI y LangGraph.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Endpoint para verificar que la aplicación está funcionando."""
    return {"status": "ok"}