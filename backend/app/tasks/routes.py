from fastapi import APIRouter, Depends, Query, status
from datetime import datetime
from bson import ObjectId

from app.tasks.service import create_task, delete_task_by_id, find_tasks, update_task
from app.tenancy.dependencies import resolve_tenant
from app.tenancy.tenant import Tenant
from app.utils.object_id import to_object_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def get_all(project_id: str = Query(...), current: Tenant = Depends(resolve_tenant)):
    project_oid = to_object_id(project_id)
    tasks = await find_tasks({"tenant_id": current.id, "project_id": project_oid})
    return tasks



@router.post("", status_code=status.HTTP_201_CREATED)
async def create(payload: dict, current: Tenant = Depends(resolve_tenant)):
    await create_task(payload, current.id)
    return {"message": "Task created successfully."}


@router.put("/{task_id}")
async def update(task_id: str, payload: dict, current: Tenant = Depends(resolve_tenant)):
    task_oid = to_object_id(task_id)
    await update_task(payload, task_oid, current.id)
    return {"message": "Task updated successfully."}



@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: str, current: Tenant = Depends(resolve_tenant)):
    task_oid = to_object_id(task_id, "task_id")
    await delete_task_by_id(
        task_id=task_oid,
        tenant_id=current.id,
    )
