# Club de Lectura

PWA para gestión de clubes de lectura. Desarrollado con Django 5, PostgreSQL y Docker.

---

## Características

- Biblioteca con votación, reseñas y categorías
- Vista galería/lista en libros y eventos (preferencia guardada por usuario)
- Eventos con foto, detalle y página de detalle al estilo de libros
- Sistema de temas visuales (6 predefinidos + colores personalizados)
- Tipografía personalizable con Google Fonts
- Toast notifications auto-descartables
- Notificaciones por correo (nuevo libro, evento, votación)
- Gestión de usuarios: registro, aprobación, invitación, suspensión, búsqueda en tiempo real
- Perfiles de miembro con redes sociales
- Lista de miembros del club (galería)
- Auto-fetch de metadatos de libros bajo demanda (Google Books + Open Library)
- Reordenamiento manual de libros
- Asignación de categorías en masa
- SEO configurable desde el panel
- Páginas de error personalizadas (404, 403, 500) con tema activo
- PWA instalable en móvil
- Integración con Amazon afiliados
- Google OAuth opcional
- Despliegue con Cloudflare Tunnel

---

## Requisitos

- Docker Desktop
- Git

---

## Instalación limpia

### 1. Clonar el repositorio

```bash
git clone https://github.com/bobybonillamx/club_lectura.git
cd club_lectura
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=cambia-esto-por-una-clave-segura
DEBUG=False
DB_NAME=clublectura
DB_USER=clublectura
DB_PASSWORD=cambia-esto
DB_HOST=db
DB_PORT=5432
PUBLIC_BASE_URL=https://tudominio.com
```

Para generar una `SECRET_KEY` segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Levantar los contenedores

```bash
docker compose up -d --build
```

### 4. Aplicar migraciones

```bash
docker compose exec web python manage.py migrate
```

### 5. Crear superadmin

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Acceder al sitio

- Sitio público: `http://localhost:8787`
- Panel de control: `http://localhost:8787/dashboard/`

---

## Estructura del proyecto

```
club_lectura/
├── app/
│   ├── clublectura/
│   │   ├── settings.py        # DEFAULT_AFFILIATE_TAG fijo aquí
│   │   └── urls.py
│   ├── core/
│   │   ├── models.py          # User, Book, Event, Category, UserSocialLink...
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── context_processors.py
│   │   ├── templatetags/
│   │   │   └── theme_tags.py  # Filtros: theme_page_color, social_icon, etc.
│   │   └── migrations/
│   └── templates/
│       ├── base.html          # ⚠️ Ver nota de |safe arriba
│       ├── home.html
│       ├── books_page.html
│       ├── book_detail.html
│       ├── events_page.html
│       ├── event_detail.html
│       ├── dashboard.html
│       ├── members_list.html
│       ├── member_profile.html
│       ├── 403.html / 404.html / 500.html
│       └── auth/
│           ├── login.html
│           └── register.html
├── docker-compose.yml
├── Dockerfile
└── .env
```

---

## Flujo de deploy tras cambios

```powershell
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate
```

---

## Configuración inicial del club

1. Entra a `/dashboard/` con el superadmin
2. **Inicio** — Nombre, descripción, logo, imagen hero
3. **SEO** — Meta descripción, palabras clave, autor
4. **Apariencia** — Elige tema y tipografía personalizada
5. **Integraciones** — SMTP, dominio público, tag Amazon del club, Google OAuth
6. **Correos** — Activa notificaciones automáticas y edita plantillas
7. **Mi perfil** — Foto, bio, redes sociales personales

---

## Temas disponibles

| Tema | Descripción |
|------|-------------|
| Literario Café | Tonos cálidos, tipografía serif clásica |
| Moderno Oscuro | Dark mode con acentos púrpura |
| Minimalista Blanco | Limpio y minimal |
| Verde Bosque | Tonos naturales verdes |
| Océano Profundo | Azules profundos |
| Rosa Editorial | Rosa elegante |

---

## Stack técnico

| Componente | Tecnología |
|-----------|-----------|
| Backend | Django 5.1.8 |
| Base de datos | PostgreSQL |
| Servidor WSGI | Gunicorn |
| Contenedores | Docker Compose |
| Frontend | HTML/CSS con variables CSS (sin Bootstrap) |
| PWA | Service Worker + Web Manifest |
| Fuentes | Google Fonts dinámico |
| Túnel | Cloudflare Tunnel |

---

## Licencia

Uso personal y comercial libre. Mantén el crédito "Powered by Gold Tech Mx" en el footer.
