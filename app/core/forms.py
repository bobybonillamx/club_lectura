from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Event, Review, ClubSettings, SocialLink, Category, THEME_CHOICES, SOCIAL_ICON_CHOICES, FONT_PRESETS


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
                  'category', 'description', 'amazon_url', 'cover_url', 'external_video_url', 'pdf_url', 'reading_month']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'starts_at', 'visibility', 'location', 'external_video_url', 'cover_image_url']
        widgets = {'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ClubSettingsForm(forms.ModelForm):
    name = forms.CharField(required=False, initial='Mi Club de Lectura')
    theme = forms.ChoiceField(required=False, choices=THEME_CHOICES)
    primary_color = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'color'}))
    accent_color = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'color'}))
    smtp_port = forms.IntegerField(required=False, initial=587)

    class Meta:
        model = ClubSettings
        fields = [
            'name', 'description', 'logo_url', 'icon_url', 'cover_image_url',
            'theme', 'primary_color', 'accent_color',
            'meta_description', 'meta_keywords', 'meta_author',
            'home_welcome_text', 'cta_register_text', 'cta_login_text',
            'font_preset', 'custom_font_url', 'custom_font_serif', 'custom_font_sans',
            'footer_text', 'footer_custom_link_text', 'footer_custom_link_url',
            'public_domain', 'affiliate_tag',
            'google_login_enabled', 'google_client_id', 'google_client_secret',
            'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_use_tls', 'email_from',
            'email_tpl_welcome', 'email_tpl_approved', 'email_tpl_invitation',
            'email_tpl_new_book', 'email_tpl_new_event', 'email_tpl_voting_open',
            'notify_new_book', 'notify_new_event', 'notify_voting_open', 'notify_pending_approvals',
        ]

    def clean_name(self):
        val = self.cleaned_data.get('name', '').strip()
        return val or (self.instance.name if self.instance.pk else 'Mi Club de Lectura')

    def clean_theme(self):
        val = self.cleaned_data.get('theme', '').strip()
        return val or (self.instance.theme if self.instance.pk else 'literario_cafe')

    def clean_smtp_port(self):
        val = self.cleaned_data.get('smtp_port')
        return val or (self.instance.smtp_port if self.instance.pk else 587)

    def clean_primary_color(self):
        return self.cleaned_data.get('primary_color', '').strip()

    def clean_accent_color(self):
        return self.cleaned_data.get('accent_color', '').strip()


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['network', 'url', 'icon']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar_url', 'bio', 'favorite_book', 'email']