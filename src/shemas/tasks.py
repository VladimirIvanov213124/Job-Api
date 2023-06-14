from dataclasses import dataclass, field


@dataclass
class TaskSchema:
    user_job_description: str = 'success money data analyse'
    links: list[str] = field(default_factory=lambda: ['https://aurora.tech/careers'])
