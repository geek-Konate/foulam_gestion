import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import ClassRepository, EnrollmentRepository, StudentRepository
from app.schemas.student import EnrollmentCreate
from app.services.rbac_service import RbacService


class EnrollmentService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        class_repo: ClassRepository,
        student_repo: StudentRepository,
        rbac_service: RbacService,
    ):
        self.enrollment_repo = enrollment_repo
        self.class_repo = class_repo
        self.student_repo = student_repo
        self.rbac_service = rbac_service

    async def enroll_student(self, data: EnrollmentCreate, current_user_id: uuid.UUID):
        student = await self.student_repo.get(data.student_id)
        if not student:
            raise NotFoundException("Élève introuvable")

        target_class = await self.class_repo.get(data.class_id)
        if not target_class:
            raise NotFoundException("Classe introuvable")

        # Le scope vient de la ressource chargée, pas de l'URL.
        # AcademicYear -> Establishment : il faut remonter la chaîne pour obtenir establishment_id.
        establishment_id = await self._get_establishment_id_for_class(target_class)

        await self.rbac_service.require_permission(
            current_user_id, "student.enroll", establishment_id=establishment_id
        )

        existing = await self.enrollment_repo.get_active_enrollment(data.student_id)
        if existing:
            raise ConflictException("Cet élève a déjà une inscription active")

        return await self.enrollment_repo.create(data.model_dump())

    async def _get_establishment_id_for_class(self, target_class) -> uuid.UUID:
        # target_class.academic_year doit être chargé (selectinload) en amont dans le repo,
        # sinon lazy-load async qui plante hors contexte de session ouverte.
        return target_class.academic_year.establishment_id