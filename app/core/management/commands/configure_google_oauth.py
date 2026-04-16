import os
from django.core.management.base import BaseCommand, CommandError
from core.models import ClubSettings
from core.oauth import sync_google_social_app_from_settings


class Command(BaseCommand):
    help = 'Configura Google OAuth leyendo primero ClubSettings (dashboard) y fallback opcional al entorno.'

    def handle(self, *args, **options):
        cfg = ClubSettings.get_solo()

        env_client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        env_client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')

        if not cfg.google_client_id and env_client_id:
            cfg.google_client_id = env_client_id
        if not cfg.google_client_secret and env_client_secret:
            cfg.google_client_secret = env_client_secret

        if not cfg.google_client_id or not cfg.google_client_secret:
            raise CommandError('Configura google_client_id y google_client_secret en Dashboard (ClubSettings).')

        cfg.google_login_enabled = True
        cfg.save(update_fields=['google_client_id', 'google_client_secret', 'google_login_enabled'])
        sync_google_social_app_from_settings()

        self.stdout.write(self.style.SUCCESS('Google OAuth configurado correctamente desde ClubSettings.'))
