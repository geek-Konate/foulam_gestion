import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.academic import EvaluationRepository
from app.repositories.student import ClassRepository, AcademicYearRepository


class EvaluationService:

    def __init__(
        self,
        evaluation_repo: EvaluationRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.evaluation_repo = evaluation_repo
        self.class_repo = class_repo
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
            raise NotFoundException(
                "Année scolaire introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def create_evaluation(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        await self._get_class(
            establishment_id,
            data.class_id,
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