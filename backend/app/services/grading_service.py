import uuid

from app.core.exceptions import NotFoundException
from app.repositories.academic import EvaluationRepository, GradeRepository
from app.repositories.student import StudentRepository
from app.schemas.academic import EvaluationCreate, GradeCreate, GradeUpdate
from app.services.rbac_service import RbacService


class GradingService:
    def __init__(
        self,
        evaluation_repo: EvaluationRepository,
        grade_repo: GradeRepository,
        student_repo: StudentRepository,
        rbac_service: RbacService,
    ):
        self.evaluation_repo = evaluation_repo
        self.grade_repo = grade_repo
        self.student_repo = student_repo
        self.rbac_service = rbac_service

    async def create_evaluation(self, data: EvaluationCreate, current_user_id: uuid.UUID):
        # Pas de FK class_id chargée ici : on a besoin du scope AVANT création,
        # donc on résout l'establishment via class_id directement.
        from app.repositories.student import ClassRepository
        class_repo = ClassRepository(self.evaluation_repo.session)
        target_class = await class_repo.get(data.class_id)
        if not target_class:
            raise NotFoundException("Classe introuvable")

        establishment_id = target_class.academic_year.establishment_id
        await self.rbac_service.require_permission(
            current_user_id, "evaluation.create", establishment_id=establishment_id
        )

        return await self.evaluation_repo.create(data.model_dump())

    async def submit_grade(self, data: GradeCreate, current_user_id: uuid.UUID):
        evaluation = await self.evaluation_repo.get(data.evaluation_id)
        if not evaluation:
            raise NotFoundException("Évaluation introuvable")

        student = await self.student_repo.get(data.student_id)
        if not student:
            raise NotFoundException("Élève introuvable")

        establishment_id = evaluation.class_.academic_year.establishment_id
        await self.rbac_service.require_permission(
            current_user_id, "grade.create", establishment_id=establishment_id
        )

        return await self.grade_repo.create(data.model_dump())

    async def update_grade(self, grade_id: uuid.UUID, data: GradeUpdate, current_user_id: uuid.UUID):
        grade = await self.grade_repo.get(grade_id)
        if not grade:
            raise NotFoundException("Note introuvable")

        evaluation = await self.evaluation_repo.get(grade.evaluation_id)
        establishment_id = evaluation.class_.academic_year.establishment_id
        await self.rbac_service.require_permission(
            current_user_id, "grade.update", establishment_id=establishment_id
        )

        return await self.grade_repo.update(grade, data.model_dump(exclude_unset=True))