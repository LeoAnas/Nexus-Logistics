from fastapi import FastAPI
from src.infrastracture.logging import logger, setup_logging
from src.config import settings
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Starting the Application
    setup_logging()
    logger.info("System Starting...")
    yield
    # Shutdown logic
    logger.info("System Shutting Down")

#openai_url is used for api versioning and swagger automatically calls this 
app = FastAPI(
    title=settings.PROJECT_NAME,lifespan=lifespan, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/health")
async def health_check():
    return {"status":"OK","Version":"0.1.0"}

    