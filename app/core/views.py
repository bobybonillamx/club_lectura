import secrets
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.db.utils import DatabaseError, OperationalError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import (
    RegisterForm,
    BookForm,
    EventForm,
    ReviewForm,
    ClubSettingsForm,
    SocialLinkForm,
    UserProfileForm,
)
from .oauth import sync_google_social_app_from_settings
from .models import (
    Book,
    BookStatus,
    Role,
    User,
    Vote,
    Review,
    Event,
    Visibility,
    Invitation,
    SocialLink,
    ClubSettings,
)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _is_effectively_approved(user):
    return bool(user.is_authenticated and (user.is_superuser or user.is_approved))


def _visible_filter(user):
    if user.is_authenticated and (user.role == Role.SUPERADMIN or user.is_superuser):
        return list(Visibility.values)
    if user.is_authenticated and user.role == Role.ADMIN:
        return [Visibility.PUBLIC, Visibility.ADMINS]
    return [Visibility.PUBLIC]


def _send_email_safe(subject, body, to):
    """Send mail swallowing errors so it never breaks a request."""
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to], fail_silently=True)
    except Exception:
        pass


# ──────────────────────────────────────────────
# Public views
# ──────────────────────────────────────────────

def home(request):
    visible = _visible_filter(request.user)
    books = Book.objects.none()
    current_book = None
    next_event = None
    events = Event.objects.none()
    links = SocialLink.objects.none()

    try:
        books = (
            Book.objects.filter(visibility__in=visible)
            .prefetch_related('reviews', 'votes')
            .order_by('-created_at')[:30]
        )
        current_book = (
            Book.objects.filter(visibility__in=visible, status=BookStatus.READING)
            .order_by('-created_at')
            .first()
        )
        next_event = (
            Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now())
            .order_by('starts_at')
            .first()
        )
        events = (
            Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now())
            .order_by('starts_at')[:20]
        )
        links = SocialLink.objects.all()
    except (DatabaseError, OperationalError):
        messages.warning(
            request,
            'No se pudieron cargar todos los datos. Verifica que las migraciones estén aplicadas.',
        )

    return render(request, 'home.html', {
        'books': books,
        'events': events,
        'current_book': current_book,
        'next_event': next_event,
        'links': links,
        'book_status': BookStatus,
    })


def books_page(request):
    visible = _visible_filter(request.user)
    status = request.GET.get('estado', '')
    query = request.GET.get('q', '').strip()

    qs = Book.objects.filter(visibility__in=visible).order_by('-created_at')

    if status in {BookStatus.COMPLETED, BookStatus.READING, BookStatus.FUTURE}:
        qs = qs.filter(status=status)

    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(author__icontains=query))

    return render(request, 'books_page.html', {
        'books': qs,
        'estado': status,
        'query': query,
    })


def book_detail(request, book_id):
    visible = _visible_filter(request.user)
    book = get_object_or_404(Book, pk=book_id, visibility__in=visible)
    approved_reviews = book.reviews.filter(is_approved=True).order_by('-created_at')
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(user=request.user, book=book).first()
    return render(request, 'book_detail.html', {
        'book': book,
        'approved_reviews': approved_reviews,
        'book_status': BookStatus,
        'user_vote': user_vote,
    })


