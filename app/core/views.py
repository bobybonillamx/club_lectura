import secrets
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import RegisterForm, BookForm, EventForm, ReviewForm, ClubSettingsForm
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


def _visible_filter(user):
    if user.is_authenticated and user.role == Role.SUPERADMIN:
        return [v for v in Visibility.values]
    if user.is_authenticated and user.role == Role.ADMIN:
        return [Visibility.PUBLIC, Visibility.ADMINS]
    return [Visibility.PUBLIC]


def home(request):
    visible = _visible_filter(request.user)
    books = Book.objects.filter(visibility__in=visible).order_by('-created_at')[:30]
    events = Event.objects.filter(visibility__in=visible, starts_at__gte=timezone.now()).order_by('starts_at')[:20]
    links = SocialLink.objects.all()
    return render(request, 'home.html', {
        'books': books,
        'events': events,
        'links': links,
        'book_status': BookStatus,
    })


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
    if not request.user.is_approved:
        return HttpResponseForbidden('Pendiente de aprobación por un admin.')

    club_settings = ClubSettings.get_solo()
    if request.method == 'POST' and request.user.is_admin_like():
        settings_form = ClubSettingsForm(request.POST, instance=club_settings)
        if request.user.role != Role.SUPERADMIN:
            settings_form.fields.pop('google_login_enabled', None)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, 'Personalización actualizada.')
            return redirect('dashboard')
    else:
        settings_form = ClubSettingsForm(instance=club_settings)
        if request.user.role != Role.SUPERADMIN:
            settings_form.fields.pop('google_login_enabled', None)

    return render(request, 'dashboard.html', {
        'book_form': BookForm(),
        'event_form': EventForm(),
        'settings_form': settings_form,
        'pending_reviews_count': Review.objects.filter(is_approved=False).count(),
    })


@login_required
def create_book(request):
    if not request.user.is_admin_like() or not request.user.is_approved:
        return HttpResponseForbidden('Solo admins aprobados.')
    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        messages.success(request, 'Libro guardado correctamente.')
    else:
        messages.error(request, f'Error al guardar libro: {form.errors}')
    return redirect('dashboard')


@login_required
def create_event(request):
    if not request.user.is_admin_like() or not request.user.is_approved:
        return HttpResponseForbidden('Solo admins aprobados.')
    form = EventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, 'Evento creado correctamente.')
    else:
        messages.error(request, f'Error al crear evento: {form.errors}')
    return redirect('dashboard')


@login_required
def vote_book(request, book_id):
    if not request.user.is_approved:
        return HttpResponseForbidden('Necesitas aprobación.')
    book = get_object_or_404(Book, pk=book_id, status=BookStatus.FUTURE)
    Vote.objects.get_or_create(user=request.user, book=book)
    messages.success(request, 'Voto registrado.')
    return redirect('home')


@login_required
def add_review(request, book_id):
    if not request.user.is_approved:
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
    return redirect('review_moderation')


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
    return redirect('review_moderation')


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
    return redirect('pending_users')


@login_required
def invite_user(request):
    if request.user.role not in {Role.ADMIN, Role.SUPERADMIN}:
        return HttpResponseForbidden('Solo admins.')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        role = request.POST.get('role', Role.USER)
        if role == Role.ADMIN and request.user.role != Role.SUPERADMIN:
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
    return redirect('dashboard')


def manifest(_request):
    return HttpResponse(
        '{"name":"Club de Lectura","short_name":"Lectura","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#6f42c1","icons":[]}',
        content_type='application/manifest+json',
    )


def service_worker(_request):
    js = "self.addEventListener('fetch', () => {});"
    return HttpResponse(js, content_type='application/javascript')
