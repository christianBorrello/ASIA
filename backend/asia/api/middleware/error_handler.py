"""Error handler middleware -- Italian user-facing messages, no technical leaks."""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": (
                    "Si e verificato un errore durante l'elaborazione "
                    "della richiesta. Riprova tra qualche istante."
                ),
                "suggestions": [
                    "Riprovare tra qualche istante",
                    "Riformulare la domanda in modo diverso",
                    "Contattare il supporto se il problema persiste",
                ],
            },
        )
