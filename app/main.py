from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import advertisements
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    yield
    logger.info("Application shutting down")

app = FastAPI(
    title="Advertisement Service API",
    description="Сервис для размещения объявлений купли/продажи",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(advertisements.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Advertisement Service API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "python_version": "3.13"}