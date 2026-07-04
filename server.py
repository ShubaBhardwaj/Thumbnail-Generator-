import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src.app import app


def start():
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )


if __name__ == "__main__":
    start()