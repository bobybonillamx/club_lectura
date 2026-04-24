import json
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse, quote_plus
from urllib.request import Request, urlopen
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Visibility(models.TextChoices):
    PUBLIC = 'public', 'Publico'
    PRIVATE = 'private', 'Privado'
    ADMINS = 'admins', 'Solo admins'


class Role(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Super Admin'
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'Usuario'


THEMES = {
    'literario_cafe': {
        'label': 'Literario Cafe',
        'page': '#F7F3EE', 'surface': '#FFFFFF', 'border': '#EAE0D5', 'border2': '#DDD4C8',
        'primary': '#3D2B1F', 'accent': '#B87333', 'accent_bg': '#FDF3E3', 'accent_bdr': '#F0D8A8',
        'ink': '#1A0F0A', 'ink_mid': '#3D2B1F', 'ink_light': '#7A6252',
        'serif': "'Lora', Georgia, serif", 'sans': "'Inter', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap',
    },
    'moderno_oscuro': {
        'label': 'Moderno Oscuro',
        'page': '#111318', 'surface': '#1C2030', 'border': '#2A2F42', 'border2': '#363C52',
        'primary': '#7C6FFF', 'accent': '#A89FFF', 'accent_bg': '#2A2050', 'accent_bdr': '#5A50A0',
        'ink': '#F0EFFF', 'ink_mid': '#D8D6F8', 'ink_light': '#9A9EBB',
        'chip_reading_bg': '#0D2E0D', 'chip_reading_ink': '#7EE87E',
        'chip_done_bg': '#0D0D2E', 'chip_done_ink': '#9999FF',
        'chip_future_bg': '#2A2050', 'chip_future_ink': '#C0B8FF', 'chip_future_bdr': '#5A50A0',
        'chip_muted_bg': '#1C2030', 'chip_muted_ink': '#9A9EBB', 'chip_muted_bdr': '#363C52',
        'serif': "'Space Grotesk', system-ui, sans-serif", 'sans': "'Space Grotesk', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&display=swap',
    },
    'minimalista_blanco': {
        'label': 'Minimalista Blanco',
        'page': '#FAFAFA', 'surface': '#FFFFFF', 'border': '#EBEBEB', 'border2': '#D8D8D8',
        'primary': '#111111', 'accent': '#111111', 'accent_bg': '#F5F5F5', 'accent_bdr': '#E0E0E0',
        'ink': '#111111', 'ink_mid': '#333333', 'ink_light': '#888888',
        'serif': "'DM Sans', system-ui, sans-serif", 'sans': "'DM Sans', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap',
    },
    'verde_bosque': {
        'label': 'Verde Bosque',
        'page': '#F2F7F2', 'surface': '#FFFFFF', 'border': '#D4E8D4', 'border2': '#B8D8B8',
        'primary': '#1E4D2B', 'accent': '#3A7D44', 'accent_bg': '#E8F5E8', 'accent_bdr': '#AEDCAE',
        'ink': '#0F2B18', 'ink_mid': '#1E4D2B', 'ink_light': '#4A6B52',
        'serif': "'Crimson Pro', Georgia, serif", 'sans': "'Inter', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap',
    },
    'oceano_profundo': {
        'label': 'Oceano Profundo',
        'page': '#EEF4FA', 'surface': '#FFFFFF', 'border': '#C8DDEF', 'border2': '#A8C8E8',
        'primary': '#0B4F8A', 'accent': '#1A72C4', 'accent_bg': '#DFF0FB', 'accent_bdr': '#9DCFF0',
        'ink': '#051E3A', 'ink_mid': '#0B4F8A', 'ink_light': '#3A6080',
        'serif': "'Libre Baskerville', Georgia, serif", 'sans': "'Inter', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap',
    },
    'rosa_editorial': {
        'label': 'Rosa Editorial',
        'page': '#FDF6F8', 'surface': '#FFFFFF', 'border': '#F0D8E0', 'border2': '#E8C0CC',
        'primary': '#8B2252', 'accent': '#C4547A', 'accent_bg': '#FCEAF0', 'accent_bdr': '#F0B8CC',
        'ink': '#3D0A22', 'ink_mid': '#8B2252', 'ink_light': '#8B5A6A',
        'serif': "'Playfair Display', Georgia, serif", 'sans': "'Plus Jakarta Sans', system-ui, sans-serif",
        'fonts': 'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap',
    },
}

THEME_CHOICES = [(k, v['label']) for k, v in THEMES.items()]

DEFAULT_TPL_WELCOME = """Hola {nombre},

Gracias por registrarte en {club}. Tu cuenta esta pendiente de aprobacion.

Te avisaremos cuando sea aprobada.

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_APPROVED = """Hola {nombre},

Tu cuenta en {club} ha sido aprobada. Accede en:

{url}/dashboard/

Bienvenido/a al club.

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_INVITATION = """Hola {nombre},

Has sido invitado/a a {club}.

Accede en: {url}/login/
Usuario: {usuario}
Contrasena temporal: {contrasena}

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_NEW_BOOK = """Hola {nombre},

Hay un nuevo libro en {club}: {titulo} de {autor}.

Verlo en: {url}/libros/{libro_id}/

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_NEW_EVENT = """Hola {nombre},

Nuevo evento en {club}: {titulo}

Fecha: {fecha}
{lugar}

Ver detalles en: {url}/eventos/

Saludos,
El equipo de {club}
"""

DEFAULT_TPL_VOTING = """Hola {nombre},

La votacion para el proximo libro esta abierta en {club}.

Vota en: {url}/libros/

Saludos,
El equipo de {club}
"""


class User(AbstractUser):
    full_name = models.CharField(max_length=180, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_approved = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
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
    logo_url = models.URLField(blank=True)
    icon_url = models.URLField(blank=True, default='')
    cover_image_url = models.URLField(blank=True, default='')
    primary_color = models.CharField(max_length=7, default='')
    accent_color = models.CharField(max_length=7, default='')

    # Tema
    theme = models.CharField(max_length=40, default='literario_cafe', choices=THEME_CHOICES)

    # SEO
    meta_description = models.CharField(max_length=260, blank=True, default='')
    meta_keywords = models.CharField(max_length=255, blank=True, default='')
    meta_author = models.CharField(max_length=120, blank=True, default='')

    # Textos
    home_welcome_text = models.CharField(max_length=255, blank=True, default='')
    cta_register_text = models.CharField(max_length=60, blank=True, default='')
    cta_login_text = models.CharField(max_length=60, blank=True, default='')

    # Footer
    footer_text = models.CharField(max_length=255, blank=True, default='')
    footer_custom_link_text = models.CharField(max_length=120, blank=True, default='')
    footer_custom_link_url = models.URLField(blank=True, default='')

    # Dominio
    public_domain = models.CharField(max_length=255, blank=True, default='')

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
    email_from = models.CharField(max_length=255, blank=True, default='')

    # Email templates
    email_tpl_welcome = models.TextField(blank=True, default='')
    email_tpl_approved = models.TextField(blank=True, default='')
    email_tpl_invitation = models.TextField(blank=True, default='')
    email_tpl_new_book = models.TextField(blank=True, default='')
    email_tpl_new_event = models.TextField(blank=True, default='')
    email_tpl_voting_open = models.TextField(blank=True, default='')

    # Custom font
    custom_font_url = models.CharField(max_length=500, blank=True, default='')
    custom_font_serif = models.CharField(max_length=120, blank=True, default='')
    custom_font_sans = models.CharField(max_length=120, blank=True, default='')

    # Notifications
    notify_new_book = models.BooleanField(default=False)
    notify_new_event = models.BooleanField(default=False)
    notify_voting_open = models.BooleanField(default=False)
    notify_pending_approvals = models.BooleanField(default=False)
    last_cron_run = models.DateTimeField(null=True, blank=True)

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

    @property
    def theme_vars(self):
        base = THEMES.get(self.theme, THEMES['literario_cafe']).copy()
        if self.primary_color:
            base['primary'] = self.primary_color
            base['ink_mid'] = self.primary_color
        if self.accent_color:
            base['accent'] = self.accent_color
        if self.custom_font_serif and self.custom_font_url:
            base['serif'] = f"'{self.custom_font_serif}', Georgia, serif"
            if self.custom_font_sans:
                base['sans'] = f"'{self.custom_font_sans}', system-ui, sans-serif"
            base['fonts'] = self.custom_font_url
        if 'chip_reading_bg' not in base:
            base['chip_reading_bg'] = '#EBF5EB'
            base['chip_reading_ink'] = '#2D5A2D'
        if 'chip_done_bg' not in base:
            base['chip_done_bg'] = '#EEF0F8'
            base['chip_done_ink'] = '#2D3A6A'
        if 'chip_future_bg' not in base:
            base['chip_future_bg'] = base.get('accent_bg', '#FDF3E3')
            base['chip_future_ink'] = base.get('accent', '#B87333')
            base['chip_future_bdr'] = base.get('accent_bdr', '#F0D8A8')
        if 'chip_muted_bg' not in base:
            base['chip_muted_bg'] = base.get('page', '#F7F3EE')
            base['chip_muted_ink'] = base.get('ink_light', '#7A6252')
            base['chip_muted_bdr'] = base.get('border', '#EAE0D5')
        return base

    @property
    def effective_cta_register(self):
        return self.cta_register_text or 'Registro'

    @property
    def effective_cta_login(self):
        return self.cta_login_text or 'Entrar'

    def get_welcome_template(self):
        return self.email_tpl_welcome or DEFAULT_TPL_WELCOME

    def get_approved_template(self):
        return self.email_tpl_approved or DEFAULT_TPL_APPROVED

    def get_invitation_template(self):
        return self.email_tpl_invitation or DEFAULT_TPL_INVITATION

    def get_new_book_template(self):
        return self.email_tpl_new_book or DEFAULT_TPL_NEW_BOOK

    def get_new_event_template(self):
        return self.email_tpl_new_event or DEFAULT_TPL_NEW_EVENT

    def get_voting_template(self):
        return self.email_tpl_voting_open or DEFAULT_TPL_VOTING


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    is_default = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


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
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    reading_month = models.CharField(max_length=7, blank=True, default='', help_text='Mes planeado YYYY-MM.')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        tag = ClubSettings.get_solo().effective_affiliate_tag
        # Auto-fetch metadata if any field is missing
        isbn = ''
        if not self.author or not self.cover_url or not self.description:
            metadata = fetch_book_metadata(self.title, self.author)
            self.cover_url = self.cover_url or metadata.get('cover_url', '')
            self.description = self.description or metadata.get('description', '')
            self.author = self.author or metadata.get('author', '')
            isbn = metadata.get('isbn', '')
            # Auto-assign category if found and not set
            if not self.category_id and metadata.get('categories'):
                cat_name = metadata['categories'][0].split('/')[0].strip()
                cat = Category.objects.filter(
                    Q(name__iexact=cat_name) | Q(name__icontains=cat_name[:6])
                ).first()
                if cat:
                    self.category = cat
        # Build Amazon URL - use ISBN for direct product link when available
        if not self.amazon_url:
            self.amazon_url = build_amazon_url(self.title, tag, isbn)
        else:
            self.amazon_url = apply_affiliate_tag(self.amazon_url, tag)
        if not self.cover_url:
            self.cover_url = f'https://source.unsplash.com/featured/?book,{quote_plus(self.title)}'
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    location = models.CharField(max_length=255, blank=True)
    external_video_url = models.URLField(blank=True)
    cover_image_url = models.URLField(blank=True, default='')
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


SOCIAL_ICON_CHOICES = [
    ('link', 'Enlace generico'), ('instagram', 'Instagram'), ('facebook', 'Facebook'),
    ('twitter', 'Twitter / X'), ('whatsapp', 'WhatsApp'), ('telegram', 'Telegram'),
    ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('spotify', 'Spotify'),
    ('email', 'Correo electronico'), ('website', 'Sitio web'),
]

class SocialLink(models.Model):
    network = models.CharField(max_length=80)
    url = models.URLField()
    icon = models.CharField(max_length=30, blank=True, default='link', choices=SOCIAL_ICON_CHOICES)


def build_amazon_url(title, affiliate_tag, isbn=''):
    if isbn:
        # Direct product search by ISBN is much more accurate
        params = urlencode({'field-keywords': isbn, 'tag': affiliate_tag})
        return f'https://www.amazon.com.mx/s?{params}'
    query = urlencode({'k': title, 'tag': affiliate_tag})
    return f'https://www.amazon.com.mx/s?{query}'


def apply_affiliate_tag(url, affiliate_tag):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = [affiliate_tag]
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def fetch_book_metadata(title, author_hint=''):
    query = f'{title} {author_hint}'.strip() if author_hint else title
    metadata = fetch_from_google_books(query)
    if not metadata.get('cover_url'):
        metadata_open = fetch_from_open_library(title)
        for key in ('cover_url', 'description', 'author'):
            if not metadata.get(key):
                metadata[key] = metadata_open.get(key, '')
    return metadata


def fetch_from_google_books(title):
    query = quote_plus(title)
    # Fetch more results to find the most popular/relevant edition
    url = f'https://www.googleapis.com/books/v1/volumes?q={quote_plus(title)}&maxResults=10&orderBy=relevance'
    data = _safe_json_get(url)
    items = data.get('items') or []
    if not items:
        return {}

    # Score each result: prefer high ratingsCount, has image, has authors
    def score(item):
        info = item.get('volumeInfo', {})
        s = 0
        if info.get('imageLinks'):
            s += 10
        if info.get('authors'):
            s += 5
        s += min(info.get('ratingsCount', 0), 1000) // 100
        if info.get('description'):
            s += 3
        if info.get('industryIdentifiers'):
            s += 2
        return s

    best = max(items, key=score)
    info = best.get('volumeInfo', {})
    image_links = info.get('imageLinks', {})
    authors = info.get('authors') or []

    # Get best quality image available
    cover = (image_links.get('extraLarge') or image_links.get('large') or
             image_links.get('medium') or image_links.get('thumbnail') or '')
    cover = cover.replace('http://', 'https://')
    # Request higher zoom for better quality
    if 'zoom=' in cover:
        import re as _re
        cover = _re.sub('zoom=[0-9]+', 'zoom=2', cover)

    return {
        'cover_url': cover,
        'description': info.get('description', ''),
        'author': ', '.join(authors),
        'categories': info.get('categories') or [],
        'isbn': next((i['identifier'] for i in info.get('industryIdentifiers', [])
                      if i['type'] in ('ISBN_13', 'ISBN_10')), ''),
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
