import uuid

from sqlalchemy import select

from app.core.exceptions import ConflictException, NotFoundException
from app.models.rbac import UserEstablishment
from app.repositories.curriculum import (
    TeacherAssignmentRepository,
    ClassCurriculumRepository,
    CurriculumSubjectRepository,
)
from app.repositories.rbac import UserRepository
from app.repositories.student import (
    ClassRepository,
    AcademicYearRepository,
)


class TeacherAssignmentService:

    def __init__(
        self,
        teacher_assignment_repo: TeacherAssignmentRepository,
        class_curriculum_repo: ClassCurriculumRepository,
        curriculum_subject_repo: CurriculumSubjectRepository,
        class_repo: ClassRepository,
        user_repo: UserRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.teacher_assignment_repo = teacher_assignment_repo
        self.class_curriculum_repo = class_curriculum_repo
        self.curriculum_subject_repo = curriculum_subject_repo
        self.class_repo = class_repo
        self.user_repo = user_repo
        self.academic_year_repo = academic_year_repo

    async def _get_class(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        school_class = await self.class_repo.get(class_id)

        if not school_class:
            raise NotFoundException("Classe introuvable")

        academic_year = await self.academic_year_repo.get(
            school_class.academic_year_id
        )

        if not academic_year:
            raise NotFoundException("Année scolaire introuvable")

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def _get_teacher(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        user = await self.user_repo.get(user_id)

        if not user:
            raise NotFoundException("Utilisateur introuvable")

        stmt = select(UserEstablishment).where(
            UserEstablishment.user_id == user_id,
            UserEstablishment.establishment_id == establishment_id,
            UserEstablishment.deleted_at.is_(None),
        )
        result = await self.user_repo.session.execute(stmt)
        user_establishment = result.scalar_one_or_none()

        if not user_establishment:
            raise NotFoundException(
                "Utilisateur introuvable dans cet établissement"
            )

        return user

    async def assign_teacher(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
        curriculum_subject_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        # Vérifier la classe
        await self._get_class(
            establishment_id,
            class_id,
        )

        # Vérifier que l'utilisateur appartient à l'établissement
        await self._get_teacher(
            establishment_id,
            user_id,
        )

        # Vérifier que le CurriculumSubject existe
        curriculum_subject = await self.curriculum_subject_repo.get(
            curriculum_subject_id
        )

        if not curriculum_subject:
            raise NotFoundException(
                "Matière de la maquette introuvable"
            )

        # Vérification : le CurriculumSubject appartient bien
        # à une maquette (sans exiger ClassCurriculum, car dans notre
        # modèle la maquette est liée au niveau, pas directement à la classe).
        if not curriculum_subject.curriculum_id:
            raise ConflictException(
                "Cette matière n'est rattachée à aucune maquette"
            )

        # Vérifier qu'il n'existe pas déjà la même affectation
        existing_assignments = (
            await self.teacher_assignment_repo.get_by_class(
                class_id
            )
        )

        for assignment in existing_assignments:
            if (
                assignment.user_id == user_id
                and assignment.curriculum_subject_id
                == curriculum_subject_id
            ):
                raise ConflictException(
                    "Cet enseignant est déjà affecté à cette matière dans cette classe"
                )

        return await self.teacher_assignment_repo.create(
            {
                "user_id": user_id,
                "class_id": class_id,
                "curriculum_subject_id": curriculum_subject_id,
            }
        )

    async def list_by_class(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        await self._get_class(
            establishment_id,
            class_id,
        )

        return await self.teacher_assignment_repo.get_by_class(
            class_id
        )

    async def list_by_teacher(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        await self._get_teacher(
            establishment_id,
            user_id,
        )

        assignments = (
            await self.teacher_assignment_repo.get_by_teacher(
                user_id
            )
        )

        # Ne retourner que les affectations de cet établissement
        result = []

        for assignment in assignments:
            try:
                await self._get_class(
                    establishment_id,
                    assignment.class_id,
                )
                result.append(assignment)
            except NotFoundException:
                continue

        return result

    async def delete_assignment(
        self,
        establishment_id: uuid.UUID,
        assignment_id: uuid.UUID,
    ):
        assignment = await self.teacher_assignment_repo.get(
            assignment_id
        )

        if not assignment:
            raise NotFoundException(
                "Affectation introuvable"
            )

        # Vérifie que l'affectation appartient bien
        # à une classe de cet établissement
        await self._get_class(
            establishment_id,
            assignment.class_id,
        )

        return await self.teacher_assignment_repo.soft_delete(
            assignment
        )