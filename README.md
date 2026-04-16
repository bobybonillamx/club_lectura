# Club de Lectura (MVP)

Mini sitio **dockerizable** para crear y publicar tu propio club de lectura, con roles, aprobación de usuarios, votaciones y eventos.

## Incluye en este MVP

- Libros por estado: leído, leyendo, por leer.
- Votaciones para libros futuros.
- Registro/login con aprobación por admin.
- Roles:
  - `superadmin`: puede crear admins.
  - `admin`: aprueba usuarios e invita usuarios.
  - `user`: participa y reseña.
- Eventos flexibles (sesión, intercambio, visita, restaurante, cine, etc.) con fecha/hora.
- Control de visibilidad en libros/eventos: público, privado, solo admins.
- Enlace Amazon automático con `tag` de afiliado fijo: `bobybonilla0b-20` (persistente, no configurable).
- Portada automática (si no se captura URL manual).
- URL base pública configurable (`PUBLIC_BASE_URL`) para invitaciones y compartir.
- Footer persistente: **Powered By: Gold Tech Mx**.
- Diseño responsive + soporte PWA básico (`manifest` + service worker).

## Stack

- Django 5
- PostgreSQL (con Docker) o SQLite (local rápido)
- Bootstrap 5

## Ejecución rápida local (SQLite)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Ejecución con Docker

```bash
docker compose up --build
```

Abre: http://localhost:8000

## Configuración clave

Variables importantes:

- `PUBLIC_BASE_URL`: URL pública de invitaciones/compartir.
- `DB_ENGINE=postgres|sqlite`
- `POSTGRES_*` si usas postgres.
- `DJANGO_SECRET_KEY`

## Flujo recomendado de roles

1. Crea un superusuario con `python manage.py createsuperuser`.
2. Entra a `/admin` y ajusta su rol a `superadmin`.
3. Superadmin crea/autoriza admins.
4. Admins autorizan usuarios y gestionan contenido.

## Google Login (paso a paso - guía)

> Este repo deja la base lista; para OAuth Google puedes usar `django-allauth`.

1. Crea proyecto en [Google Cloud Console](https://console.cloud.google.com/).
2. Ve a **APIs & Services → OAuth consent screen** y configura nombre/app.
3. Ve a **Credentials → Create Credentials → OAuth client ID**.
4. Tipo: **Web application**.
5. Authorized redirect URI (ejemplo local):
   - `http://localhost:8000/accounts/google/login/callback/`
6. Guarda `Client ID` y `Client Secret`.
7. Instala y configura `django-allauth` en `INSTALLED_APPS` y `urls.py`.
8. Define variables seguras para secrets en tu `.env`.
9. Reinicia y prueba login con Google.

## Seguridad recomendada para producción

- `DEBUG=false`
- `ALLOWED_HOSTS` correcto
- HTTPS con reverse proxy (Nginx/Caddy)
- Rotar `DJANGO_SECRET_KEY`
- Políticas de backup de base de datos

## Pendiente para siguiente iteración

- Integración real de OAuth Google en código.
- Personalización visual completa desde panel.
- Scraping/búsqueda enriquecida de Amazon y portadas (OpenLibrary/Google Books).
- Moderación avanzada de reseñas/actividad.
