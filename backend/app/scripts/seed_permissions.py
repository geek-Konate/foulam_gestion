# app/scripts/seed_permissions.py

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.rbac import Permission, Role, RolePermission
from app.schemas.rbac import ScopeType


# ═══════════════════════════════════════════════════════
# PERMISSIONS SYSTÈME
# ═══════════════════════════════════════════════════════

PERMISSIONS = [
    # ─────────────────────────────────────────────
    # ONBOARDING
    # ─────────────────────────────────────────────
    (
        "onboarding.review",
        "Approuver ou rejeter une demande d'onboarding",
        "onboarding",
    ),

    # ─────────────────────────────────────────────
    # ORGANIZATION / SAAS
    # ─────────────────────────────────────────────

    ("organization.create", "Créer une organisation", "organization"),
    ("organization.read", "Consulter une organisation", "organization"),
    ("organization.update", "Modifier une organisation", "organization"),
    ("organization.delete", "Supprimer une organisation", "organization"),

    ("subscription.create", "Créer un abonnement", "organization"),
    ("subscription.read", "Consulter un abonnement", "organization"),
    ("subscription.update", "Modifier un abonnement", "organization"),
    ("subscription.delete", "Supprimer un abonnement", "organization"),

    ("establishment.create", "Créer un établissement", "organization"),
    ("establishment.read", "Consulter un établissement", "organization"),
    ("establishment.update", "Modifier un établissement", "organization"),
    ("establishment.delete", "Supprimer un établissement", "organization"),

    # ─────────────────────────────────────────────
    # RBAC
    # ─────────────────────────────────────────────
    ("user.create", "Créer un utilisateur", "rbac"),
    ("user.read", "Consulter un utilisateur", "rbac"),
    ("user.update", "Modifier un utilisateur", "rbac"),
    ("user.delete", "Supprimer un utilisateur", "rbac"),

    ("role.manage", "Gérer les rôles et permissions", "rbac"),
    ("role.assign", "Assigner un rôle à un utilisateur", "rbac"),

    # ─────────────────────────────────────────────
    # STRUCTURE SCOLAIRE
    # ─────────────────────────────────────────────
    (
        "academic_year.create",
        "Créer une année académique",
        "academic_structure",
    ),
    (
        "academic_year.read",
        "Consulter les années académiques",
        "academic_structure",
    ),
    (
        "academic_year.update",
        "Modifier une année académique",
        "academic_structure",
    ),
    (
        "academic_year.delete",
        "Supprimer une année académique",
        "academic_structure",
    ),
    (
        "class.create",
        "Créer une classe",
        "academic_structure",
    ),
    (
        "class.read",
        "Consulter une classe",
        "academic_structure",
    ),
    (
        "class.update",
        "Modifier une classe",
        "academic_structure",
    ),

    # ─────────────────────────────────────────────
    # ÉLÈVES
    # ─────────────────────────────────────────────
    ("student.create", "Créer un élève", "student"),
    ("student.read", "Consulter un élève", "student"),
    ("student.update", "Modifier un élève", "student"),
    (
        "student.enroll",
        "Inscrire un élève dans une classe",
        "student",
    ),

    ("guardian.create", "Créer un tuteur", "student"),
    ("guardian.read", "Consulter un tuteur", "student"),

    # ─────────────────────────────────────────────
    # MAQUETTE PÉDAGOGIQUE
    # ─────────────────────────────────────────────
    (
        "curriculum.create",
        "Créer une maquette pédagogique",
        "curriculum",
    ),
    (
        "curriculum.read",
        "Consulter une maquette pédagogique",
        "curriculum",
    ),
    (
        "subject.create",
        "Créer une matière",
        "curriculum",
    ),
    (
        "teacher_assignment.create",
        "Affecter un enseignant",
        "curriculum",
    ),

    # ─────────────────────────────────────────────
    # NOTES / PRÉSENCES
    # ─────────────────────────────────────────────
    (
        "evaluation.create",
        "Créer une évaluation",
        "academic",
    ),
    (
        "evaluation.read",
        "Consulter une évaluation",
        "academic",
    ),

    ("grade.create", "Saisir une note", "academic"),
    ("grade.update", "Modifier une note", "academic"),
    ("grade.read", "Consulter une note", "academic"),

    (
        "attendance.create",
        "Saisir une présence/absence",
        "academic",
    ),
    (
        "attendance.read",
        "Consulter les présences",
        "academic",
    ),

    (
        "report_card.generate",
        "Générer un bulletin",
        "academic",
    ),
    (
        "report_card.read",
        "Consulter un bulletin",
        "academic",
    ),

    # ─────────────────────────────────────────────
    # FINANCE
    # ─────────────────────────────────────────────
    (
        "fee_type.create",
        "Créer un type de frais",
        "finance",
    ),
    (
        "fee_type.read",
        "Consulter les types de frais",
        "finance",
    ),

    (
        "payment.create",
        "Enregistrer un paiement",
        "finance",
    ),
    (
        "payment.read",
        "Consulter les paiements",
        "finance",
    ),

    (
        "receipt.read",
        "Consulter un reçu",
        "finance",
    ),
]


