from fastapi import APIRouter
from sqlalchemy.sql import roles

from app.api import auth, grades, organizations, payments, students, classe, curriculum, onboarding, user, role, \
    user_role, role_permission, academic_year, level, guardian, student_guardian , enrollment,subject , curriculum_subject , teacher_assignment, evaluation , attendance,report_cards , fee_type,\
payments, dashboard, receipts

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
api_router.include_router(level.router)
api_router.include_router(classe.router)
api_router.include_router(guardian.router)
api_router.include_router(student_guardian.router)
api_router.include_router(enrollment.router)
api_router.include_router(subject.router)
api_router.include_router(curriculum.router)
api_router.include_router(curriculum_subject.router)
api_router.include_router(teacher_assignment.router)
api_router.include_router(evaluation.router)
api_router.include_router(attendance.router)
api_router.include_router(report_cards.router)
api_router.include_router(fee_type.router)
api_router.include_router(payments.router)
api_router.include_router(dashboard.router)
api_router.include_router(receipts.router)