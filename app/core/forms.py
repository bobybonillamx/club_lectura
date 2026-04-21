from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Event, Review, ClubSettings, SocialLink, THEME_CHOICES


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=180)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password1', 'password2')


class BookForm(forms.ModelForm):
    reemplazar_leyendo_actual = forms.BooleanField(required=False)

    class Meta:
        model = Book
        fields = ['title', 'author', 'status', 'visibility', 'allow_voting',
                  'description', 'amazon_url', 'cover_url', 'external_video_url', 'pdf_url']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'starts_at', 'visibility', 'location', 'external_video_url']
        widgets = {'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ClubSettingsForm(forms.ModelForm):
    primary_color = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'color'}))
    accent_color = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = ClubSettings
        fields = [
            'name', 'description', 'logo_url', 'icon_url', 'cover_image_url',
            'theme', 'primary_color', 'accent_color',
            'public_domain', 'affiliate_tag',
            'google_login_enabled', 'google_client_id', 'google_client_secret',
            'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_use_tls', 'email_from',
            'email_tpl_welcome', 'email_tpl_approved', 'email_tpl_invitation',
            'meta_description', 'home_welcome_text', 'cta_register_text', 'cta_login_text',
            'footer_powered_by_name', 'footer_powered_by_url',
            'footer_custom_link_text', 'footer_custom_link_url', 'footer_text',
        ]

    def clean_primary_color(self):
        return self.cleaned_data.get('primary_color', '').strip()

    def clean_accent_color(self):
        return self.cleaned_data.get('accent_color', '').strip()


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['network', 'url']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar_url', 'bio', 'favorite_book', 'email']