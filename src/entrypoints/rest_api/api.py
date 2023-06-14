import asyncio

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from src.core.enums import CeleryResultEnum
from src.entrypoints.container import AppContainer
from src.shemas.tasks import TaskSchema
from src.usecases.common import TaskUseCase

STREAM_DELAY = 2
router = APIRouter(prefix='/api')


@router.post('/create_task', summary='Create task request')
@inject
async def create_task(task_data: TaskSchema, use_case: TaskUseCase = Depends(Provide[AppContainer.use_case])):
    try:
        task_data.links = [link.replace(' ', '') for link in task_data.links]
        task_id = use_case.create_task(task_data)
        return JSONResponse(
            status_code=200,
            content={'task_id': task_id}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'error_code': str(e)}
        )


@router.get('/get_status_task/{task_id}')
@inject
async def get_status_task(task_id: str, use_case: TaskUseCase = Depends(Provide[AppContainer.use_case])):
    try:
        status = use_case.get_task_status(task_id)
        return {'status': status}
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'error_code': str(e)}
        )


@router.get('/stream/{task_id}')
@inject
async def stream_task(task_id: str, request: Request, use_case: TaskUseCase = Depends(Provide[AppContainer.use_case])):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            status = use_case.get_task_status(task_id)
            if status == CeleryResultEnum.failure or status == CeleryResultEnum.success:
                yield status
                break

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


@router.get('/get_parse_data/{task_id}')
@inject
async def get_excel_file(task_id: str, use_case: TaskUseCase = Depends(Provide[AppContainer.use_case])):
    try:
        path = use_case.get_excel_file(task_id)
        headers = {'Content-Disposition': f'attachment; filename="{task_id}.csv"'}
        return FileResponse(path, headers=headers)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'error_code': str(e)}
        )
