from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ─────────────────────────────────────────────
    # DATABASE
    # ─────────────────────────────────────────────

    db_user: str
    db_password: str
    db_host: str
    db_port: int = 5432
    db_name: str

    # ─────────────────────────────────────────────
    # JWT
    # ─────────────────────────────────────────────

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # ─────────────────────────────────────────────
    # SUPER ADMIN — PLATEFORME
    # ─────────────────────────────────────────────

    superadmin_email: EmailStr
    superadmin_password: str

    # ─────────────────────────────────────────────
    # INITIAL ORGANIZATION
    # ─────────────────────────────────────────────

    initial_organization_name: str
    initial_organization_slug: str

    initial_admin_first_name: str
    initial_admin_last_name: str
    initial_admin_email: EmailStr
    initial_admin_password: str

    initial_organization_country: str
    initial_organization_city: str

    # ─────────────────────────────────────────────
    # EMAIL / RESEND
    # ─────────────────────────────────────────────

    resend_api_key: str
    resend_from_email: str
    frontend_url: str

    # ─────────────────────────────────────────────
    # CONFIGURATION
    # ─────────────────────────────────────────────

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()