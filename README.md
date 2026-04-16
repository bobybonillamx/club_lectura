# Club de Lectura

Plataforma web para crear y administrar clubes de lectura con roles, aprobación de usuarios, votaciones, eventos, reseñas moderadas, OAuth con Google, PWA y despliegue Docker.

## Funcionalidades incluidas

- Gestión de libros: leídos, leyendo, por leer.
- Votación para elegir próximos libros.
- Registro/login tradicional + login con Google (django-allauth, opcional y activable por superadmin).
- Roles: `superadmin`, `admin`, `user`.
- Aprobación manual de usuarios por admins.
- Invitación de usuarios con contraseña temporal autogenerada.
- Eventos flexibles (sesión, intercambio, visita, restaurante, cine, etc.).
- Visibilidad por contenido: público, privado, solo admins.
- Reseñas con moderación (aprobar/marcar).
- Personalización visual completa desde dashboard:
  - Nombre del club
  - Descripción
  - Logo
  - Color principal y color acento
  - Tag de afiliado Amazon (si está vacío se usa automáticamente el tag base del sistema)
- Enlaces de compra en Amazon con tag de afiliado aplicado automáticamente.
- Búsqueda enriquecida de metadatos de libros:
  - Google Books
  - OpenLibrary
- Footer persistente:
  - Powered By: Gold Tech Mx
  - Repositorio oficial de GitHub
- PWA básica (instalable en Android/iOS con “Agregar a pantalla de inicio”).

---

## Requisitos

- Docker + Docker Compose
- (Opcional) Python 3.12 para correr sin Docker
- Cuenta de Google Cloud para OAuth

---

## Instalación en VPS (recomendada con Docker)

### 1) Clonar o actualizar repositorio

```bash
git clone https://github.com/bobybonillamx/club_lectura.git
cd club_lectura
```

Si ya existe en tu servidor:

```bash
cd club_lectura
git pull
```

### 2) Crear archivo de variables

```bash
cp .env.example .env
```

Edita `.env` según tu servidor. Variables principales:

- `APP_PORT` puerto público del sitio (default recomendado: `8787`)
- `PUBLIC_BASE_URL` URL pública real (ejemplo: `https://club.midominio.com`)
- `DJANGO_SECRET_KEY` secreto de producción
- `POSTGRES_*` credenciales de base de datos
- `POSTGRES_PORT`: puerto interno y externo de Postgres (debe ser el mismo en `db` y `web`).

### 3) Levantar servicios

```bash
docker compose --env-file .env up -d --build
```

### 4) Ejecutar migraciones y super admin inicial

```bash
docker compose --env-file .env exec web python manage.py migrate
docker compose --env-file .env exec web python manage.py createsuperuser
```

### 5) Activar OAuth Google desde el dashboard (sin .env)

- Inicia sesión como **superadmin**
- Ve a `Dashboard`
- En “Personalización visual y branding” captura:
  - `google_login_enabled`
  - `google_client_id`
  - `google_client_secret`
- Guarda cambios

### 6) Abrir la app

- URL local por defecto: `http://localhost:8787`
- URL real: la que definiste en `PUBLIC_BASE_URL`

---

## Configuración OAuth Google (Cloud Console)

1. Entra a https://console.cloud.google.com/
2. Crea proyecto o selecciona uno existente.
3. Configura **OAuth consent screen**.
4. Crea credencial **OAuth Client ID** tipo **Web application**.
5. Agrega redirect URI:
   - `https://TU_DOMINIO/accounts/google/login/callback/`
   - En local: `http://localhost:8787/accounts/google/login/callback/`
6. Captura `Client ID` y `Client Secret` en el Dashboard como superadmin.
7. Guarda cambios y prueba el botón de Google en `/login/`.

---

## Despliegue y mantenimiento

Actualizar en VPS:

```bash
git pull
docker compose --env-file .env up -d --build
docker compose --env-file .env exec web python manage.py migrate
```

Ver logs:

```bash
docker compose logs -f web
```

Respaldar base de datos (ejemplo rápido):

```bash
docker compose exec db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > backup.sql
```

---

## Seguridad mínima recomendada

- Ejecutar con `DEBUG=false`
- Usar HTTPS con proxy reverso (Nginx/Caddy/Traefik)
- Definir `ALLOWED_HOSTS` real
- Rotar `DJANGO_SECRET_KEY` en producción
- Respaldos automáticos de PostgreSQL
