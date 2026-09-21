from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.curriculum import SubjectRepository
from app.schemas.curriculum import SubjectCreate, SubjectUpdate


class SubjectService:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    async def create_subject(self, data: SubjectCreate):
        existing = await self.subject_repo.get_by_name(data.name)

        if existing:
            raise ConflictException(
                "Une matière avec ce nom existe déjà"
            )

        return await self.subject_repo.create(
            data.model_dump()
        )

    async def list_subjects(self):
        return await self.subject_repo.list()

    async def get_subject(self, subject_id: UUID):
        subject = await self.subject_repo.get(subject_id)

        if not subject:
            raise NotFoundException("Matière introuvable")

        return subject

    async def update_subject(
        self,
        subject_id: UUID,
        data: SubjectUpdate,
    ):
        subject = await self.get_subject(subject_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing = await self.subject_repo.get_by_name(
                update_data["name"]
            )

            if existing and existing.id != subject.id:
                raise ConflictException(
                    "Une matière avec ce nom existe déjà"
                )

        return await self.subject_repo.update(
            subject,
            update_data,
        )

    async def delete_subject(self, subject_id: UUID):
        subject = await self.get_subject(subject_id)

        return await self.subject_repo.soft_delete(subject)