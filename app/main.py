from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.database import engine, Base
from app.routers import advertisements, auth, users
from app.config import settings

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
    title=settings.PROJECT_NAME,
    description="Сервис для размещения объявлений купли/продажи с аутентификацией",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(advertisements.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Advertisement Service API",
        "docs": "/docs",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }