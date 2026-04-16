from django.http import HttpResponseNotFound
from core.models import ClubSettings


class GoogleLoginToggleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/accounts/google/'):
            cfg = ClubSettings.get_solo()
            if not (cfg.google_login_enabled and cfg.google_client_id and cfg.google_client_secret):
                return HttpResponseNotFound('Google login deshabilitado por el super admin.')
        return self.get_response(request)
