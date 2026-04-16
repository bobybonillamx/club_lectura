from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('registro/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('libros/nuevo/', views.create_book, name='create_book'),
    path('libros/<int:book_id>/votar/', views.vote_book, name='vote_book'),
    path('libros/<int:book_id>/resena/', views.add_review, name='add_review'),
    path('eventos/nuevo/', views.create_event, name='create_event'),
    path('usuarios/pendientes/', views.pending_users, name='pending_users'),
    path('usuarios/<int:user_id>/aprobar/', views.approve_user, name='approve_user'),
    path('admin/invitar/', views.invite_user, name='invite_user'),
    path('resenas/moderacion/', views.review_moderation, name='review_moderation'),
    path('resenas/<int:review_id>/aprobar/', views.approve_review, name='approve_review'),
    path('resenas/<int:review_id>/marcar/', views.flag_review, name='flag_review'),
    path('pwa/manifest.json', views.manifest, name='manifest'),
    path('pwa/sw.js', views.service_worker, name='service_worker'),
]
