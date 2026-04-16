from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Visibility(models.TextChoices):
    PUBLIC = 'public', 'Público'
    PRIVATE = 'private', 'Privado'
    ADMINS = 'admins', 'Solo admins'


class Role(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Super Admin'
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'Usuario'


class User(AbstractUser):
    full_name = models.CharField(max_length=180, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_approved = models.BooleanField(default=False)

    def is_admin_like(self):
        return self.role in {Role.ADMIN, Role.SUPERADMIN}


class ClubSettings(models.Model):
    name = models.CharField(max_length=120, default='Mi Club de Lectura')
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    affiliate_tag = models.CharField(max_length=120, blank=True, default='')
    primary_color = models.CharField(max_length=7, default='#6f42c1')

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def effective_affiliate_tag(self):
        return 'bobybonilla0b-20'


class BookStatus(models.TextChoices):
    COMPLETED = 'completed', 'Leído'
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.amazon_url:
            self.amazon_url = build_amazon_url(self.title, ClubSettings.get_solo().effective_affiliate_tag)
        else:
            self.amazon_url = apply_affiliate_tag(self.amazon_url, ClubSettings.get_solo().effective_affiliate_tag)
        if not self.cover_url:
            self.cover_url = f'https://source.unsplash.com/featured/?book,{self.title.replace(" ", ",")}'
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=120, help_text='Sesión, intercambio, visita, restaurante, cine, etc.')
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


def build_amazon_url(title: str, affiliate_tag: str) -> str:
    query = urlencode({'k': title, 'tag': affiliate_tag})
    return f'https://www.amazon.com.mx/s?{query}'


def apply_affiliate_tag(url: str, affiliate_tag: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query['tag'] = [affiliate_tag]
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
