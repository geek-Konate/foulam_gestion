class AppException(Exception):
    status_code: int = 500
    detail: str = "Erreur interne"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundException(AppException):
    status_code = 404
    detail = "Ressource introuvable"


class ConflictException(AppException):
    status_code = 409
    detail = "Conflit sur la ressource"


class ForbiddenException(AppException):
    status_code = 403
    detail = "Action non autorisée"


class UnauthorizedException(AppException):
    status_code = 401
    detail = "Authentification requise"


class ValidationException(AppException):
    status_code = 422
    detail = "Données invalides"