def events_page(request):
    visible = _visible_filter(request.user)
    now = timezone.now()
    upcoming = Event.objects.filter(visibility__in=visible, starts_at__gte=now).order_by('starts_at')
    past = Event.objects.filter(visibility__in=visible, starts_at__lt=now).order_by('-starts_at')
    return render(request, 'events_page.html', {'upcoming': upcoming, 'past': past})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_approved = False
            user.role = Role.USER
            user.save()
            # Notify admins
            admin_emails = list(
                User.objects.filter(
                    role__in=[Role.ADMIN, Role.SUPERADMIN], is_approved=True
                ).values_list('email', flat=True)
            )
            for email in admin_emails:
                _send_email_safe(
                    subject=f'[{_club_name()}] Nuevo usuario pendiente: {user.username}',
                    body=(
                        f'El usuario {user.username} ({user.email}) se ha registrado '
                        f'y está esperando aprobación.\n\n'
                        f'Apruébalo desde el dashboard: {settings.PUBLIC_BASE_URL}/dashboard/?seccion=usuarios'
                    ),
                    to=email,
                )
            messages.success(
                request,
                'Tu cuenta fue creada. Un administrador debe aprobarla antes de que puedas acceder al panel.',
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


# ──────────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────────

@login_required
def dashboard(request):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Tu cuenta está pendiente de aprobación por un administrador.')

    section = request.GET.get('seccion', 'inicio')
    club_settings = ClubSettings.get_solo()
    settings_form = ClubSettingsForm(instance=club_settings)
    if request.user.role != Role.SUPERADMIN and not request.user.is_superuser:
        for f in ('google_login_enabled', 'google_client_id', 'google_client_secret'):
            settings_form.fields.pop(f, None)

    # Stats
    stats = _build_stats()

    context = {
        'seccion': section,
        'book_form': BookForm(),
        'event_form': EventForm(),
        'settings_form': settings_form,
        'social_form': SocialLinkForm(),
        'profile_form': UserProfileForm(instance=request.user),
        'books': Book.objects.order_by('-created_at')[:100],
        'events_all': Event.objects.order_by('-starts_at')[:100],
        'users_all': User.objects.order_by('-date_joined')[:100],
        'users_pending': User.objects.filter(is_approved=False),
        'reviews_pending': Review.objects.filter(is_approved=False).order_by('-created_at'),
        'reviews_all': Review.objects.order_by('-created_at')[:200],
        'social_links': SocialLink.objects.all(),
        'pending_reviews_count': Review.objects.filter(is_approved=False).count(),
        'stats': stats,
        'default_affiliate_tag': settings.DEFAULT_AFFILIATE_TAG,
    }
    return render(request, 'dashboard.html', context)


def _club_name():
    try:
        return ClubSettings.get_solo().name
    except Exception:
        return 'Club de Lectura'


def _build_stats():
    top_voted = (
        Book.objects.filter(status=BookStatus.FUTURE)
        .annotate(vote_count=Count('votes'))
        .filter(vote_count__gt=0)
        .order_by('-vote_count')[:5]
    )
    return {
        'total_books': Book.objects.count(),
        'books_read': Book.objects.filter(status=BookStatus.COMPLETED).count(),
        'total_votes': Vote.objects.count(),
        'approved_users': User.objects.filter(is_approved=True).count(),
        'top_voted': top_voted,
        'recent_reviews': Review.objects.filter(is_approved=True).select_related('book', 'user').order_by('-created_at')[:5],
    }


# ──────────────────────────────────────────────
# Settings
# ──────────────────────────────────────────────

@login_required
def update_club_settings(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')

    club_settings = ClubSettings.get_solo()
    form = ClubSettingsForm(request.POST, instance=club_settings)
    if request.user.role != Role.SUPERADMIN and not request.user.is_superuser:
        for f in ('google_login_enabled', 'google_client_id', 'google_client_secret'):
            form.fields.pop(f, None)
    if form.is_valid():
        form.save()
        if request.user.role == Role.SUPERADMIN or request.user.is_superuser:
            sync_google_social_app_from_settings()
        messages.success(request, 'Configuración del club actualizada.')
    else:
        messages.error(request, f'Error de configuración: {form.errors}')
    section = request.POST.get('seccion', 'inicio')
    return redirect(f'/dashboard/?seccion={section}')


# ──────────────────────────────────────────────
# Books
# ──────────────────────────────────────────────

@login_required
def create_book(request):
    if not request.user.is_admin_like() or not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Solo admins aprobados.')
    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        if book.status == BookStatus.READING and form.cleaned_data.get('reemplazar_leyendo_actual'):
            Book.objects.filter(status=BookStatus.READING).exclude(id=book.id).update(status=BookStatus.COMPLETED)
        messages.success(request, f'Libro "{book.title}" guardado correctamente.')
    else:
        messages.error(request, f'Error al guardar libro: {form.errors}')
    return redirect('/dashboard/?seccion=libros')


@login_required
def edit_book(request, book_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    book = get_object_or_404(Book, pk=book_id)
    # Partial inline edit from dashboard (title/author/status only)
    book.title = request.POST.get('title', book.title).strip() or book.title
    book.author = request.POST.get('author', book.author).strip()
    new_status = request.POST.get('status', book.status)
    if new_status in dict(BookStatus.choices):
        book.status = new_status
    book.save(update_fields=['title', 'author', 'status'])
    messages.success(request, 'Libro actualizado.')
    return redirect('/dashboard/?seccion=libros')


@login_required
def delete_book(request, book_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Libro eliminado.')
    return redirect('/dashboard/?seccion=libros')


# ──────────────────────────────────────────────
# Events
# ──────────────────────────────────────────────

@login_required
def create_event(request):
    if not request.user.is_admin_like() or not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Solo admins aprobados.')
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, 'Evento creado correctamente.')
    else:
        messages.error(request, f'Error al crear evento: {form.errors}')
    return redirect('/dashboard/?seccion=eventos')


@login_required
def edit_event(request, event_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    event = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, 'Evento actualizado.')
    else:
        messages.error(request, f'No se pudo actualizar evento: {form.errors}')
    return redirect('/dashboard/?seccion=eventos')


@login_required
def delete_event(request, event_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Evento eliminado.')
    return redirect('/dashboard/?seccion=eventos')


# ──────────────────────────────────────────────
# Voting & Reviews
# ──────────────────────────────────────────────

@login_required
def vote_book(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobación para votar.')
    book = get_object_or_404(Book, pk=book_id, status=BookStatus.FUTURE, allow_voting=True)
    vote, created = Vote.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f'Voto registrado por "{book.title}".')
    else:
        messages.info(request, f'Ya habías votado por "{book.title}".')
    return redirect(request.POST.get('next') or f'/libros/{book.id}/')


@login_required
def add_review(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobación para reseñar.')
    book = get_object_or_404(Book, pk=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.is_approved = False
        review.save()
        messages.success(request, 'Reseña enviada. Aparecerá una vez que un admin la apruebe.')
    return redirect(request.POST.get('next') or 'home')


@login_required
def review_moderation(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    reviews = Review.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'review_moderation.html', {'reviews': reviews})


@login_required
def approve_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.is_approved = True
    review.is_flagged = False
    review.moderation_note = request.POST.get('moderation_note', '').strip()
    review.save(update_fields=['is_approved', 'is_flagged', 'moderation_note'])
    messages.success(request, 'Reseña aprobada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def flag_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.is_approved = False
    review.is_flagged = True
    review.moderation_note = request.POST.get('moderation_note', '').strip() or 'Marcada por moderación'
    review.save(update_fields=['is_approved', 'is_flagged', 'moderation_note'])
    messages.success(request, 'Reseña marcada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def delete_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Reseña eliminada.')
    return redirect('/dashboard/?seccion=resenas')


# ──────────────────────────────────────────────
# Users
# ──────────────────────────────────────────────

@login_required
def pending_users(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    users = User.objects.filter(is_approved=False)
    return render(request, 'pending_users.html', {'users': users})


@login_required
def approve_user(request, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    user = get_object_or_404(User, pk=user_id)
    user.is_approved = True
    user.save(update_fields=['is_approved'])
    # Notify user
    if user.email:
        _send_email_safe(
            subject=f'Tu cuenta en {_club_name()} fue aprobada',
            body=(
                f'Hola {user.username},\n\n'
                f'Tu cuenta en {_club_name()} ha sido aprobada. '
                f'Ya puedes acceder al panel desde:\n{settings.PUBLIC_BASE_URL}/dashboard/\n\n'
                f'¡Bienvenido/a!'
            ),
            to=user.email,
        )
    messages.success(request, f'{user.username} aprobado.')
    return redirect('/dashboard/?seccion=usuarios')


@login_required
def edit_user(request, user_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    user = get_object_or_404(User, pk=user_id)
    user.full_name = request.POST.get('full_name', user.full_name)
    user.email = request.POST.get('email', user.email)
    user.favorite_book = request.POST.get('favorite_book', user.favorite_book)
    user.save()
    messages.success(request, 'Usuario actualizado.')
    return redirect('/dashboard/?seccion=usuarios')


@login_required
def delete_user(request, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    user = get_object_or_404(User, pk=user_id)
    if user.id == request.user.id:
        return HttpResponseForbidden('No puedes eliminarte a ti mismo.')
    user.delete()
    messages.success(request, 'Usuario eliminado.')
    return redirect('/dashboard/?seccion=usuarios')


@login_required
def invite_user(request):
    if request.user.role not in {Role.ADMIN, Role.SUPERADMIN} and not request.user.is_superuser:
        return HttpResponseForbidden('Solo admins.')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        role = request.POST.get('role', Role.USER)
        if role == Role.ADMIN and request.user.role != Role.SUPERADMIN and not request.user.is_superuser:
            return HttpResponseForbidden('Solo el superadmin puede crear admins.')

        alphabet = string.ascii_letters + string.digits + '!@#$%'
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        username = email.split('@')[0]
        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'full_name': name,
            'role': role,
            'is_approved': True,
        })
        if created:
            user.set_password(password)
            user.save()

        Invitation.objects.create(
            invited_name=name,
            email=email,
            generated_password=password,
            invited_by=request.user,
        )
        invite_link = f'{settings.PUBLIC_BASE_URL}/login/'

        # Send invitation email
        _send_email_safe(
            subject=f'Invitación a {_club_name()}',
            body=(
                f'Hola {name},\n\n'
                f'Has sido invitado/a a unirte a {_club_name()}.\n\n'
                f'Accede en: {invite_link}\n'
                f'Usuario: {username}\n'
                f'Contraseña temporal: {password}\n\n'
                f'Te recomendamos cambiar tu contraseña al ingresar.'
            ),
            to=email,
        )
        messages.success(
            request,
            f'Invitación creada para {email}. Contraseña temporal: {password}. '
            f'Se envió un correo de invitación (si el servidor de correo está configurado).',
        )
    return redirect('/dashboard/?seccion=usuarios')


# ──────────────────────────────────────────────
# Social links & Profile
# ──────────────────────────────────────────────

@login_required
def add_social_link(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    form = SocialLinkForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Red social agregada.')
    else:
        messages.error(request, f'Error: {form.errors}')
    return redirect('/dashboard/?seccion=integraciones')


@login_required
def delete_social_link(request, link_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    link = get_object_or_404(SocialLink, pk=link_id)
    link.delete()
    messages.success(request, 'Red social eliminada.')
    return redirect('/dashboard/?seccion=integraciones')


@login_required
def edit_profile(request):
    form = UserProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Perfil actualizado.')
    else:
        messages.error(request, f'Error al actualizar perfil: {form.errors}')
    return redirect('/dashboard/?seccion=perfil')


# ──────────────────────────────────────────────
# PWA
# ──────────────────────────────────────────────


def manifest(request):
    import json as _json
    cfg = ClubSettings.get_solo()
    icons = []
    if cfg.icon_url:
        icons = [
            {"src": cfg.icon_url, "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
            {"src": cfg.icon_url, "sizes": "192x192", "type": "image/png"},
        ]
    data = {
        "name": cfg.name,
        "short_name": cfg.name[:12],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F7F3EE",
        "theme_color": cfg.primary_color or "#6f42c1",
        "icons": icons,
    }
    return HttpResponse(_json.dumps(data), content_type='application/manifest+json')


def service_worker(_request):
    return HttpResponse("self.addEventListener('fetch', () => {});", content_type='application/javascript')