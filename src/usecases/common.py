from celery.result import AsyncResult

from src.interfeces.tasks import TaskServiceInterface
from src.shemas.tasks import TaskSchema


class TaskUseCase:
    def __init__(self, task_service: TaskServiceInterface):
        self._task_service = task_service

    @staticmethod
    def get_task_status(task_id: str):
        status_task = AsyncResult(task_id).state
        return status_task

    @staticmethod
    def get_task_results(task_id):
        results = AsyncResult(task_id)
        data = results.get()
        return data

    def create_task(self, data: TaskSchema) -> int:
        task_id = self._task_service.create_task(data)
        return task_id

    def get_excel_file(self, task_id: str) -> str:
        # status = self.get_task_status(task_id)
        # if status != CeleryResultEnum.success:
        #     raise ValueError('status task is not success')
        # data = self.get_task_results(task_id)
        data = []
        filename = self._task_service.build_excel_file(task_id, data)
        return filename
