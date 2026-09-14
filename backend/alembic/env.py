# alembic/env.py
from logging.config import fileConfig
import sys
from pathlib import Path

from app.core.database import encoded_password

# Force l'ajout du chemin du projet
sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from urllib.parse import quote_plus  # Ajouté pour reconstruire l'URL comme dans ton database.py
from alembic import context

# 1. Importe ta base, tes modèles et tes réglages centralisés
from app.models import Base
from app.core.config import settings

# Cet objet config donne accès aux valeurs du fichier alembic.ini.
config = context.config

# 2. RECONSTRUCTION DYNAMIQUE DE L'URL (Évite la duplication dans alembic.ini)
encode_password = quote_plus(settings.db_password)
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{encoded_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

# Crucial pour Alembic : On escape le caractère % en %% pour éviter le bug de configparser
DATABASE_URL_ALEMBIC = DATABASE_URL.replace("%", "%%")

# On injecte l'URL protégée dans la configuration d'Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL_ALEMBIC)
# Configure le logging si le fichier de conf existe
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Indique à Alembic où trouver la structure de tes tables
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Exécute les migrations en mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Exécute les migrations en mode 'online' (avec connexion active)."""
    # Ici, engine_from_config va lire l'URL qu'on a injectée plus haut via set_main_option
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()