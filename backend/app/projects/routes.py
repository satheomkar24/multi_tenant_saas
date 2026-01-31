from fastapi import APIRouter, Depends, status
from app.projects.service import (
    create_project,
    delete_project_by_id,
    find_projects,
    update_project,
)
from app.tenancy.dependencies import resolve_tenant
from app.tenancy.tenant import Tenant
from app.utils.object_id import to_object_id

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("")
async def get_all(current: Tenant = Depends(resolve_tenant)):
    projects = await find_projects({"tenant_id": current.id})
    return projects


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(payload: dict, current: Tenant = Depends(resolve_tenant)):
    await create_project(payload, current.id)
    return {"message": "Project created successfully."}


@router.put("/{project_id}")
async def update(
    project_id: str, payload: dict, current: Tenant = Depends(resolve_tenant)
):
    project_oid = to_object_id(project_id)
    await update_project(payload, project_oid, current.id)
    return {"message": "Project updated successfully."}


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, current=Depends(resolve_tenant)):
    project_oid = to_object_id(project_id, "project_id")
    await delete_project_by_id(
        project_id=project_oid,
        tenant_id=current.id,
    )