# ═══════════════════════════════════════════════════════
# RÔLES SYSTÈME
# ═══════════════════════════════════════════════════════

SYSTEM_ROLES = [
    {
        "name": "Super Admin",
        "description": "Administrateur global de la plateforme SaaS",
        "scope_type": ScopeType.PLATFORM,
            "is_system": True,
    },
]


# ═══════════════════════════════════════════════════════
# SEED PERMISSIONS
# ═══════════════════════════════════════════════════════

async def create_permissions(session) -> dict[str, Permission]:
    """
    Crée les permissions manquantes.

    Retourne toutes les permissions sous forme :
        {
            "permission.code": Permission
        }
    """

    result = await session.execute(
        select(Permission)
    )

    permissions = {
        permission.code: permission
        for permission in result.scalars().all()
    }

    created = 0

    for code, name, module in PERMISSIONS:

        if code in permissions:
            continue

        permission = Permission(
            code=code,
            name=name,
            module=module,
        )

        session.add(permission)
        permissions[code] = permission
        created += 1

    if created:
        await session.flush()

    print(
        f"✅ Permissions : {created} créée(s), "
        f"{len(PERMISSIONS) - created} déjà existante(s)."
    )

    return permissions


# ═══════════════════════════════════════════════════════
# SEED RÔLES
# ═══════════════════════════════════════════════════════

async def seed_roles(session) -> dict[str, Role]:
    """
    Crée les rôles système manquants.
    """

    result = await session.execute(
        select(Role)
    )

    roles = {
        role.name: role
        for role in result.scalars().all()
    }

    created = 0

    for role_data in SYSTEM_ROLES:

        role_name = role_data["name"]

        if role_name in roles:
            continue

        role = Role(
            name=role_data["name"],
            description=role_data["description"],
            scope_type=role_data["scope_type"],
            is_system=role_data["is_system"],
        )

        session.add(role)
        roles[role_name] = role
        created += 1

    if created:
        await session.flush()

    print(
        f"✅ Rôles : {created} créé(s), "
        f"{len(SYSTEM_ROLES) - created} déjà existant(s)."
    )

    return roles


# ═══════════════════════════════════════════════════════
# SUPER ADMIN → PERMISSIONS
# ═══════════════════════════════════════════════════════

async def seed_superadmin_permissions(
    session,
    roles: dict[str, Role],
    permissions: dict[str, Permission],
) -> None:
    """
    Donne toutes les permissions au Super Admin.
    """

    superadmin_role = roles.get("Super Admin")

    if not superadmin_role:
        raise RuntimeError(
            "Le rôle 'Super Admin' n'existe pas."
        )

    result = await session.execute(
        select(RolePermission.permission_id).where(
            RolePermission.role_id == superadmin_role.id
        )
    )

    existing_permission_ids = {
        permission_id
        for permission_id in result.scalars().all()
    }

    created = 0

    for permission in permissions.values():

        if permission.id in existing_permission_ids:
            continue

        session.add(
            RolePermission(
                role_id=superadmin_role.id,
                permission_id=permission.id,
            )
        )

        created += 1

    if created:
        await session.flush()

    print(
        f"✅ Permissions Super Admin : "
        f"{created} ajoutée(s)."
    )


# ═══════════════════════════════════════════════════════
# SEED GLOBAL
# ═══════════════════════════════════════════════════════

async def seed_permissions() -> None:

    async with AsyncSessionLocal() as session:

        try:
            permissions = await create_permissions(session)

            roles = await seed_roles(session)

            await seed_superadmin_permissions(
                session,
                roles,
                permissions,
            )

            await session.commit()

            print("════════════════════════════════════")
            print("✅ Seed RBAC terminé avec succès")
            print("════════════════════════════════════")

        except Exception:
            await session.rollback()
            raise


# ═══════════════════════════════════════════════════════
# EXECUTION DIRECTE
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    asyncio.run(seed_permissions())