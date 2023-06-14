from abc import ABC
from abc import abstractmethod
from typing import List

from src.shemas.tasks import TaskSchema


class TaskServiceInterface(ABC):

    @abstractmethod
    def create_task(self, data: TaskSchema) -> int:
        raise NotImplementedError()

    @abstractmethod
    def build_excel_file(self, task_id: str, data: List[dict]) -> str:
        raise NotImplementedError()
