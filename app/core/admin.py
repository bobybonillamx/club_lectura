from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Event, Vote, Review, Invitation, ClubSettings, SocialLink


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Club Lectura', {'fields': ('full_name', 'role', 'is_approved')}),
    )
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'is_approved', 'is_flagged', 'created_at')
    list_filter = ('is_approved', 'is_flagged')
    search_fields = ('book__title', 'user__username', 'comment')


@admin.register(ClubSettings)
class ClubSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'accent_color', 'affiliate_tag')


admin.site.register(Book)
admin.site.register(Event)
admin.site.register(Vote)
admin.site.register(Invitation)
admin.site.register(SocialLink)
