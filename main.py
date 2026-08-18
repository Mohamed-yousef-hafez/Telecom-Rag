from fastapi import FastAPI
from src.config.config_parser import settings
from src.logging.logger import logger
from src.core.factories import ModelFactory
 
async def lifespan(app: FastAPI):
    logger.info(f" {settings.app_name} v{settings.app_version} ")
    logger.info("starting app")
    ModelFactory.get_embeddings()
    ModelFactory.get_llm()
    
    logger.info("Application start successfully")
    yield  
    
    logger.info("shutting down")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade Telecom Customer Support RAG Microservice built with FastAPI, LangChain, FAISS, and Gemini.",
    lifespan=lifespan
)



@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)