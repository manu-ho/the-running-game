import logging

from pydantic import ValidationError

from src.utils import setup_logging

setup_logging()

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.dependency_container import DependencyContainer
from src.endpoints import router

logger = logging.getLogger(__name__)


def validation_excetion_handler(request, exc):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc))


def create_app() -> FastAPI:
    logger.debug("creating app")
    container = DependencyContainer()

    for provider in container.traverse():
        logger.debug(provider)
    container.check_dependencies()

    # TODO switch to alembic for migration
    database = container.database()
    database.create_database()

    logger.debug("created DI container")

    origins = [
        "http://localhost",
        "http://localhost:8083",  # local backend
        "http://localhost:8080",  # local frontend
        "http://localhost:3000",  # local dev vite frontend
    ]

    app = FastAPI()
    app.container = container
    app.add_exception_handler(ValidationError, validation_excetion_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    logger.debug("created app")
    return app


app = create_app()
