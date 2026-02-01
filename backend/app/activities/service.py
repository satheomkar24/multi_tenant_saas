from app.enums.activity import ActivityAction
from app.enums.user import Role
from app.providers.repository import get_activity_repo
from app.users.user import User, get_current_user


async def get_activities(tenant_id):
    activity_repo = get_activity_repo()
    return await activity_repo.find_all(
        {"tenant_id": tenant_id}, sort=("created_at", -1)
    )


async def create_activity(
    *,
    action: ActivityAction,
    entity: str,
    entity_id: str,
    message: str,
    meta: dict | None = None,
    user: User | None = None
):
    activity_repo = get_activity_repo()

    if user is None:
        try:
            user = get_current_user()
        except Exception:
            user = None

    activity = {
        "action": action,
        "entity": entity,
        "entity_id": entity_id,
        "message": message,
        "meta": meta or {},
    }

    # user-dependent fields (only if user exists)
    if user is not None:
        activity.update(
            {
                "tenant_id": user.tenant_id,
                "actor_id": user.id,
                "actor_role": user.role,
            }
        )
    else:
        # system / signup / anonymous activity
        activity.update(
            {
                "tenant_id": None,
                "actor_id": None,
                "actor_role": Role.SYSTEM,
            }
        )

    await activity_repo.insert_one(activity)
