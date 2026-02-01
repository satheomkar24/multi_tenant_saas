from bson import ObjectId
from fastapi import HTTPException, status

from app.activities.service import create_activity
from app.enums.activity import ActivityAction
from app.enums.task import Priority, TaskStatus
from app.providers.repository import get_task_repo


async def find_tasks(data: dict):
    taskRepository = get_task_repo()
    tasks = await taskRepository.find_all(data)
    return tasks


async def create_task(data: dict, tenant_id):
    taskRepository = get_task_repo()
    task = {
        "tenant_id": tenant_id,
        "project_id": data["project_id"],
        "title": data["title"],
        "description": data.get("description", ""),
        "status": TaskStatus.TODO,
        "priority": data.get("priority", Priority.MEDIUM),
        "assigned_to": data.get("assigned_to"),
    }
    task_result = await taskRepository.insert_one(task)

    await create_activity(
        action=ActivityAction.TASK_CREATED,
        entity="task",
        entity_id=task_result.inserted_id,
        message=f"Task '{task['title']}' created",
    )


async def update_task(data: dict, task_id: ObjectId, tenant_id):
    taskRepository = get_task_repo()
    # Keep only keys that have a non-None value
    fields = {k: v for k, v in data.items() if v is not None}

    old_task = await taskRepository.find_one({"_id": task_id, "tenant_id": tenant_id})
    await taskRepository.update_one(id=task_id, tenant_id=tenant_id, data=fields)
    await assign_task_activity(old_task, fields, task_id)


async def delete_task_by_id(task_id: ObjectId, tenant_id):
    task_repo = get_task_repo()
    result = await task_repo.delete_one(
        {
            "_id": task_id,
            "tenant_id": tenant_id,
        }
    )
    if not result.deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


field_action_map = {
    "assigned_to": lambda old, new: ActivityAction.TASK_ASSIGNED,
    "status": lambda old, new: (
        ActivityAction.TASK_COMPLETED
        if new == "completed"
        else ActivityAction.TASK_STATUS_CHANGED
    ),
    "priority": lambda old, new: ActivityAction.TASK_PRIORITY_CHANGED,
    "due_date": lambda old, new: ActivityAction.TASK_DUE_DATE_CHANGED,
}


async def assign_task_activity(
    old_task: dict | None, new_task: dict | None, task_id: ObjectId
):
    if old_task is None or new_task is None:
        return

    for key, new_value in new_task.items():
        old_value = old_task.get(key)
        if old_value != new_value:
            action_func = field_action_map.get(
                key, lambda old, new: ActivityAction.TASK_UPDATED
            )
            action = action_func(old_value, new_value)

            await create_activity(
                action=action,
                entity="task",
                entity_id=str(task_id),
                message=f"{key} changed from '{old_value}' to '{new_value}'",
            )
