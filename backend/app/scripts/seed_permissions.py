from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rbac import (
    Permission,
    Role,
    RolePermission,
    ScopeType,
)


PERMISSIONS = [
    # ============================================================
    # ONBOARDING
    # ============================================================
    {
        "code": "onboarding.review",
        "name": "Examiner les demandes d'inscription",
        "module": "onboarding",
        "description": "Permet d'accepter ou de refuser les demandes d'inscription.",
    },

    # ============================================================
    # ORGANIZATION
    # ============================================================
    {
        "code": "organization.create",
        "name": "Créer une organisation",
        "module": "organization",
        "description": "Permet de créer une organisation.",
    },
    {
        "code": "organization.read",
        "name": "Consulter les organisations",
        "module": "organization",
        "description": "Permet de consulter les organisations.",
    },
    {
        "code": "organization.update",
        "name": "Modifier une organisation",
        "module": "organization",
        "description": "Permet de modifier une organisation.",
    },
    {
        "code": "organization.delete",
        "name": "Supprimer une organisation",
        "module": "organization",
        "description": "Permet de supprimer une organisation.",
    },

    # ============================================================
    # SUBSCRIPTION
    # ============================================================
    {
        "code": "subscription.create",
        "name": "Créer un abonnement",
        "module": "subscription",
        "description": "Permet de créer un abonnement.",
    },
    {
        "code": "subscription.read",
        "name": "Consulter les abonnements",
        "module": "subscription",
        "description": "Permet de consulter les abonnements.",
    },
    {
        "code": "subscription.update",
        "name": "Modifier un abonnement",
        "module": "subscription",
        "description": "Permet de modifier un abonnement.",
    },
    {
        "code": "subscription.delete",
        "name": "Supprimer un abonnement",
        "module": "subscription",
        "description": "Permet de supprimer un abonnement.",
    },

    # ============================================================
    # ESTABLISHMENT
    # ============================================================
    {
        "code": "establishment.create",
        "name": "Créer un établissement",
        "module": "establishment",
        "description": "Permet de créer un établissement.",
    },
    {
        "code": "establishment.read",
        "name": "Consulter les établissements",
        "module": "establishment",
        "description": "Permet de consulter les établissements.",
    },
    {
        "code": "establishment.update",
        "name": "Modifier un établissement",
        "module": "establishment",
        "description": "Permet de modifier un établissement.",
    },
    {
        "code": "establishment.delete",
        "name": "Supprimer un établissement",
        "module": "establishment",
        "description": "Permet de supprimer un établissement.",
    },

    # ============================================================
    # USER
    # ============================================================
    {
        "code": "user.create",
        "name": "Créer un utilisateur",
        "module": "user",
        "description": "Permet de créer un utilisateur.",
    },
    {
        "code": "user.read",
        "name": "Consulter les utilisateurs",
        "module": "user",
        "description": "Permet de consulter les utilisateurs.",
    },
    {
        "code": "user.update",
        "name": "Modifier un utilisateur",
        "module": "user",
        "description": "Permet de modifier un utilisateur.",
    },
    {
        "code": "user.delete",
        "name": "Supprimer un utilisateur",
        "module": "user",
        "description": "Permet de supprimer un utilisateur.",
    },

    # ============================================================
    # ROLE / RBAC
    # ============================================================
    {
        "code": "role.manage",
        "name": "Gérer les rôles",
        "module": "role",
        "description": "Permet de créer, modifier et supprimer les rôles.",
    },
    {
        "code": "role.assign",
        "name": "Attribuer les rôles",
        "module": "role",
        "description": "Permet d'attribuer des rôles aux utilisateurs.",
    },

    # ============================================================
    # ACADEMIC YEAR
    # ============================================================
    {
        "code": "academic_year.create",
        "name": "Créer une année scolaire",
        "module": "academic_year",
        "description": "Permet de créer une année scolaire.",
    },
    {
        "code": "academic_year.read",
        "name": "Consulter les années scolaires",
        "module": "academic_year",
        "description": "Permet de consulter les années scolaires.",
    },
    {
        "code": "academic_year.update",
        "name": "Modifier une année scolaire",
        "module": "academic_year",
        "description": "Permet de modifier une année scolaire.",
    },
    {
        "code": "academic_year.delete",
        "name": "Supprimer une année scolaire",
        "module": "academic_year",
        "description": "Permet de supprimer une année scolaire.",
    },

    # ============================================================
    # LEVEL
    # ============================================================
    {
        "code": "level.create",
        "name": "Créer un niveau",
        "module": "level",
        "description": "Permet de créer un niveau.",
    },
    {
        "code": "level.read",
        "name": "Consulter les niveaux",
        "module": "level",
        "description": "Permet de consulter les niveaux.",
    },
    {
        "code": "level.update",
        "name": "Modifier un niveau",
        "module": "level",
        "description": "Permet de modifier un niveau.",
    },
    {
        "code": "level.delete",
        "name": "Supprimer un niveau",
        "module": "level",
        "description": "Permet de supprimer un niveau.",
    },

    # ============================================================
    # CLASS
    # ============================================================
    {
        "code": "class.create",
        "name": "Créer une classe",
        "module": "class",
        "description": "Permet de créer une classe.",
    },
    {
        "code": "class.read",
        "name": "Consulter les classes",
        "module": "class",
        "description": "Permet de consulter les classes.",
    },
    {
        "code": "class.update",
        "name": "Modifier une classe",
        "module": "class",
        "description": "Permet de modifier une classe.",
    },
    {
        "code": "class.delete",
        "name": "Supprimer une classe",
        "module": "class",
        "description": "Permet de supprimer une classe.",
    },

    # ============================================================
    # STUDENT
    # ============================================================
    {
        "code": "student.create",
        "name": "Créer un élève",
        "module": "student",
        "description": "Permet d'enregistrer un élève.",
    },
    {
        "code": "student.read",
        "name": "Consulter les élèves",
        "module": "student",
        "description": "Permet de consulter les élèves.",
    },
    {
        "code": "student.update",
        "name": "Modifier un élève",
        "module": "student",
        "description": "Permet de modifier les informations d'un élève.",
    },
    {
        "code": "student.enroll",
        "name": "Inscrire un élève",
        "module": "student",
        "description": "Permet d'inscrire un élève dans une classe.",
    },
    {
        "code": "student.delete",
        "name": "Supprimer un élève",
        "module": "student",
        "description": "Permet de supprimer un élève.",
    },

    # ============================================================
    # GUARDIAN
    # ============================================================
    {
        "code": "guardian.create",
        "name": "Créer un responsable",
        "module": "guardian",
        "description": "Permet d'enregistrer un responsable.",
    },
    {
        "code": "guardian.read",
        "name": "Consulter les responsables",
        "module": "guardian",
        "description": "Permet de consulter les responsables.",
    },
    {
        "code": "guardian.update",
        "name": "Modifier un responsable",
        "module": "guardian",
        "description": "Permet de modifier un responsable.",
    },
    {
        "code": "guardian.delete",
        "name": "Supprimer un responsable",
        "module": "guardian",
        "description": "Permet de supprimer un responsable.",
    },

    # ============================================================
    # CURRICULUM
    # ============================================================
    {
        "code": "curriculum.create",
        "name": "Créer une maquette",
        "module": "curriculum",
        "description": "Permet de créer une maquette pédagogique.",
    },
    {
        "code": "curriculum.read",
        "name": "Consulter les maquettes",
        "module": "curriculum",
        "description": "Permet de consulter les maquettes pédagogiques.",
    },
    {
        "code": "curriculum.update",
        "name": "Modifier une maquette",
        "module": "curriculum",
        "description": "Permet de modifier une maquette pédagogique.",
    },
    {
        "code": "curriculum.delete",
        "name": "Supprimer une maquette",
        "module": "curriculum",
        "description": "Permet de supprimer une maquette pédagogique.",
    },

    # ============================================================
    # SUBJECT
    # ============================================================
    {
        "code": "subject.create",
        "name": "Créer une matière",
        "module": "subject",
        "description": "Permet de créer une matière.",
    },
    {
        "code": "subject.read",
        "name": "Consulter les matières",
        "module": "subject",
        "description": "Permet de consulter les matières.",
    },
    {
        "code": "subject.update",
        "name": "Modifier une matière",
        "module": "subject",
        "description": "Permet de modifier une matière.",
    },
    {
        "code": "subject.delete",
        "name": "Supprimer une matière",
        "module": "subject",
        "description": "Permet de supprimer une matière.",
    },

    # ============================================================
    # TEACHER ASSIGNMENT
    # ============================================================
    {
        "code": "teacher_assignment.create",
        "name": "Affecter un enseignant",
        "module": "teacher_assignment",
        "description": "Permet d'affecter un enseignant à une classe et une matière.",
    },
    {
        "code": "teacher_assignment.read",
        "name": "Consulter les affectations",
        "module": "teacher_assignment",
        "description": "Permet de consulter les affectations des enseignants.",
    },
    {
        "code": "teacher_assignment.delete",
        "name": "Supprimer une affectation",
        "module": "teacher_assignment",
        "description": "Permet de supprimer une affectation.",
    },

    # ============================================================
    # EVALUATION
    # ============================================================
    {
        "code": "evaluation.create",
        "name": "Créer une évaluation",
        "module": "evaluation",
        "description": "Permet de créer une évaluation.",
    },
    {
        "code": "evaluation.read",
        "name": "Consulter les évaluations",
        "module": "evaluation",
        "description": "Permet de consulter les évaluations.",
    },
    {
        "code": "evaluation.delete",
        "name": "Supprimer une évaluation",
        "module": "evaluation",
        "description": "Permet de supprimer une évaluation.",
    },

    # ============================================================
    # GRADE
    # ============================================================
    {
        "code": "grade.create",
        "name": "Saisir une note",
        "module": "grade",
        "description": "Permet de saisir une note.",
    },
    {
        "code": "grade.update",
        "name": "Modifier une note",
        "module": "grade",
        "description": "Permet de modifier une note.",
    },
    {
        "code": "grade.read",
        "name": "Consulter les notes",
        "module": "grade",
        "description": "Permet de consulter les notes.",
    },

    # ============================================================
    # ATTENDANCE
    # ============================================================
    {
        "code": "attendance.create",
        "name": "Enregistrer une présence",
        "module": "attendance",
        "description": "Permet d'enregistrer une présence ou une absence.",
    },
    {
        "code": "attendance.read",
        "name": "Consulter les présences",
        "module": "attendance",
        "description": "Permet de consulter les présences et absences.",
    },
    {
        "code": "attendance.update",
        "name": "Modifier une présence",
        "module": "attendance",
        "description": "Permet de modifier une présence ou une absence.",
    },
    {
        "code": "attendance.delete",
        "name": "Supprimer une présence",
        "module": "attendance",
        "description": "Permet de supprimer une présence ou une absence.",
    },

    # ============================================================
    # REPORT CARD
    # ============================================================
    {
        "code": "report_card.generate",
        "name": "Générer un bulletin",
        "module": "report_card",
        "description": "Permet de générer un bulletin scolaire.",
    },
    {
        "code": "report_card.read",
        "name": "Consulter les bulletins",
        "module": "report_card",
        "description": "Permet de consulter les bulletins scolaires.",
    },

    # ============================================================
    # ENROLLMENT
    # ============================================================
    {
        "code": "enrollment.create",
        "name": "Créer une inscription",
        "module": "enrollment",
        "description": "Permet de créer une inscription dans une classe.",
    },
    {
        "code": "enrollment.read",
        "name": "Consulter les inscriptions",
        "module": "enrollment",
        "description": "Permet de consulter les inscriptions.",
    },
    {
        "code": "enrollment.update",
        "name": "Modifier une inscription",
        "module": "enrollment",
        "description": "Permet de modifier une inscription.",
    },
    {
        "code": "enrollment.delete",
        "name": "Supprimer une inscription",
        "module": "enrollment",
        "description": "Permet de supprimer une inscription.",
    },

    # ============================================================
    # FEE TYPE
    # ============================================================
    {
        "code": "fee_type.create",
        "name": "Créer un type de frais",
        "module": "fee_type",
        "description": "Permet de créer un type de frais scolaire.",
    },
    {
        "code": "fee_type.read",
        "name": "Consulter les types de frais",
        "module": "fee_type",
        "description": "Permet de consulter les types de frais scolaires.",
    },
    {
        "code": "fee_type.update",
        "name": "Modifier un type de frais",
        "module": "fee_type",
        "description": "Permet de modifier un type de frais scolaire.",
    },
    {
        "code": "fee_type.delete",
        "name": "Supprimer un type de frais",
        "module": "fee_type",
        "description": "Permet de supprimer un type de frais scolaire.",
    },

    # ============================================================
    # PAYMENT
    # ============================================================
    {
        "code": "payment.create",
        "name": "Enregistrer un paiement",
        "module": "payment",
        "description": "Permet d'enregistrer un paiement.",
    },
    {
        "code": "payment.read",
        "name": "Consulter les paiements",
        "module": "payment",
        "description": "Permet de consulter les paiements.",
    },
    {
        "code": "payment.delete",
        "name": "Supprimer un paiement",
        "module": "payment",
        "description": "Permet de supprimer un paiement.",
    },

    # ============================================================
    # RECEIPT
    # ============================================================
    {
        "code": "receipt.read",
        "name": "Consulter les reçus",
        "module": "receipt",
        "description": "Permet de consulter les reçus de paiement.",
    },
    {
        "code": "receipt.create",
        "name": "Créer un reçu",
        "module": "receipt",
        "description": "Permet de créer un reçu de paiement.",
    },
    {
        "code": "receipt.delete",
        "name": "Supprimer un reçu",
        "module": "receipt",
        "description": "Permet de supprimer un reçu de paiement.",
    },

    # ============================================================
    # DASHBOARD
    # ============================================================
    {
        "code": "dashboard.read",
        "name": "Consulter le tableau de bord",
        "module": "dashboard",
        "description": "Permet de consulter les tableaux de bord.",
    },
]


