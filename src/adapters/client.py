from celery import Celery


class CeleryClient:

    @staticmethod
    def _build_celery_client_(name: str, broker_url: str, result_backend: str) -> Celery:
        app = Celery(name)
        app.conf.broker_url = broker_url
        app.conf.result_backend = result_backend
        return app

    def __init__(self, name: str, broker_url: str, result_backend: str):
        self.celery_app = self._build_celery_client_(name, broker_url, result_backend)
