import uvicorn

from src.app import app
from src.common.config.settings import settings


def start():
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT
    )


if __name__ == "__main__":
    start()