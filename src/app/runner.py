from fastapi import FastAPI
import uvicorn

from src.app.settings import Settings
from src.api.routes import api_router
from src.app.lifespan import initialize_lifespan


def create_app(settings) -> FastAPI:
    app = FastAPI(lifespan=initialize_lifespan(settings))
    app.include_router(api_router, prefix="/api/v1")

    return app


def run_app() -> None:
    app = create_app(Settings())  # type: ignore[call-arg]
    uvicorn.run(app, host="0.0.0.0", port=8000)


if "__main__" == __name__:
    run_app()
