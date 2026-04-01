import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from asia.api.middleware.error_handler import register_error_handlers
from asia.api.routes import cases, explain_paper, metadata, query

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Wire all services on startup, cleanup on shutdown."""
    logger.info("Initializing ASIA services...")

    # --- RAG pipeline (query + embedding + LLM) ---
    from asia.api.dependencies import create_rag_pipeline

    rag_pipeline = create_rag_pipeline()
    application.state.rag_pipeline = rag_pipeline

    # --- Case service (in-memory for MVP) ---
    from asia.adapters.in_memory_case_repository import InMemoryCaseRepository
    from asia.services.case_service import CaseService

    case_repo = InMemoryCaseRepository()
    application.state.case_service = CaseService(
        case_repository=case_repo,
        rag_pipeline=rag_pipeline,
    )

    # --- Paper explainer ---
    from asia.services.paper_explainer import PaperExplainer

    application.state.paper_explainer = PaperExplainer(
        paper_repository=rag_pipeline._repo,
        llm_provider=rag_pipeline._llm,
    )

    logger.info("ASIA services ready.")
    yield
    logger.info("ASIA shutting down.")


app = FastAPI(
    title="ASIA",
    description="AI-powered Scientific Information Assistant for veterinary oncology",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(cases.router)
app.include_router(query.router)
app.include_router(metadata.router)
app.include_router(explain_paper.router)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "healthy"}
