import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.api.router import api_router
from app.core.config import get_settings
from app.services.supabase import get_supabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Init
        get_settings()
        get_supabase()

        # Running
        yield

    finally:
        # Shutdown
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
