import uuid
from decimal import Decimal

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.academic import (
    EvaluationRepository,
    GradeRepository,
)
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    ClassRepository,
    AcademicYearRepository,
)
from app.repositories.curriculum import TeacherAssignmentRepository, CurriculumSubjectRepository
from app.repositories.rbac import UserRepository


class GradeService:

    def __init__(
            self,
            grade_repo: GradeRepository,
            evaluation_repo: EvaluationRepository,
            student_repo: StudentRepository,
            enrollment_repo: EnrollmentRepository,
            class_repo: ClassRepository,
            academic_year_repo: AcademicYearRepository,
            teacher_assignment_repo: TeacherAssignmentRepository,
            curriculum_subject_repo: CurriculumSubjectRepository,
            user_repo: UserRepository,
    ):
        self.grade_repo = grade_repo
        self.evaluation_repo = evaluation_repo
        self.student_repo = student_repo
        self.enrollment_repo = enrollment_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo
        self.teacher_assignment_repo = teacher_assignment_repo
        self.curriculum_subject_repo = curriculum_subject_repo
        self.user_repo = user_repo

    async def _get_evaluation(
        self,
        establishment_id: uuid.UUID,
        evaluation_id: uuid.UUID,
    ):
        evaluation = await self.evaluation_repo.get(
            evaluation_id
        )

        if not evaluation:
            raise NotFoundException(
                "Évaluation introuvable"
            )

        school_class = await self.class_repo.get(
            evaluation.class_id
        )

        if not school_class:
            raise NotFoundException(
                "Classe introuvable"
            )

        academic_year = await self.academic_year_repo.get(
            school_class.academic_year_id
        )

        if not academic_year:
            raise NotFoundException(
                "Année scolaire introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException(
                "Évaluation introuvable"
            )

        return evaluation

    async def _get_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException(
                "Élève introuvable"
            )

        if student.establishment_id != establishment_id:
            raise NotFoundException(
                "Élève introuvable"
            )

        return student

    async def _validate_student_in_class(
        self,
        student_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        enrollments = await self.enrollment_repo.get_by_student(
            student_id
        )

        for enrollment in enrollments:
            if (
                enrollment.class_id == class_id
                and enrollment.status == "active"
            ):
                return enrollment

        raise ConflictException(
            "Cet élève n'est pas inscrit dans cette classe"
        )

    async def _validate_teacher_assignment(
        self,
        teacher_id: uuid.UUID,
        class_id: uuid.UUID,
        subject_id: uuid.UUID,
    ):
        assignments = (
            await self.teacher_assignment_repo.get_by_class(
                class_id
            )
        )

        for assignment in assignments:
            if assignment.user_id != teacher_id:
                continue

            curriculum_subject = (
                await self._get_curriculum_subject(
                    assignment.curriculum_subject_id
                )
            )

            if curriculum_subject.subject_id == subject_id:
                return assignment

        raise ConflictException(
            "Cet enseignant n'est pas affecté à cette matière dans cette classe"
        )

    async def _get_curriculum_subject(
            self,
            curriculum_subject_id: uuid.UUID,
    ):
        from app.repositories.curriculum import (
            CurriculumSubjectRepository,
        )

        # Cette méthode sera remplacée par l'injection du repository
        # si nécessaire.
        raise NotImplementedError

    async def create_grade(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        evaluation = await self._get_evaluation(
            establishment_id,
            data.evaluation_id,
        )

        await self._get_student(
            establishment_id,
            data.student_id,
        )

        await self._validate_student_in_class(
            data.student_id,
            evaluation.class_id,
        )

        if data.value < Decimal("0"):
            raise ConflictException(
                "La note ne peut pas être négative"
            )

        if data.value > Decimal("20"):
            raise ConflictException(
                "La note ne peut pas être supérieure à 20"
            )

        existing = await self.grade_repo.get_by_evaluation(
            data.evaluation_id
        )

        for grade in existing:
            if grade.student_id == data.student_id:
                raise ConflictException(
                    "Cet élève possède déjà une note pour cette évaluation"
                )

        return await self.grade_repo.create(
            data.model_dump()
        )

    async def list_grades(
        self,
        establishment_id: uuid.UUID,
        evaluation_id: uuid.UUID,
    ):
        await self._get_evaluation(
            establishment_id,
            evaluation_id,
        )

        return await self.grade_repo.get_by_evaluation(
            evaluation_id
        )

    async def list_student_grades(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        return await self.grade_repo.get_by_student(
            student_id
        )

    async def get_grade(
        self,
        establishment_id: uuid.UUID,
        grade_id: uuid.UUID,
    ):
        grade = await self.grade_repo.get(grade_id)

        if not grade:
            raise NotFoundException(
                "Note introuvable"
            )

        await self._get_evaluation(
            establishment_id,
            grade.evaluation_id,
        )

        return grade

    async def update_grade(
        self,
        establishment_id: uuid.UUID,
        grade_id: uuid.UUID,
        data,
    ):
        grade = await self.get_grade(
            establishment_id,
            grade_id,
        )

        if data.value is not None:
            if data.value < Decimal("0"):
                raise ConflictException(
                    "La note ne peut pas être négative"
                )

            if data.value > Decimal("20"):
                raise ConflictException(
                    "La note ne peut pas être supérieure à 20"
                )

        payload = data.model_dump(
            exclude_unset=True
        )

        return await self.grade_repo.update(
            grade,
            payload,
        )

    async def delete_grade(
        self,
        establishment_id: uuid.UUID,
        grade_id: uuid.UUID,
    ):
        grade = await self.get_grade(
            establishment_id,
            grade_id,
        )

        return await self.grade_repo.soft_delete(
            grade
        )