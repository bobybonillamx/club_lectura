from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Event, Review, ClubSettings, SocialLink


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=180)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password1', 'password2')


class BookForm(forms.ModelForm):
    reemplazar_leyendo_actual = forms.BooleanField(
        required=False,
        help_text='Mover libros actuales "Leyendo" a "Leido".'
    )

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'status', 'visibility', 'allow_voting',
            'description', 'amazon_url', 'cover_url', 'external_video_url', 'pdf_url',
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'starts_at', 'visibility', 'location', 'external_video_url']
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ClubSettingsForm(forms.ModelForm):
    class Meta:
        model = ClubSettings
        fields = [
            'name', 'description', 'logo_url', 'icon_url',
            'primary_color', 'accent_color', 'affiliate_tag',
            'google_login_enabled', 'google_client_id', 'google_client_secret',
        ]
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
        }


class ReviewModerationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['is_approved', 'is_flagged', 'moderation_note']


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['network', 'url']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar_url', 'bio', 'favorite_book', 'email']