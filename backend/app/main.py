import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.calls import router as calls_router
from app.api.chat import router as chat_router
from app.api.files import router as files_router
from app.api.google_routes import router as google_router
from app.api.logs import router as logs_router
from app.api.memory import router as memory_router
from app.api.settings import router as settings_router
from app.api.tasks import router as tasks_router
from app.api.voice import router as voice_router
from app.core.config import settings
from app.core.logging_config import configure_logging, get_logger
from app.db import init_db
import app.tools  # noqa: F401  — importing registers every tool with tool_registry

configure_logging()
logger = get_logger(__name__)


def _tool_names() -> list[str]:
    from app.tools.registry import tool_registry
    return tool_registry.list_tools()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    logger.info("%s started. Registered tools: %s", settings.APP_NAME, ", ".join(sorted(_tool_names())))
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI travel assistant with Gmail/Calendar/Drive/Sheets, Twilio, and Vapi integrations.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS is restricted to the configured frontend origin(s) — the previous
# `allow_origins=["*"]` combined with `allow_credentials=True` is invalid
# per the CORS spec for credentialed requests and was a real gap now that
# auth uses cookies.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s -> %s (%.1fms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(tasks_router)
app.include_router(memory_router)
app.include_router(logs_router)
app.include_router(settings_router)
app.include_router(files_router)
app.include_router(voice_router)
app.include_router(calls_router)
app.include_router(google_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
