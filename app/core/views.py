import secrets
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.db.utils import DatabaseError, OperationalError
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


def _is_effectively_approved(user):
    return bool(user.is_authenticated and (user.is_superuser or user.is_approved))


def _visible_filter(user):
    if user.is_authenticated and (user.role == Role.SUPERADMIN or user.is_superuser):
        return [v for v in Visibility.values]
    if user.is_authenticated and user.role == Role.ADMIN:
        return [Visibility.PUBLIC, Visibility.ADMINS]
    return [Visibility.PUBLIC]


def home(request):
    visible = _visible_filter(request.user)
    books = Book.objects.none()
    current_book = None
    next_event = None
    events = Event.objects.none()
    links = SocialLink.objects.none()

    try:
        books = Book.objects.filter(visibility__in=visible).order_by('-created_at')[:30]
        current_book = Book.objects.filter(visibility__in=visible, status=BookStatus.READING).order_by('-created_at').first()
        next_event = Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now()).order_by('starts_at').first()
        events = Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now()).order_by('starts_at')[:20]
        links = SocialLink.objects.all()
    except (DatabaseError, OperationalError):
        messages.warning(
            request,
            'No se pudieron cargar todos los datos de inicio. Verifica migraciones pendientes.',
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
    qs = Book.objects.filter(visibility__in=visible).order_by('-created_at')
    if status in {BookStatus.COMPLETED, BookStatus.READING, BookStatus.FUTURE}:
        qs = qs.filter(status=status)
    return render(request, 'books_page.html', {'books': qs, 'estado': status})


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
            messages.success(request, 'Tu cuenta fue creada. Un admin debe aprobarte para entrar al dashboard.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def dashboard(request):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Pendiente de aprobación por un admin.')

    section = request.GET.get('seccion', 'inicio')
    club_settings = ClubSettings.get_solo()
    settings_form = ClubSettingsForm(instance=club_settings)
    if request.user.role != Role.SUPERADMIN and not request.user.is_superuser:
        settings_form.fields.pop('google_login_enabled', None)
        settings_form.fields.pop('google_client_id', None)
        settings_form.fields.pop('google_client_secret', None)

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
    }
    return render(request, 'dashboard.html', context)


@login_required
def update_club_settings(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')

    club_settings = ClubSettings.get_solo()
    form = ClubSettingsForm(request.POST, instance=club_settings)
    if request.user.role != Role.SUPERADMIN and not request.user.is_superuser:
        form.fields.pop('google_login_enabled', None)
        form.fields.pop('google_client_id', None)
        form.fields.pop('google_client_secret', None)
    if form.is_valid():
        form.save()
        if request.user.role == Role.SUPERADMIN or request.user.is_superuser:
            sync_google_social_app_from_settings()
        messages.success(request, 'Configuración del club actualizada.')
    else:
        messages.error(request, f'Error de configuración: {form.errors}')
    section = request.POST.get('seccion', 'inicio')
    return redirect(f'/dashboard/?seccion={section}')


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
        messages.success(request, 'Libro guardado correctamente.')
    else:
        messages.error(request, f'Error al guardar libro: {form.errors}')
    return redirect('/dashboard/?seccion=libros')


@login_required
def edit_book(request, book_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    book = get_object_or_404(Book, pk=book_id)
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
        updated = form.save()
        if updated.status == BookStatus.READING and form.cleaned_data.get('reemplazar_leyendo_actual'):
            Book.objects.filter(status=BookStatus.READING).exclude(id=updated.id).update(status=BookStatus.COMPLETED)
        messages.success(request, 'Libro actualizado.')
    else:
        messages.error(request, f'No se pudo actualizar: {form.errors}')
    return redirect('/dashboard/?seccion=libros')


@login_required
def delete_book(request, book_id):
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
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Evento eliminado.')
    return redirect('/dashboard/?seccion=eventos')


@login_required
def vote_book(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobación.')
    book = get_object_or_404(Book, pk=book_id, status=BookStatus.FUTURE, allow_voting=True)
    vote, created = Vote.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f'Tu voto por "{book.title}" quedó registrado. Puedes votar por otros libros también.')
    else:
        messages.info(request, f'Ya habías votado por "{book.title}". Tu voto sigue contando.')
    return redirect(request.POST.get('next') or f'/libros/{book.id}/')


@login_required
def add_review(request, book_id):
    if not _is_effectively_approved(request.user):
        return HttpResponseForbidden('Necesitas aprobación.')
    book = get_object_or_404(Book, pk=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.is_approved = False
        review.save()
        messages.success(request, 'Reseña enviada a moderación.')
    return redirect('home')


@login_required
def review_moderation(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')

    reviews = Review.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'review_moderation.html', {'reviews': reviews})


@login_required
def approve_review(request, review_id):
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
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.is_approved = False
    review.is_flagged = True
    review.moderation_note = request.POST.get('moderation_note', '').strip() or 'Marcada por moderación'
    review.save(update_fields=['is_approved', 'is_flagged', 'moderation_note'])
    messages.success(request, 'Reseña marcada para seguimiento.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def delete_review(request, review_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Reseña eliminada.')
    return redirect('/dashboard/?seccion=resenas')


@login_required
def pending_users(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    users = User.objects.filter(is_approved=False)
    return render(request, 'pending_users.html', {'users': users})


@login_required
def approve_user(request, user_id):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    user = get_object_or_404(User, pk=user_id)
    user.is_approved = True
    user.save(update_fields=['is_approved'])
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
            return HttpResponseForbidden('Solo el super admin puede crear admins.')

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
        invite_link = f"{settings.PUBLIC_BASE_URL}/login/"
        messages.success(request, f'Invitación creada para {email}. Password temporal: {password}. Link: {invite_link}')
    return redirect('/dashboard/?seccion=usuarios')


@login_required
def add_social_link(request):
    if not request.user.is_admin_like():
        return HttpResponseForbidden('Solo admins.')
    form = SocialLinkForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Red social agregada.')
    else:
        messages.error(request, f'Error en red social: {form.errors}')
    return redirect('/dashboard/?seccion=integraciones')


@login_required
def delete_social_link(request, link_id):
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


def manifest(_request):
    return HttpResponse(
        '{"name":"Club de Lectura","short_name":"Lectura","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#6f42c1","icons":[]}',
        content_type='application/manifest+json',
    )


def service_worker(_request):
    js = "self.addEventListener('fetch', () => {});"
    return HttpResponse(js, content_type='application/javascript')
