from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import tasks, uploads

app = FastAPI(title="TaskMaster API", version="1.0.0")

origins = settings.allowed_origins or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(uploads.router)


@app.get("/")
def health():
    return {"status": "ok"}