SYSTEM_ROLES = {
    "super_admin": {
        "name": "Super Admin",
        "description": "Administrateur global de la plateforme.",
        "scope_type": "PLATFORM",
    },
}


async def seed_permissions(session: AsyncSession) -> dict:
    created = 0
    existing = 0

    for permission_data in PERMISSIONS:
        result = await session.execute(
            select(Permission).where(
                Permission.code == permission_data["code"]
            )
        )

        permission = result.scalar_one_or_none()

        if permission:
            existing += 1
            continue

        permission = Permission(**permission_data)
        session.add(permission)
        created += 1

    await session.commit()

    return {
        "created": created,
        "existing": existing,
        "total": len(PERMISSIONS),
    }
async def seed_system_roles(session: AsyncSession) -> dict:
    created = 0
    existing = 0
    permissions_added = 0

    for role_data in SYSTEM_ROLES.values():
        scope_type = ScopeType(role_data["scope_type"])

        result = await session.execute(
            select(Role).where(
                Role.name == role_data["name"],
                Role.scope_type == scope_type,
                Role.organization_id.is_(None),
                Role.establishment_id.is_(None),
                Role.deleted_at.is_(None),
            )
        )
        role = result.scalar_one_or_none()

        if role is None:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
                scope_type=scope_type,
                organization_id=None,
                establishment_id=None,
                is_system=True,
            )
            session.add(role)
            await session.flush()
            created += 1
        else:
            role.is_system = True
            existing += 1

        # Charger toutes les associations déjà présentes,
        # y compris celles qui ont été supprimées logiquement.
        result = await session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role.id
            )
        )
        associations = result.scalars().all()
        associations_by_permission = {
            association.permission_id: association
            for association in associations
        }

        # Récupérer les permissions actives.
        result = await session.execute(
            select(Permission).where(
                Permission.deleted_at.is_(None)
            )
        )
        permissions = result.scalars().all()

        for permission in permissions:
            association = associations_by_permission.get(permission.id)

            if association is not None:
                # Réactiver une association supprimée logiquement.
                if association.deleted_at is not None:
                    association.deleted_at = None
                    permissions_added += 1
                continue

            session.add(
                RolePermission(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )
            permissions_added += 1

    await session.commit()

    return {
        "created": created,
        "existing": existing,
        "permissions_added": permissions_added,
        "total": len(SYSTEM_ROLES),
    }