from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Event, Vote, Review, Invitation, ClubSettings, SocialLink


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Club Lectura', {'fields': ('full_name', 'role', 'is_approved')}),
    )
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')


admin.site.register(Book)
admin.site.register(Event)
admin.site.register(Vote)
admin.site.register(Review)
admin.site.register(Invitation)
@admin.register(ClubSettings)
class ClubSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ('affiliate_tag',)

admin.site.register(SocialLink)
