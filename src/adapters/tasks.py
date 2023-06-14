import csv
from typing import List

from celery import Celery

from src.interfeces.tasks import TaskServiceInterface
from src.shemas.tasks import TaskSchema


class TaskService(TaskServiceInterface):

    def __init__(self, celery_app: Celery):
        self._celery_app = celery_app

    def create_task(self, data: TaskSchema) -> int:
        data.links = [link.replace(' ', '') for link in data.links]
        print(data.links)
        task = self._celery_app.send_task('AlgorithmTask', (data.user_job_description, data.links,))
        return task.id

    def build_excel_file(self, task_id: str, data: List[dict]) -> str:
        path = f'media/{task_id}.csv'
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Score', 'Job Name', 'Job Url'])
            for row in data:
                writer.writerow([row[0], row[1], row[2]])
        return path
