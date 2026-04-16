from core.models import ClubSettings


def branding(_request):
    settings_obj = ClubSettings.get_solo()
    return {
        'club_settings': settings_obj,
    }
