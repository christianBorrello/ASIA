from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from asia.api.middleware.error_handler import register_error_handlers
from asia.api.routes import metadata, query

app = FastAPI(
    title="ASIA",
    description="AI-powered Scientific Information Assistant for veterinary oncology",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(query.router)
app.include_router(metadata.router)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "healthy"}
