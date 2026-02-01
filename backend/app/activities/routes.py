from fastapi import APIRouter, Depends

from app.activities.service import get_activities
from app.tenancy.dependencies import resolve_tenant
from app.tenancy.tenant import Tenant


router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("")
async def get_all(current:Tenant=Depends(resolve_tenant)):
    activities = await get_activities(current.id)

