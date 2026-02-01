from app.activities.repository import ActivityRepository
from app.core.database import get_database
from app.projects.repository import ProjectRepository
from app.tasks.repository import TaskRepository
from app.tenancy.repository import TenantRepository
from app.users.repository import UserRepository


def get_tenant_repo() -> TenantRepository:
    return TenantRepository(get_database())


def get_user_repo() -> UserRepository:
    return UserRepository(get_database())


def get_project_repo() -> ProjectRepository:
    return ProjectRepository(get_database())


def get_task_repo() -> TaskRepository:
    return TaskRepository(get_database())

def get_activity_repo() -> ActivityRepository:
    return ActivityRepository(get_database())
