from fastapi import APIRouter
from sqlalchemy.sql import roles

from app.api import auth, grades, organizations, payments, students,classes,curriculum,onboarding,user,role,user_role,role_permission,academic_year
api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(students.router)
api_router.include_router(grades.router)
api_router.include_router(payments.router)
api_router.include_router(onboarding.router)
api_router.include_router(user.router)
api_router.include_router(role.router)
api_router.include_router(user_role.router)
api_router.include_router(role_permission.router)
api_router.include_router(academic_year.router)