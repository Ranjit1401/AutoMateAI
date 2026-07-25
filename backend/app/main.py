from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router
from app.api.voice import router as voice_router
from app.api.calls import router as calls_router
from app.api.google_routes import router as google_router


app = FastAPI()

# Allows a frontend running on a different origin (e.g. localhost:3000,
# a deployed dashboard, etc.) to call these endpoints directly.
# Tighten allow_origins to your actual frontend URL(s) in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(voice_router, tags=["Vapi Voice"])
app.include_router(calls_router, tags=["Twilio"])
app.include_router(google_router, tags=["Google"])
