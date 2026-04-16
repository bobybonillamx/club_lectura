from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from core.models import ClubSettings


def sync_google_social_app_from_settings() -> None:
    cfg = ClubSettings.get_solo()

    if not (cfg.google_login_enabled and cfg.google_client_id and cfg.google_client_secret):
        return

    site, _ = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8787', 'name': 'Club Lectura'})
    app, _ = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth Club Lectura',
            'client_id': cfg.google_client_id,
            'secret': cfg.google_client_secret,
        },
    )
    app.client_id = cfg.google_client_id
    app.secret = cfg.google_client_secret
    app.save()
    app.sites.add(site)
