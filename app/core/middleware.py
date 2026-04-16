from django.http import HttpResponseNotFound
from core.models import ClubSettings


class GoogleLoginToggleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/accounts/google/'):
            if not ClubSettings.get_solo().google_login_enabled:
                return HttpResponseNotFound('Google login deshabilitado por el super admin.')
        return self.get_response(request)
