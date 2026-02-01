from bson import ObjectId
from fastapi import HTTPException, status

from app.activities.service import create_activity
from app.enums.activity import ActivityAction
from app.providers.repository import get_project_repo


async def find_projects(data: dict):
    projectRepository = get_project_repo()
    projects = await projectRepository.find_all(data)
    return projects


async def create_project(data: dict, tenant_id):
    projectRepository = get_project_repo()
    project = {
        "tenant_id": tenant_id,
        "name": data["name"],
        "description": data.get("description", ""),
    }
    project_result = await projectRepository.insert_one(project)

    await create_activity(
        action=ActivityAction.PROJECT_CREATED,
        entity="project",
        entity_id=project_result.inserted_id,
        message=f"Project '{project['name']}' created",
    )


async def update_project(data: dict, project_id: ObjectId, tenant_id):
    projectRepository = get_project_repo()
    fields = {
        "name": data["name"],
        "description": data.get("description", ""),
    }
    await projectRepository.update_one(
        id=project_id,
        tenant_id=tenant_id,
        data=fields,
    )


async def delete_project_by_id(project_id: ObjectId, tenant_id):
    project_repo = get_project_repo()
    result = await project_repo.delete_one(
        {
            "_id": project_id,
            "tenant_id": tenant_id,
        }
    )
    if not result.deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
