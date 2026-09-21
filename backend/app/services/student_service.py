from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    async def create_student(
        self,
        establishment_id: UUID,
        data: StudentCreate,
    ):
        existing_students = await self.student_repo.search_by_name(
            data.first_name,
            data.last_name,
        )

        for student in existing_students:
            if student.establishment_id == establishment_id:
                raise ConflictException(
                    "Un élève avec ce nom existe déjà dans cet établissement"
                )

        student_data = data.model_dump()
        student_data["establishment_id"] = establishment_id

        return await self.student_repo.create(student_data)

    async def list_students(
        self,
        establishment_id: UUID,
    ):
        return await self.student_repo.get_by_establishment(
            establishment_id
        )

    async def get_student(
        self,
        establishment_id: UUID,
        student_id: UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException("Élève introuvable")

        if student.establishment_id != establishment_id:
            raise NotFoundException("Élève introuvable")

        return student

    async def update_student(
        self,
        establishment_id: UUID,
        student_id: UUID,
        data: StudentUpdate,
    ):
        student = await self.get_student(
            establishment_id,
            student_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        return await self.student_repo.update(
            student,
            update_data,
        )

    async def delete_student(
        self,
        establishment_id: UUID,
        student_id: UUID,
    ):
        student = await self.get_student(
            establishment_id,
            student_id,
        )

        return await self.student_repo.soft_delete(student)