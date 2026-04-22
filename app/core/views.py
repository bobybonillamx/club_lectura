import secrets
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, get_connection
from django.http import HttpResponse, HttpResponseForbidden
from django.db.utils import DatabaseError, OperationalError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import (
    RegisterForm, BookForm, EventForm, ReviewForm,
    ClubSettingsForm, SocialLinkForm, UserProfileForm,
)
from .oauth import sync_google_social_app_from_settings
from .models import (
    Book, BookStatus, Role, User, Vote, Review, Event,
    Visibility, Invitation, SocialLink, ClubSettings,
    DEFAULT_TPL_WELCOME, DEFAULT_TPL_APPROVED, DEFAULT_TPL_INVITATION,
    THEMES,
)


def _is_effectively_approved(user):
    return bool(user.is_authenticated and (user.is_superuser or user.is_approved))


def _visible_filter(user):
    if user.is_authenticated and (user.role == Role.SUPERADMIN or user.is_superuser):
        return list(Visibility.values)
    if user.is_authenticated and user.role == Role.ADMIN:
        return [Visibility.PUBLIC, Visibility.ADMINS]
    return [Visibility.PUBLIC]


def _send_email(subject, body, to, cfg=None):
    if cfg is None:
        cfg = ClubSettings.get_solo()
    try:
        if cfg.smtp_configured:
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=cfg.smtp_host, port=cfg.smtp_port,
                username=cfg.smtp_user, password=cfg.smtp_password,
                use_tls=cfg.smtp_use_tls, fail_silently=False,
            )
            from_email = cfg.email_from or f'{cfg.name} <{cfg.smtp_user}>'
        else:
            connection = None
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost')
        send_mail(subject, body, from_email, [to], connection=connection, fail_silently=True)
    except Exception:
        pass


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


