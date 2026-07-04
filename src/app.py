from fastapi import FastAPI, APIRouter

app = FastAPI(
    title="FastAPI Backend"
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