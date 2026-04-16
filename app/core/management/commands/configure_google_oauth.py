import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Configura automáticamente Google OAuth en django-allauth usando variables de entorno.'

    def handle(self, *args, **options):
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise CommandError('Faltan GOOGLE_CLIENT_ID y/o GOOGLE_CLIENT_SECRET en el entorno.')

        site, _ = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8787', 'name': 'Club Lectura'})

        app, _ = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth Club Lectura',
                'client_id': client_id,
                'secret': client_secret,
            },
        )
        app.client_id = client_id
        app.secret = client_secret
        app.save()
        app.sites.add(site)

        self.stdout.write(self.style.SUCCESS('Google OAuth configurado correctamente en SocialApp.'))