def home(request):
    visible = _visible_filter(request.user)
    books = Book.objects.none()
    current_book = None
    next_event = None
    events = Event.objects.none()
    links = SocialLink.objects.none()
    try:
        books = Book.objects.filter(visibility__in=visible).prefetch_related('reviews', 'votes').order_by('-created_at')[:30]
        current_book = Book.objects.filter(visibility__in=visible, status=BookStatus.READING).order_by('-created_at').first()
        next_event = Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now()).order_by('starts_at').first()
        events = Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now()).order_by('starts_at')[:20]
        links = SocialLink.objects.all()
    except (DatabaseError, OperationalError):
        messages.warning(request, 'No se pudieron cargar todos los datos.')
    return render(request, 'home.html', {
        'books': books, 'events': events, 'current_book': current_book,
        'next_event': next_event, 'links': links, 'book_status': BookStatus,
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
    return render(request, 'books_page.html', {'books': qs, 'estado': status, 'query': query})


def book_detail(request, book_id):
    visible = _visible_filter(request.user)
    book = get_object_or_404(Book, pk=book_id, visibility__in=visible)
    approved_reviews = book.reviews.filter(is_approved=True).order_by('-created_at')
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(user=request.user, book=book).first()
    return render(request, 'book_detail.html', {
        'book': book, 'approved_reviews': approved_reviews,
        'book_status': BookStatus, 'user_vote': user_vote,
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
            cfg = ClubSettings.get_solo()
            admin_emails = list(
                User.objects.filter(role__in=[Role.ADMIN, Role.SUPERADMIN], is_approved=True)
                .values_list('email', flat=True)
            )
            for email in admin_emails:
                _send_email(
                    subject=f'[{cfg.name}] Nuevo usuario pendiente: {user.username}',
                    body=f'El usuario {user.username} ({user.email}) se ha registrado.\n\n{cfg.public_url}/dashboard/?seccion=usuarios',
                    to=email, cfg=cfg,
                )
            if user.email:
                body = cfg.get_welcome_template().format(
                    nombre=user.username, club=cfg.name, url=cfg.public_url, usuario=user.username,
                )
                _send_email(subject=f'Bienvenido a {cfg.name}', body=body, to=user.email, cfg=cfg)
            messages.success(request, 'Tu cuenta fue creada. Un administrador debe aprobarla.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def dashboard(request):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Tu cuenta esta pendiente de aprobacion.')

    section = request.GET.get('seccion', 'inicio')
    cfg = ClubSettings.get_solo()
    settings_form = ClubSettingsForm(instance=cfg)
    if not (request.user.role == Role.SUPERADMIN or request.user.is_superuser):
        for f in ('google_login_enabled', 'google_client_id', 'google_client_secret',
                  'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_use_tls',
                  'email_from', 'email_tpl_welcome', 'email_tpl_approved', 'email_tpl_invitation',
                  'public_domain'):
            settings_form.fields.pop(f, None)

    context = {
        'seccion': section,
        'settings_form': settings_form,
        'social_form': SocialLinkForm(),
        'profile_form': UserProfileForm(instance=request.user),
        'books': Book.objects.order_by('-created_at')[:100],
        'events_all': Event.objects.order_by('-starts_at')[:100],
        'users_all': User.objects.order_by('-date_joined')[:100],
        'users_pending': User.objects.filter(is_approved=False),
        'reviews_all': Review.objects.order_by('-created_at')[:200],
        'social_links': SocialLink.objects.all(),
        'pending_reviews_count': Review.objects.filter(is_approved=False).count(),
        'stats': _build_stats(),
        'cfg': cfg,
        'theme_choices': list(THEMES.items()),
        'default_tpl_welcome': DEFAULT_TPL_WELCOME,
        'default_tpl_approved': DEFAULT_TPL_APPROVED,
        'default_tpl_invitation': DEFAULT_TPL_INVITATION,
    }
    return render(request, 'dashboard.html', context)


@login_required
def update_club_settings(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')

    cfg = ClubSettings.get_solo()
    section = request.POST.get('seccion', 'inicio')

    section_fields = {
        'inicio': ['name', 'description', 'logo_url', 'icon_url', 'cover_image_url',
                   'home_welcome_text', 'meta_description', 'cta_register_text', 'cta_login_text'],
        'apariencia': ['theme', 'primary_color', 'accent_color',
                       'footer_custom_link_text', 'footer_custom_link_url', 'footer_text'],
        'integraciones': ['public_domain', 'affiliate_tag',
                          'google_login_enabled', 'google_client_id', 'google_client_secret',
                          'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_use_tls', 'email_from'],
        'correos': ['email_tpl_welcome', 'email_tpl_approved', 'email_tpl_invitation'],
    }

    allowed = section_fields.get(section, section_fields['inicio'])
    form = ClubSettingsForm(request.POST, instance=cfg)
    for f in list(form.fields.keys()):
        if f not in allowed:
            form.fields.pop(f)

    if not (request.user.role == Role.SUPERADMIN or request.user.is_superuser):
        for f in ('google_login_enabled', 'google_client_id', 'google_client_secret',
                  'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_use_tls',
                  'email_from', 'public_domain'):
            form.fields.pop(f, None)

    if form.is_valid():
        form.save()
        if section == 'integraciones':
            sync_google_social_app_from_settings()
        messages.success(request, 'Configuracion guardada.')
    else:
        messages.error(request, f'Error: {form.errors}')

    return redirect(f'/dashboard/?seccion={section}')


@login_required
def reset_colors(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    cfg = ClubSettings.get_solo()
    cfg.primary_color = ''
    cfg.accent_color = ''
    cfg.save(update_fields=['primary_color', 'accent_color'])
    messages.success(request, 'Colores restablecidos al tema.')
    return redirect('/dashboard/?seccion=apariencia')


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
        messages.success(request, f'Libro "{book.title}" guardado.')
    else:
        messages.error(request, f'Error: {form.errors}')
    return redirect('/dashboard/?seccion=libros')


@login_required
def edit_book(request, book_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    book = get_object_or_404(Book, pk=book_id)
    book.title = request.POST.get('title', book.title).strip() or book.title
    book.author = request.POST.get('author', book.author).strip()
    book.description = request.POST.get('description', book.description).strip()
    book.cover_url = request.POST.get('cover_url', book.cover_url).strip()
    book.amazon_url = request.POST.get('amazon_url', book.amazon_url).strip()
    book.pdf_url = request.POST.get('pdf_url', book.pdf_url).strip()
    book.external_video_url = request.POST.get('external_video_url', book.external_video_url).strip()
    new_status = request.POST.get('status', book.status)
    if new_status in dict(BookStatus.choices):
        book.status = new_status
    new_vis = request.POST.get('visibility', book.visibility)
    if new_vis in dict(Visibility.choices):
        book.visibility = new_vis
    book.allow_voting = request.POST.get('allow_voting', 'True') == 'True'
    book.save(update_fields=['title', 'author', 'description', 'cover_url', 'amazon_url',
                             'pdf_url', 'external_video_url', 'status', 'visibility', 'allow_voting'])
    messages.success(request, 'Libro actualizado.')
    return redirect('/dashboard/?seccion=libros')


@login_required
def delete_book(request, book_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Libro eliminado.')
    return redirect('/dashboard/?seccion=libros')


@login_required
def create_event(request):
    if not request.user.is_admin_like() or not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Solo admins aprobados.')
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, 'Evento creado.')
    else:
        messages.error(request, f'Error: {form.errors}')
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
        messages.error(request, f'Error: {form.errors}')
    return redirect('/dashboard/?seccion=eventos')


@login_required
def delete_event(request, event_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Evento eliminado.')
    return redirect('/dashboard/?seccion=eventos')


@login_required
def vote_book(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobacion para votar.')
    book = get_object_or_404(Book, pk=book_id, status=BookStatus.FUTURE, allow_voting=True)
    vote, created = Vote.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f'Voto registrado por "{book.title}".')
    else:
        messages.info(request, f'Ya habias votado por "{book.title}".')
    return redirect(request.POST.get('next') or f'/libros/{book.id}/')


@login_required
def add_review(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobacion.')
    book = get_object_or_404(Book, pk=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.is_approved = False
        review.save()
        messages.success(request, 'Resena enviada a moderacion.')
    return redirect(request.POST.get('next') or 'home')


@login_required
def approve_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.is_approved = True
    review.is_flagged = False
    review.moderation_note = request.POST.get('moderation_note', '').strip()
    review.save(update_fields=['is_approved', 'is_flagged', 'moderation_note'])
    messages.success(request, 'Resena aprobada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def flag_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.is_approved = False
    review.is_flagged = True
    review.moderation_note = request.POST.get('moderation_note', '').strip() or 'Marcada'
    review.save(update_fields=['is_approved', 'is_flagged', 'moderation_note'])
    messages.success(request, 'Resena marcada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def delete_review(request, review_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Resena eliminada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def pending_users(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    users = User.objects.filter(is_approved=False)
    return render(request, 'pending_users.html', {'users': users})


@login_required
def approve_user(request, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    user = get_object_or_404(User, pk=user_id)
    user.is_approved = True
    user.save(update_fields=['is_approved'])
    cfg = ClubSettings.get_solo()
    if user.email:
        body = cfg.get_approved_template().format(
            nombre=user.username, club=cfg.name, url=cfg.public_url, usuario=user.username,
        )
        _send_email(subject=f'Tu cuenta en {cfg.name} fue aprobada', body=body, to=user.email, cfg=cfg)
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
        return HttpResponseForbidden('Metodo no permitido.')
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
            'email': email, 'full_name': name, 'role': role, 'is_approved': True,
        })
        if created:
            user.set_password(password)
            user.save()
        Invitation.objects.create(
            invited_name=name, email=email,
            generated_password=password, invited_by=request.user,
        )
        cfg = ClubSettings.get_solo()
        body = cfg.get_invitation_template().format(
            nombre=name, club=cfg.name, url=cfg.public_url,
            usuario=username, contrasena=password,
        )
        _send_email(subject=f'Invitacion a {cfg.name}', body=body, to=email, cfg=cfg)
        messages.success(request, f'Invitacion creada. Contrasena temporal: {password}')
    return redirect('/dashboard/?seccion=usuarios')


@login_required
def test_smtp(request):
    if not (request.user.role == Role.SUPERADMIN or request.user.is_superuser):
        return HttpResponseForbidden('Solo superadmin.')
    cfg = ClubSettings.get_solo()
    if not cfg.smtp_configured:
        messages.error(request, 'Configura SMTP antes de probarlo.')
        return redirect('/dashboard/?seccion=integraciones')
    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=cfg.smtp_host, port=cfg.smtp_port,
            username=cfg.smtp_user, password=cfg.smtp_password,
            use_tls=cfg.smtp_use_tls, fail_silently=False,
        )
        send_mail(
            subject=f'Prueba de correo - {cfg.name}',
            message=f'Correo de prueba desde {cfg.name}.',
            from_email=cfg.email_from or cfg.smtp_user,
            recipient_list=[request.user.email],
            connection=connection,
        )
        messages.success(request, f'Correo de prueba enviado a {request.user.email}.')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('/dashboard/?seccion=integraciones')


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
    return redirect('/dashboard/?seccion=inicio')


@login_required
def delete_social_link(request, link_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Metodo no permitido.')
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    link = get_object_or_404(SocialLink, pk=link_id)
    link.delete()
    messages.success(request, 'Red social eliminada.')
    return redirect('/dashboard/?seccion=inicio')


@login_required
def edit_profile(request):
    form = UserProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Perfil actualizado.')
    else:
        messages.error(request, f'Error: {form.errors}')
    return redirect('/dashboard/?seccion=perfil')


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