import json
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse, quote_plus
from urllib.request import Request, urlopen
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Visibility(models.TextChoices):
    PUBLIC = 'public', 'Publico'
    PRIVATE = 'private', 'Privado'
    ADMINS = 'admins', 'Solo admins'


class Role(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Super Admin'
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'Usuario'


DEFAULT_TPL_WELCOME = """Hola {nombre},

Gracias por registrarte en {club}. Tu cuenta esta pendiente de aprobacion por un administrador.

Te avisaremos por correo cuando tu cuenta sea aprobada.

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_APPROVED = """Hola {nombre},

Tu cuenta en {club} ha sido aprobada. Ya puedes acceder al panel desde:

{url}/dashboard/

Bienvenido/a al club.

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_INVITATION = """Hola {nombre},

Has sido invitado/a a unirte a {club}.

Accede en: {url}/login/
Usuario: {usuario}
Contrasena temporal: {contrasena}

Te recomendamos cambiar tu contrasena al ingresar.

Saludos,
El equipo de {club}
"""


class User(AbstractUser):
    full_name = models.CharField(max_length=180, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_approved = models.BooleanField(default=False)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    favorite_book = models.CharField(max_length=255, blank=True)

    def is_admin_like(self):
        return self.is_superuser or self.role in {Role.ADMIN, Role.SUPERADMIN}

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = Role.SUPERADMIN
            self.is_approved = True
        super().save(*args, **kwargs)


class ClubSettings(models.Model):
    # Identidad
    name = models.CharField(max_length=120, default='Mi Club de Lectura')
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True, help_text='Logo rectangular para la navbar.')
    icon_url = models.URLField(blank=True, default='', help_text='Icono cuadrado 512x512 para PWA/favicon.')
    cover_image_url = models.URLField(blank=True, default='', help_text='Imagen de portada para la pagina principal.')
    primary_color = models.CharField(max_length=7, default='#6f42c1')
    accent_color = models.CharField(max_length=7, default='#5C3D2E')

    # Dominio publico
    public_domain = models.CharField(max_length=255, blank=True, default='', help_text='Dominio publico sin https://. Ej: miclub.com')

    # Amazon
    affiliate_tag = models.CharField(max_length=120, blank=True, default='')

    # Google OAuth
    google_login_enabled = models.BooleanField(default=False)
    google_client_id = models.CharField(max_length=255, blank=True, default='')
    google_client_secret = models.CharField(max_length=255, blank=True, default='')

    # SMTP
    smtp_host = models.CharField(max_length=255, blank=True, default='')
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_user = models.CharField(max_length=255, blank=True, default='')
    smtp_password = models.CharField(max_length=255, blank=True, default='')
    smtp_use_tls = models.BooleanField(default=True)
    email_from = models.CharField(max_length=255, blank=True, default='', help_text='Ej: Club de Lectura <club@midominio.com>')

    # Plantillas de correo
    email_tpl_welcome = models.TextField(blank=True, default='')
    email_tpl_approved = models.TextField(blank=True, default='')
    email_tpl_invitation = models.TextField(blank=True, default='')

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def effective_affiliate_tag(self):
        return self.affiliate_tag or settings.DEFAULT_AFFILIATE_TAG

    @property
    def nav_logo(self):
        return self.logo_url or self.icon_url

    @property
    def public_url(self):
        if self.public_domain:
            return f'https://{self.public_domain.rstrip("/")}'
        return getattr(settings, 'PUBLIC_BASE_URL', 'http://localhost:8787')

    @property
    def smtp_configured(self):
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)

    def get_welcome_template(self):
        return self.email_tpl_welcome or DEFAULT_TPL_WELCOME

    def get_approved_template(self):
        return self.email_tpl_approved or DEFAULT_TPL_APPROVED

    def get_invitation_template(self):
        return self.email_tpl_invitation or DEFAULT_TPL_INVITATION


class BookStatus(models.TextChoices):
    COMPLETED = 'completed', 'Leido'
    READING = 'reading', 'Leyendo'
    FUTURE = 'future', 'Por leer'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=BookStatus.choices, default=BookStatus.FUTURE)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    description = models.TextField(blank=True)
    amazon_url = models.URLField(blank=True)
    cover_url = models.URLField(blank=True)
    external_video_url = models.URLField(blank=True)
    pdf_url = models.URLField(blank=True)
    allow_voting = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        tag = ClubSettings.get_solo().effective_affiliate_tag
        if not self.amazon_url:
            self.amazon_url = build_amazon_url(self.title, tag)
        else:
            self.amazon_url = apply_affiliate_tag(self.amazon_url, tag)
        if not self.cover_url or not self.description or not self.author:
            metadata = fetch_book_metadata(self.title)
            self.cover_url = self.cover_url or metadata.get('cover_url', '')
            self.description = self.description or metadata.get('description', '')
            self.author = self.author or metadata.get('author', '')
        if not self.cover_url:
            self.cover_url = f'https://source.unsplash.com/featured/?book,{self.title.replace(" ", ",")}'
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    location = models.CharField(max_length=255, blank=True)
    external_video_url = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'book')


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    moderation_note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Invitation(models.Model):
    invited_name = models.CharField(max_length=180)
    email = models.EmailField()
    generated_password = models.CharField(max_length=120)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SocialLink(models.Model):
    network = models.CharField(max_length=80)
    url = models.URLField()


def build_amazon_url(title, affiliate_tag):
    query = urlencode({'k': title, 'tag': affiliate_tag})
    return f'https://www.amazon.com.mx/s?{query}'


def apply_affiliate_tag(url, affiliate_tag):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = [affiliate_tag]
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def fetch_book_metadata(title):
    metadata = fetch_from_google_books(title)
    if metadata.get('cover_url'):
        return metadata
    metadata_open = fetch_from_open_library(title)
    for key in ('cover_url', 'description', 'author'):
        if not metadata.get(key):
            metadata[key] = metadata_open.get(key, '')
    return metadata


def fetch_from_google_books(title):
    query = quote_plus(title)
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{query}&maxResults=1&langRestrict=es'
    data = _safe_json_get(url)
    items = data.get('items') or []
    if not items:
        return {}
    info = items[0].get('volumeInfo', {})
    image_links = info.get('imageLinks', {})
    authors = info.get('authors') or []
    return {
        'cover_url': image_links.get('thumbnail', '').replace('http://', 'https://'),
        'description': info.get('description', ''),
        'author': ', '.join(authors),
    }


def fetch_from_open_library(title):
    query = quote_plus(title)
    url = f'https://openlibrary.org/search.json?title={query}&limit=1'
    data = _safe_json_get(url)
    docs = data.get('docs') or []
    if not docs:
        return {}
    first = docs[0]
    cover_id = first.get('cover_i')
    authors = first.get('author_name') or []
    return {
        'cover_url': f'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg' if cover_id else '',
        'author': ', '.join(authors),
        'description': '',
    }


def _safe_json_get(url):
    req = Request(url, headers={'User-Agent': 'ClubLecturaBot/1.0'})
    try:
        with urlopen(req, timeout=5) as res:
            return json.loads(res.read().decode('utf-8'))
    except Exception:
        return {}