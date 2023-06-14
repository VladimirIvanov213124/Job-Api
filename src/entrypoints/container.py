from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration
from dependency_injector.providers import Factory
from dependency_injector.providers import Singleton

from src.adapters.client import CeleryClient
from src.adapters.tasks import TaskService
from src.entrypoints.secrets import AppSecret
from src.usecases.common import TaskUseCase


class AppContainer(DeclarativeContainer):
    config = Configuration(pydantic_settings=[AppSecret()])
    celery_client = Singleton(CeleryClient, name=config.celery_name,
                              broker_url=config.broker_url, result_backend=config.result_backend)
    task_service = Factory(TaskService, celery_app=celery_client.provided.celery_app)
    use_case = Factory(TaskUseCase, task_service=task_service)
