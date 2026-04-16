from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Event, Review, ClubSettings


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=180)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password1', 'password2')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'status',
            'visibility',
            'description',
            'amazon_url',
            'cover_url',
            'external_video_url',
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
        fields = ['name', 'description', 'logo_url', 'primary_color', 'accent_color', 'affiliate_tag', 'google_login_enabled', 'google_client_id', 'google_client_secret']


class ReviewModerationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['is_approved', 'is_flagged', 'moderation_note']
