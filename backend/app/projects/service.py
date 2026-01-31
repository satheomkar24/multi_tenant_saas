from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.providers.repository import get_project_repo


async def find_projects(data: dict):
    projectRepository = get_project_repo()
    projects = await projectRepository.find(data)
    return projects


async def create_project(data: dict, tenant_id):
    projectRepository = get_project_repo()
    project = {
        "tenant_id": tenant_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    await projectRepository.insert_one(project)


async def update_project(data: dict, project_id: ObjectId, tenant_id):
    projectRepository = get_project_repo()
    fields = {
        "name": data["name"],
        "description": data.get("description", ""),
        "updated_at": datetime.now(),
    }
    await projectRepository.update_one(fields, project_id, tenant_id)


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
