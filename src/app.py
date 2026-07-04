from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from src.modules.auth.routes.auth_routes import router as auth_router
from src.common.config.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="FastAPI Backend",
    lifespan=lifespan
)

router = APIRouter()

# Routes
@router.get("/")
async def root():
    return {
        "success": True,
        "message": "Welcome to FastAPI Backend"
    }

@router.get("/health")
async def health_check():
    return {
        "success": True,
        "message": "Health check done, Server is running successfully"
    }

app.include_router(router)
app.include_router(auth_router)