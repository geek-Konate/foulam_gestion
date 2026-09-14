# app/scripts/seed_superadmin.py

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.rbac import User
from app.models.rbac import Role
from app.models.rbac import UserRole

from app.core.security import hash_password


SUPERADMIN_ROLE = "Super Admin"


async def seed_superadmin() -> None:
    async with AsyncSessionLocal() as session:
        # ─────────────────────────────────────────
        # 1. Vérifier si le Super Admin existe
        # ─────────────────────────────────────────
        result = await session.execute(
            select(User).where(
                User.email == settings.superadmin_email
            )
        )

        user = result.scalar_one_or_none()

        if user:
            print(
                f"⚠️ Super Admin déjà existant : "
                f"{settings.superadmin_email}"
            )
            return

        # ─────────────────────────────────────────
        # 2. Récupérer le rôle Super Admin
        # ─────────────────────────────────────────
        result = await session.execute(
            select(Role).where(
                Role.name == SUPERADMIN_ROLE
            )
        )

        role = result.scalar_one_or_none()

        if not role:
            raise RuntimeError(
                "❌ Le rôle 'Super Admin' n'existe pas. "
                "Crée d'abord les rôles système."
            )

        # ─────────────────────────────────────────
        # 3. Créer le Super Admin
        # ─────────────────────────────────────────
        admin = User(
            first_name="Super",
            last_name="Admin",
            email=settings.superadmin_email,
            password_hash=hash_password(
                settings.superadmin_password
            ),
            status="active",
        )

        session.add(admin)

        # Flush pour obtenir admin.id
        await session.flush()

        # ─────────────────────────────────────────
        # 4. Assigner le rôle
        # ─────────────────────────────────────────
        user_role = UserRole(
            user_id=admin.id,
            role_id=role.id,
        )

        session.add(user_role)

        # ─────────────────────────────────────────
        # 5. Commit
        # ─────────────────────────────────────────
        await session.commit()

        print(
            f"✅ Super Admin créé : "
            f"{settings.superadmin_email}"
        )


if __name__ == "__main__":
    asyncio.run(seed_superadmin())