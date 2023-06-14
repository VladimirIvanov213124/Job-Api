from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.entrypoints.container import AppContainer
from src.entrypoints.rest_api.api import router


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(router)
    return app


def create_app() -> FastAPI:
    container = AppContainer()
    container.wire(modules=[
        'src.entrypoints.rest_api.api',
    ])
    app = FastAPI(
        title='Parse Api',
        version='v1',
    )
    origins = [
        'http://127.0.0.1:3000',
        'http://localhost:3000',
        'http://backend:3000',
        'http://rest-api:3000',
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app = register_routers(app)
    return app


application = create_app()
