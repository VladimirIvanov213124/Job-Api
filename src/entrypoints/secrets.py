from pydantic import BaseSettings


class AppSecret(BaseSettings):
    celery_name: str
    broker_url: str
    result_backend: str

    class Config:
        env_file: str = '.env'
