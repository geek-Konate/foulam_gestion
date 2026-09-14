import resend

from app.core.config import settings


class EmailService:
    def __init__(self):
        resend.api_key = settings.resend_api_key

    async def send_invitation_email(
        self,
        recipient_email: str,
        recipient_name: str,
        invitation_token: str,
    ) -> None:
        invitation_link = (
            f"{settings.frontend_url}"
            f"/accept-invitation?token={invitation_token}"
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Invitation</title>
        </head>
        <body>
            <h2>Bienvenue sur FouLam Gestion School</h2>

            <p>Bonjour {recipient_name},</p>

            <p>
                Votre compte a été créé.
                Vous êtes invité à rejoindre la plateforme.
            </p>

            <p>
                Cliquez sur le bouton ci-dessous pour définir
                votre mot de passe et activer votre compte.
            </p>

            <p>
                <a href="{invitation_link}"
                   style="
                       display:inline-block;
                       padding:12px 20px;
                       background:#000;
                       color:#fff;
                       text-decoration:none;
                       border-radius:6px;
                   ">
                    Activer mon compte
                </a>
            </p>

            <p>
                Ce lien est valable pendant 48 heures.
            </p>

            <p>
                Si vous n'êtes pas à l'origine de cette demande,
                vous pouvez ignorer cet email.
            </p>

            <p>
                Cordialement,<br>
                FouLam Gestion School
            </p>
        </body>
        </html>
        """

        await resend.Emails.send_async(
            {
                "from": settings.resend_from_email,
                "to": [recipient_email],
                "subject": "Votre invitation – FouLam Gestion School",
                "html": html,
            }
        )