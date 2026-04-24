# Club de Lectura

PWA para gestión de clubes de lectura. Desarrollado con Django 5, PostgreSQL y Docker.

**Desarrollado por [Gold Tech Mx](https://goldtech.mx)**

---

## Características

- Biblioteca con votación, reseñas y categorías
- Eventos con foto, detalle y vista galería/lista
- Sistema de temas visuales (6 predefinidos + colores personalizados)
- Tipografía personalizable con Google Fonts
- Notificaciones por correo (nuevo libro, evento, votación)
- Gestión de usuarios: registro, aprobación, invitación, suspensión
- Perfiles de miembro con redes sociales
- Auto-fetch de metadatos de libros (Google Books + Open Library)
- SEO configurable desde el panel
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
- Panel de admin: `http://localhost:8787/dashboard/`

---

## Estructura del proyecto

```
club_lectura/
├── app/
│   ├── clublectura/          # Configuración Django
│   │   ├── settings.py
│   │   └── urls.py
│   ├── core/                 # App principal
│   │   ├── models.py         # Modelos: User, Book, Event, Category...
│   │   ├── views.py          # Vistas
│   │   ├── forms.py          # Formularios
│   │   ├── context_processors.py
│   │   ├── templatetags/
│   │   │   └── theme_tags.py # Filtros para temas e iconos
│   │   └── migrations/
│   └── templates/            # Templates HTML
│       ├── base.html
│       ├── home.html
│       ├── books_page.html
│       ├── book_detail.html
│       ├── events_page.html
│       ├── event_detail.html
│       ├── dashboard.html
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

## Despliegue en producción

### Con Cloudflare Tunnel

1. Instala `cloudflared` en tu servidor
2. Crea un túnel apuntando a `http://localhost:8787`
3. En el panel del club → Integraciones → pon el dominio del túnel (sin `https://`)

### Variables adicionales para producción

```env
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

---

## Flujo de deploy tras cambios

```powershell
# En Windows
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate
```

---

## Configuración inicial del club

1. Entra a `/dashboard/` con el superadmin
2. **Inicio** — Nombre del club, descripción, logo, imagen hero
3. **SEO** — Meta descripción, palabras clave
4. **Apariencia** — Elige un tema y tipografía
5. **Integraciones** — Configura SMTP para correos, dominio público, tag de Amazon
6. **Correos** — Activa notificaciones automáticas

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

Uso personal y comercial libre. Mantén el crédito "Powered by Locos X la Tecnología" en el footer.
