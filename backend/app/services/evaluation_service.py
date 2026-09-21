import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.academic import EvaluationRepository
from app.repositories.curriculum import (
    ClassCurriculumRepository,
    CurriculumSubjectRepository,
)
from app.repositories.student import (
    ClassRepository,
    AcademicYearRepository,
)


class EvaluationService:

    def __init__(
        self,
        evaluation_repo: EvaluationRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
        class_curriculum_repo: ClassCurriculumRepository,
        curriculum_subject_repo: CurriculumSubjectRepository,
    ):
        self.evaluation_repo = evaluation_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo
        self.class_curriculum_repo = class_curriculum_repo
        self.curriculum_subject_repo = curriculum_subject_repo

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
            raise NotFoundException(
                "Année scolaire introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def _validate_subject_for_class(
        self,
        class_id: uuid.UUID,
        subject_id: uuid.UUID,
    ):
        class_curriculum = (
            await self.class_curriculum_repo.get_by_class(
                class_id
            )
        )

        if not class_curriculum:
            raise ConflictException(
                "Aucune maquette n'est affectée à cette classe"
            )

        curriculum_subjects = (
            await self.curriculum_subject_repo.get_by_curriculum(
                class_curriculum.curriculum_id
            )
        )

        for curriculum_subject in curriculum_subjects:
            if curriculum_subject.subject_id == subject_id:
                return curriculum_subject

        raise ConflictException(
            "Cette matière n'est pas associée à la maquette de cette classe"
        )

    async def create_evaluation(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        await self._get_class(
            establishment_id,
            data.class_id,
        )

        await self._validate_subject_for_class(
            data.class_id,
            data.subject_id,
        )

        existing_evaluations = (
            await self.evaluation_repo.get_by_class_and_period(
                data.class_id,
                data.period,
            )
        )

        for evaluation in existing_evaluations:
            if (
                evaluation.subject_id == data.subject_id
                and evaluation.name.lower() == data.name.lower()
                and evaluation.date == data.date
            ):
                raise ConflictException(
                    "Cette évaluation existe déjà pour cette classe et cette matière"
                )

        return await self.evaluation_repo.create(
            data.model_dump()
        )

    async def list_evaluations(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
        period: str | None = None,
    ):
        await self._get_class(
            establishment_id,
            class_id,
        )

        if period is not None:
            return await self.evaluation_repo.get_by_class_and_period(
                class_id,
                period,
            )

        return await self.evaluation_repo.get_by_class(
            class_id
        )

    async def get_evaluation(
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

        await self._get_class(
            establishment_id,
            evaluation.class_id,
        )

        return evaluation

    async def delete_evaluation(
        self,
        establishment_id: uuid.UUID,
        evaluation_id: uuid.UUID,
    ):
        evaluation = await self.get_evaluation(
            establishment_id,
            evaluation_id,
        )

        return await self.evaluation_repo.soft_delete(
            evaluation
        )