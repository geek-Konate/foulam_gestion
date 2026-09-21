import uuid
from decimal import Decimal

from fastapi import Depends

from app.api.deps import get_academic_year_repository, get_user_repository, get_class_repository, \
    get_evaluation_repository, get_teacher_assignment_repository
from app.core.exceptions import NotFoundException
from app.repositories.academic import EvaluationRepository
from app.repositories.rbac import UserRepository

from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    StudentRepository,
)

from app.repositories.curriculum import (
    TeacherAssignmentRepository,
)

from app.repositories.finance import (
    FeeTypeRepository,
    PaymentRepository,
)


class DashboardService:

    def __init__(
        self,
        academic_year_repo: AcademicYearRepository,
        class_repo: ClassRepository,
        student_repo: StudentRepository,
        teacher_assignment_repo: TeacherAssignmentRepository,
        fee_type_repo: FeeTypeRepository,
        payment_repo: PaymentRepository,
    ):
        self.academic_year_repo = academic_year_repo
        self.class_repo = class_repo
        self.student_repo = student_repo
        self.teacher_assignment_repo = teacher_assignment_repo
        self.fee_type_repo = fee_type_repo
        self.payment_repo = payment_repo

    async def get_establishment_dashboard(
        self,
        establishment_id: uuid.UUID,
    ):
        academic_year = (
            await self.academic_year_repo.get_current(
                establishment_id
            )
        )

        if not academic_year:
            return {
                "establishment_id": establishment_id,
                "academic_year_id": None,
                "academic_year_name": None,
                "students_count": 0,
                "classes_count": 0,
                "teachers_count": 0,
                "total_due": Decimal("0"),
                "total_paid": Decimal("0"),
                "remaining": Decimal("0"),
            }

        classes = await self.class_repo.get_by_academic_year(
            academic_year.id
        )

        students = await self.student_repo.get_by_establishment(
            establishment_id
        )

        teacher_ids = set()

        for class_ in classes:
            assignments = (
                await self.teacher_assignment_repo.get_by_class(
                    class_.id
                )
            )

            for assignment in assignments:
                teacher_ids.add(assignment.user_id)

        total_due = await self.fee_type_repo.get_total_amount(
            establishment_id
        )

        total_paid = Decimal("0")

        for student in students:
            total_paid += (
                await self.payment_repo.get_total_paid_by_student(
                    student.id
                )
            )

        remaining = total_due - total_paid

        if remaining < 0:
            remaining = Decimal("0")

        return {
            "establishment_id": establishment_id,
            "academic_year_id": academic_year.id,
            "academic_year_name": academic_year.name,
            "students_count": len(students),
            "classes_count": len(classes),
            "teachers_count": len(teacher_ids),
            "total_due": total_due,
            "total_paid": total_paid,
            "remaining": remaining,
        }



class TeacherDashboardService:

    def __init__(
        self,
        teacher_assignment_repo: TeacherAssignmentRepository,
        evaluation_repo: EvaluationRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
        user_repo: UserRepository,
    ):
        self.teacher_assignment_repo = teacher_assignment_repo
        self.evaluation_repo = evaluation_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo
        self.user_repo = user_repo

    async def get_teacher_dashboard(
        self,
        establishment_id: uuid.UUID,
        teacher_id: uuid.UUID,
    ):
        user = await self.user_repo.get(teacher_id)

        if not user:
            raise NotFoundException(
                "Enseignant introuvable"
            )

        # Vérification que l'utilisateur appartient
        # bien à l'établissement.
        user_establishment = next(
            (
                item
                for item in user.user_establishments
                if item.establishment_id == establishment_id
            ),
            None,
        )

        if not user_establishment:
            raise NotFoundException(
                "Enseignant introuvable"
            )

        assignments = (
            await self.teacher_assignment_repo.get_by_teacher(
                teacher_id
            )
        )

        establishment_assignments = []

        for assignment in assignments:
            class_ = await self.class_repo.get(
                assignment.class_id
            )

            if not class_:
                continue

            academic_year = await self.academic_year_repo.get(
                class_.academic_year_id
            )

            if not academic_year:
                continue

            if academic_year.establishment_id != establishment_id:
                continue

            establishment_assignments.append(
                assignment
            )

        class_ids = {
            assignment.class_id
            for assignment in establishment_assignments
        }

        evaluations_count = 0

        for class_id in class_ids:
            evaluations = (
                await self.evaluation_repo.get_by_class(
                    class_id
                )
            )

            evaluations_count += len(evaluations)

        assignments_data = [
            {
                "assignment_id": assignment.id,
                "class_id": assignment.class_id,
                "curriculum_subject_id": (
                    assignment.curriculum_subject_id
                ),
            }
            for assignment in establishment_assignments
        ]

        return {
            "teacher_id": teacher_id,
            "establishment_id": establishment_id,
            "assignments_count": len(
                establishment_assignments
            ),
            "classes_count": len(class_ids),
            "evaluations_count": evaluations_count,
            "assignments": assignments_data,
        }

def get_teacher_dashboard_service(
    teacher_assignment_repo: TeacherAssignmentRepository = Depends(
        get_teacher_assignment_repository
    ),
    evaluation_repo: EvaluationRepository = Depends(
        get_evaluation_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
):
    return TeacherDashboardService(
        teacher_assignment_repo=teacher_assignment_repo,
        evaluation_repo=evaluation_repo,
        class_repo=class_repo,
        academic_year_repo=academic_year_repo,
        user_repo=user_repo,
    )