"""
fix_templates.py
Escribe todos los templates del proyecto directamente al disco.
Correr desde dentro del contenedor:
    python fix_templates.py
"""
import os

BASE = "/app/app/templates"
os.makedirs(f"{BASE}/auth", exist_ok=True)

files = {}

# ─────────────────────────────────────────────
# base.html
# ─────────────────────────────────────────────
files[f"{BASE}/base.html"] = """
{% load static %}
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="{{ club_settings.primary_color }}" />
  <link rel="manifest" href="/pwa/manifest.json" />
  <link rel="icon" type="image/svg+xml" href="{% static 'favicon.svg' %}" />
  <title>{{ club_settings.name }}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    :root {
      --club-primary: {{ club_settings.primary_color }};
      --club-accent:  {{ club_settings.accent_color|default:'#5C3D2E' }};
      --ink:          #2C1A0E;
      --ink-light:    #6B4F3A;
      --parchment:    #FAF6F0;
      --parchment-2:  #F2EBE0;
      --parchment-3:  #E8DDD0;
      --warm-border:  #D9CEBC;
      --serif: 'Lora', Georgia, serif;
      --sans:  'Inter', system-ui, sans-serif;
    }
    * { box-sizing: border-box; }
    body { font-family: var(--sans); font-size: 15px; background-color: var(--parchment); color: var(--ink); min-height: 100vh; }
    h1, h2, h3, h4 { font-family: var(--serif); color: var(--ink); }
    .site-nav { background: var(--parchment); border-bottom: 1px solid var(--warm-border); padding: 0.75rem 0; }
    .site-nav .brand { font-family: var(--serif); font-size: 1.2rem; font-weight: 600; color: var(--ink) !important; text-decoration: none; }
    .site-nav .nav-link { font-size: 0.875rem; color: var(--ink-light); text-decoration: none; padding: 0.35rem 0.75rem; border-radius: 6px; transition: background 0.15s; }
    .site-nav .nav-link:hover { background: var(--parchment-2); color: var(--ink); }
    .btn-primary-warm { background: var(--club-primary); color: #fff; border: none; border-radius: 8px; padding: 0.45rem 1.1rem; font-size: 0.875rem; cursor: pointer; transition: opacity 0.15s; display: inline-block; text-decoration: none; }
    .btn-primary-warm:hover { opacity: 0.88; color: #fff; }
    .btn-outline-warm { background: transparent; color: var(--ink-light); border: 1px solid var(--warm-border); border-radius: 8px; padding: 0.4rem 1rem; font-size: 0.875rem; cursor: pointer; text-decoration: none; display: inline-block; transition: background 0.15s; }
    .btn-outline-warm:hover { background: var(--parchment-2); color: var(--ink); }
    .btn-danger-warm { background: #9B2626; color: #fff; border: none; border-radius: 8px; padding: 0.4rem 1rem; font-size: 0.875rem; cursor: pointer; text-decoration: none; display: inline-block; }
    .btn-danger-warm:hover { opacity: 0.88; color: #fff; }
    .card-warm { background: #fff; border: 1px solid var(--warm-border); border-radius: 12px; overflow: hidden; }
    .card-warm-body { padding: 1.25rem 1.5rem; }
    .form-control, .form-select { background: #fff; border: 1px solid var(--warm-border); border-radius: 8px; color: var(--ink); font-size: 0.875rem; }
    .form-control:focus, .form-select:focus { border-color: var(--club-primary); box-shadow: none; }
    .form-label { font-size: 0.8125rem; font-weight: 500; color: var(--ink-light); margin-bottom: 0.3rem; }
    .alert-warm { background: #FFF8F0; border: 1px solid #F0D9B5; border-radius: 10px; color: var(--ink); padding: 0.75rem 1rem; font-size: 0.875rem; }
    .badge-warm { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; background: var(--parchment-2); color: var(--ink-light); border: 1px solid var(--warm-border); }
    .badge-warm.reading   { background: #EDF6EC; color: #2D6A2D; border-color: #BAD9B5; }
    .badge-warm.completed { background: #EDF0F6; color: #2D3A6A; border-color: #B5BCDA; }
    .badge-warm.future    { background: #FEF6E7; color: #7A4F0D; border-color: #F0D295; }
    .divider { border: none; border-top: 1px solid var(--warm-border); margin: 1.5rem 0; }
    .section-label { font-family: var(--sans); font-size: 0.7rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 0.75rem; }
    .side-nav a { display: block; padding: 0.5rem 0.85rem; border-radius: 8px; font-size: 0.875rem; color: var(--ink-light); text-decoration: none; margin-bottom: 2px; transition: background 0.12s; }
    .side-nav a:hover { background: var(--parchment-2); color: var(--ink); }
    .side-nav a.active { background: var(--parchment-3); color: var(--ink); font-weight: 500; }
    .stars { color: #C0833A; }
  </style>
</head>
<body>
<nav class="site-nav">
  <div class="container d-flex align-items-center gap-3">
    <a class="brand" href="/">
      {% if club_settings.logo_url %}
        <img src="{{ club_settings.logo_url }}" alt="{{ club_settings.name }}" style="height:32px;width:auto;object-fit:contain;">
      {% else %}
        {{ club_settings.name }}
      {% endif %}
    </a>
    <div class="d-none d-md-flex gap-1 ms-1">
      <a class="nav-link" href="/libros/">Libros</a>
      <a class="nav-link" href="/eventos/">Eventos</a>
    </div>
    <div class="ms-auto d-flex align-items-center gap-2">
      {% if user.is_authenticated %}
        <a class="btn-outline-warm" href="/dashboard/">Panel</a>
        <form action="/logout/" method="post" style="margin:0">{% csrf_token %}
          <button class="btn-danger-warm">Salir</button>
        </form>
      {% else %}
        <a class="btn-outline-warm" href="/login/">Entrar</a>
        <a class="btn-primary-warm" href="/registro/">Registro</a>
      {% endif %}
    </div>
  </div>
</nav>
<main class="container py-4">
  {% if messages %}
    {% for message in messages %}
      <div class="alert-warm mb-3">{{ message }}</div>
    {% endfor %}
  {% endif %}
  {% block content %}{% endblock %}
</main>
<footer style="border-top:1px solid var(--warm-border);padding:1.5rem 0;text-align:center;font-size:0.8125rem;color:var(--ink-light);background:var(--parchment);">
  Powered by <a href="https://goldtech.mx" target="_blank" rel="noopener" style="color:var(--ink-light);">Gold Tech Mx</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/bobybonillamx/club_lectura" target="_blank" rel="noopener" style="color:var(--ink-light);">Repositorio en GitHub</a>
</footer>
<script>if ('serviceWorker' in navigator) navigator.serviceWorker.register('/pwa/sw.js');</script>
</body>
</html>
""".strip()

# ─────────────────────────────────────────────
# home.html
# ─────────────────────────────────────────────
files[f"{BASE}/home.html"] = """
{% extends 'base.html' %}
{% block content %}
<section style="padding:2.5rem 0 1.5rem;">
  <p class="section-label">Bienvenido</p>
  <h1 style="font-size:2rem;margin-bottom:0.5rem;">{{ club_settings.name }}</h1>
  {% if club_settings.description %}
    <p style="color:var(--ink-light);max-width:520px;margin-bottom:1.5rem;">{{ club_settings.description }}</p>
  {% endif %}
  <div class="row g-3" style="max-width:640px;">
    <div class="col-sm-6">
      <div class="card-warm card-warm-body" style="height:100%;">
        <p class="section-label mb-1">Leyendo ahora</p>
        {% if current_book %}
          <strong style="font-family:var(--serif);">{{ current_book.title }}</strong>
          <div style="font-size:0.8125rem;color:var(--ink-light);margin-top:2px;">{{ current_book.author }}</div>
        {% else %}
          <span style="color:var(--ink-light);font-size:0.875rem;">Sin libro activo</span>
        {% endif %}
      </div>
    </div>
    <div class="col-sm-6">
      <div class="card-warm card-warm-body" style="height:100%;">
        <p class="section-label mb-1">Proximo evento</p>
        {% if next_event %}
          <strong style="font-family:var(--serif);">{{ next_event.title }}</strong>
          <div style="font-size:0.8125rem;color:var(--ink-light);margin-top:2px;">{{ next_event.starts_at|date:"j M, H:i" }}</div>
        {% else %}
          <span style="color:var(--ink-light);font-size:0.875rem;">Sin eventos proximos</span>
        {% endif %}
      </div>
    </div>
  </div>
</section>
<hr class="divider">
<div class="row g-4">
  <div class="col-lg-8">
    <p class="section-label">Biblioteca del club</p>
    {% for book in books %}
    <div class="card-warm mb-3" style="display:flex;">
      <div style="flex-shrink:0;width:80px;background:var(--parchment-2);">
        {% if book.cover_url %}
          <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:80px;height:120px;object-fit:cover;border-radius:12px 0 0 12px;">
        {% else %}
          <div style="width:80px;height:120px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">📖</div>
        {% endif %}
      </div>
      <div class="card-warm-body" style="flex:1;padding:1rem 1.25rem;">
        <div class="d-flex justify-content-between align-items-start gap-2">
          <div>
            <h3 style="font-size:1rem;margin-bottom:2px;">{{ book.title }}</h3>
            <div style="font-size:0.8125rem;color:var(--ink-light);">{{ book.author }}</div>
          </div>
          <span class="badge-warm {% if book.status == 'reading' %}reading{% elif book.status == 'completed' %}completed{% else %}future{% endif %}" style="white-space:nowrap;flex-shrink:0;">{{ book.get_status_display }}</span>
        </div>
        {% if book.status == 'future' and book.allow_voting %}
          <div style="margin-top:0.5rem;font-size:0.8125rem;color:#7A4F0D;background:#FEF6E7;padding:0.35rem 0.6rem;border-radius:6px;display:inline-block;">
            Votacion abierta · {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}
          </div>
        {% endif %}
        <div class="d-flex flex-wrap gap-2 mt-3 align-items-center">
          <a class="btn-outline-warm" href="/libros/{{ book.id }}/" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Ver detalle</a>
          {% if book.amazon_url %}<a href="{{ book.amazon_url }}" target="_blank" rel="noopener" style="font-size:0.8125rem;color:var(--ink-light);">Amazon</a>{% endif %}
          {% if book.pdf_url %}<a href="{{ book.pdf_url }}" target="_blank" style="font-size:0.8125rem;color:var(--ink-light);">PDF</a>{% endif %}
        </div>
        {% with approved=book.reviews.all %}
          {% if approved %}
          <div style="margin-top:0.75rem;border-top:1px solid var(--parchment-3);padding-top:0.75rem;">
            {% for review in approved %}{% if review.is_approved %}
            <div style="font-size:0.8125rem;color:var(--ink-light);">
              <span class="stars">{% for i in "12345" %}{% if forloop.counter <= review.rating %}★{% else %}☆{% endif %}{% endfor %}</span>
              <strong style="color:var(--ink);">{{ review.user.username }}</strong> — {{ review.comment|truncatechars:100 }}
            </div>
            {% endif %}{% endfor %}
          </div>
          {% endif %}
        {% endwith %}
      </div>
    </div>
    {% empty %}<p style="color:var(--ink-light);">Aun no hay libros registrados.</p>{% endfor %}
  </div>
  <div class="col-lg-4">
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Proximos eventos</p>
      {% for event in events %}
        <div style="padding:0.75rem 0;{% if not forloop.last %}border-bottom:1px solid var(--parchment-3);{% endif %}">
          <strong style="font-family:var(--serif);font-size:0.9375rem;">{{ event.title }}</strong>
          <div style="font-size:0.8125rem;color:var(--ink-light);margin-top:2px;">{{ event.event_type }} · {{ event.starts_at|date:"j M" }}</div>
          {% if event.location %}<div style="font-size:0.8rem;color:var(--ink-light);">{{ event.location }}</div>{% endif %}
        </div>
      {% empty %}<p style="color:var(--ink-light);font-size:0.875rem;margin:0;">Sin eventos proximos.</p>{% endfor %}
    </div>
    {% if links %}
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Redes del club</p>
      {% for link in links %}
        <a href="{{ link.url }}" target="_blank" rel="noopener" style="display:block;font-size:0.875rem;color:var(--ink-light);padding:0.25rem 0;text-decoration:none;">{{ link.network }}</a>
      {% endfor %}
    </div>
    {% endif %}
    <button class="btn-outline-warm w-100" onclick="navigator.share ? navigator.share({title:document.title,url:location.href}) : alert('Comparte: '+location.href)">Compartir club</button>
  </div>
</div>
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# books_page.html
# ─────────────────────────────────────────────
files[f"{BASE}/books_page.html"] = """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-end mb-3 flex-wrap gap-2">
  <div>
    <p class="section-label mb-0">Biblioteca</p>
    <h1 style="font-size:1.75rem;margin:0;">Libros del club</h1>
  </div>
</div>
<form method="get" action="/libros/" class="d-flex gap-2 flex-wrap mb-4">
  <input type="text" name="q" value="{{ query|default:'' }}" class="form-control" placeholder="Buscar por titulo o autor..." style="max-width:320px;">
  <select name="estado" class="form-select" style="max-width:180px;" onchange="this.form.submit()">
    <option value="">Todos los estados</option>
    <option value="completed" {% if estado == 'completed' %}selected{% endif %}>Leidos</option>
    <option value="reading"   {% if estado == 'reading'   %}selected{% endif %}>Leyendo</option>
    <option value="future"    {% if estado == 'future'    %}selected{% endif %}>En votacion</option>
  </select>
  <button class="btn-primary-warm" type="submit">Buscar</button>
  {% if query or estado %}<a class="btn-outline-warm" href="/libros/">Limpiar</a>{% endif %}
</form>
{% for book in books %}
  <a href="/libros/{{ book.id }}/" style="text-decoration:none;display:block;">
    <div class="card-warm mb-2" style="{% if book.status == 'future' and book.allow_voting %}border-color:#C0833A;{% endif %}">
      {% if book.status == 'future' and book.allow_voting %}
      <div style="background:#FEF6E7;border-bottom:1px solid #F0D295;padding:0.4rem 1.25rem;font-size:0.75rem;color:#7A4F0D;">
        Votacion abierta &mdash; {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }} &middot; Haz clic para votar
      </div>
      {% endif %}
      <div class="card-warm-body d-flex justify-content-between align-items-center gap-3">
        <div style="display:flex;align-items:center;gap:0.875rem;">
          {% if book.cover_url %}
            <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:40px;height:60px;object-fit:cover;border-radius:4px;flex-shrink:0;">
          {% else %}
            <div style="width:40px;height:60px;background:var(--parchment-2);border-radius:4px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">📖</div>
          {% endif %}
          <div>
            <strong style="font-family:var(--serif);color:var(--ink);font-size:0.9375rem;">{{ book.title }}</strong>
            <div style="font-size:0.8125rem;color:var(--ink-light);">{{ book.author }}</div>
          </div>
        </div>
        <span class="badge-warm {% if book.status == 'reading' %}reading{% elif book.status == 'completed' %}completed{% else %}future{% endif %}" style="white-space:nowrap;">{{ book.get_status_display }}</span>
      </div>
    </div>
  </a>
{% empty %}
  <p style="color:var(--ink-light);padding:2rem 0;">No se encontraron libros con estos filtros.</p>
{% endfor %}
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# book_detail.html
# ─────────────────────────────────────────────
files[f"{BASE}/book_detail.html"] = """
{% extends 'base.html' %}
{% block content %}
<a href="/libros/" class="btn-outline-warm mb-4" style="display:inline-block;">Volver</a>
<div class="row g-4">
  <div class="col-md-3">
    {% if book.cover_url %}
      <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:100%;max-width:220px;aspect-ratio:2/3;object-fit:cover;border-radius:10px;">
    {% else %}
      <div style="width:100%;max-width:220px;aspect-ratio:2/3;background:var(--parchment-2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:3rem;">📖</div>
    {% endif %}
  </div>
  <div class="col-md-9">
    <span class="badge-warm {% if book.status == 'reading' %}reading{% elif book.status == 'completed' %}completed{% else %}future{% endif %} mb-2">{{ book.get_status_display }}</span>
    <h1 style="font-size:1.75rem;margin-bottom:0.25rem;">{{ book.title }}</h1>
    {% if book.author %}<p style="font-size:1rem;color:var(--ink-light);margin-bottom:1rem;font-style:italic;">{{ book.author }}</p>{% endif %}
    {% if book.description %}<p style="line-height:1.75;color:var(--ink);max-width:600px;">{{ book.description }}</p>{% endif %}
    <div class="d-flex flex-wrap gap-2 mt-3">
      {% if book.amazon_url %}<a href="{{ book.amazon_url }}" class="btn-outline-warm" target="_blank" rel="noopener">Ver en Amazon</a>{% endif %}
      {% if book.external_video_url %}<a href="{{ book.external_video_url }}" class="btn-outline-warm" target="_blank" rel="noopener">Video</a>{% endif %}
      {% if book.pdf_url %}<a href="{{ book.pdf_url }}" class="btn-outline-warm" target="_blank" rel="noopener">Descargar PDF</a>{% endif %}
    </div>
    {% if book.status == 'future' and book.allow_voting %}
    <div class="card-warm card-warm-body mt-4" style="max-width:480px;border-color:#C0833A;background:#FEF6E7;">
      <p class="section-label" style="color:#7A4F0D;">Votacion abierta</p>
      <p style="font-family:var(--serif);font-size:1rem;color:var(--ink);margin-bottom:0.5rem;">Quieres leer este libro en el club?</p>
      <p style="font-size:0.875rem;color:var(--ink-light);margin-bottom:1rem;">Cada miembro aprobado puede votar por todos los libros que quiera. El libro con mas votos sera el proximo en leerse.</p>
      <div style="font-size:1.25rem;font-family:var(--serif);font-weight:600;color:#7A4F0D;margin-bottom:1rem;">{{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}</div>
      {% if user_vote %}
        <div style="color:#2D6A2D;font-size:0.9375rem;">Votaste por este libro</div>
      {% elif user.is_authenticated %}
        {% if user.is_approved or user.is_superuser %}
        <form action="/libros/{{ book.id }}/votar/" method="post">
          {% csrf_token %}
          <input type="hidden" name="next" value="/libros/{{ book.id }}/">
          <button class="btn-primary-warm" style="background:#C0833A;">Votar por este libro</button>
        </form>
        {% else %}
          <p style="font-size:0.8125rem;color:var(--ink-light);">Tu cuenta esta pendiente de aprobacion.</p>
        {% endif %}
      {% else %}
        <a href="/login/" class="btn-outline-warm">Inicia sesion para votar</a>
      {% endif %}
    </div>
    {% endif %}
  </div>
</div>
<hr class="divider">
<div class="row g-4">
  <div class="col-lg-7">
    <p class="section-label">Resenas</p>
    {% for review in approved_reviews %}
      <div class="card-warm card-warm-body mb-3">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <strong style="font-size:0.9375rem;">{{ review.user.username }}</strong>
          <span class="stars">{% for i in "12345" %}{% if forloop.counter <= review.rating %}★{% else %}☆{% endif %}{% endfor %}</span>
        </div>
        <p style="margin:0;font-size:0.9375rem;line-height:1.6;">{{ review.comment }}</p>
        <div style="font-size:0.75rem;color:var(--ink-light);margin-top:0.5rem;">{{ review.created_at|date:"j M Y" }}</div>
      </div>
    {% empty %}
      <p style="color:var(--ink-light);">Aun no hay resenas aprobadas.</p>
    {% endfor %}
  </div>
  {% if user.is_authenticated %}
  {% if user.is_approved or user.is_superuser %}
  <div class="col-lg-5">
    <div class="card-warm card-warm-body" style="background:var(--parchment);">
      <p class="section-label">Escribe tu resena</p>
      <form action="/libros/{{ book.id }}/resena/" method="post">
        {% csrf_token %}
        <div class="mb-3">
          <label class="form-label">Calificacion</label>
          <select name="rating" class="form-select">
            <option value="5">5 estrellas</option>
            <option value="4">4 estrellas</option>
            <option value="3">3 estrellas</option>
            <option value="2">2 estrellas</option>
            <option value="1">1 estrella</option>
          </select>
        </div>
        <div class="mb-3">
          <label class="form-label">Comentario</label>
          <textarea name="comment" class="form-control" rows="4" placeholder="Que te parecio el libro?" required></textarea>
        </div>
        <button class="btn-primary-warm">Enviar resena</button>
        <p style="font-size:0.75rem;color:var(--ink-light);margin-top:0.5rem;">Pasa por moderacion antes de publicarse.</p>
      </form>
    </div>
  </div>
  {% endif %}
  {% endif %}
</div>
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# events_page.html
# ─────────────────────────────────────────────
files[f"{BASE}/events_page.html"] = """
{% extends 'base.html' %}
{% block content %}
<p class="section-label mb-0">Agenda</p>
<h1 style="font-size:1.75rem;margin-bottom:2rem;">Eventos del club</h1>
<p class="section-label">Proximos</p>
{% for e in upcoming %}
<div class="card-warm card-warm-body mb-3">
  <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap">
    <div>
      <h3 style="font-size:1.0625rem;margin-bottom:0.25rem;">{{ e.title }}</h3>
      <div style="font-size:0.8125rem;color:var(--ink-light);">
        <span class="badge-warm">{{ e.event_type }}</span>
        <span style="margin-left:0.5rem;">{{ e.starts_at|date:"j M Y, H:i" }}</span>
        {% if e.location %} &middot; {{ e.location }}{% endif %}
      </div>
      {% if e.description %}<p style="margin-top:0.5rem;font-size:0.875rem;margin-bottom:0;">{{ e.description }}</p>{% endif %}
    </div>
    {% if e.external_video_url %}<a href="{{ e.external_video_url }}" class="btn-outline-warm" target="_blank" rel="noopener">Ver video</a>{% endif %}
  </div>
</div>
{% empty %}<p style="color:var(--ink-light);">Sin eventos proximos.</p>{% endfor %}
<hr class="divider">
<p class="section-label">Pasados</p>
{% for e in past %}
<div class="card-warm card-warm-body mb-2" style="opacity:0.75;">
  <div class="d-flex justify-content-between align-items-center gap-2 flex-wrap">
    <div>
      <strong style="font-family:var(--serif);">{{ e.title }}</strong>
      <span style="font-size:0.8125rem;color:var(--ink-light);margin-left:0.5rem;">{{ e.event_type }} &middot; {{ e.starts_at|date:"j M Y" }}</span>
    </div>
    {% if e.external_video_url %}<a href="{{ e.external_video_url }}" class="btn-outline-warm" target="_blank" style="font-size:0.8125rem;padding:0.25rem 0.6rem;">Video</a>{% endif %}
  </div>
</div>
{% empty %}<p style="color:var(--ink-light);">Sin eventos pasados.</p>{% endfor %}
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# auth/login.html
# ─────────────────────────────────────────────
files[f"{BASE}/auth/login.html"] = """
{% extends 'base.html' %}
{% block content %}
<div style="max-width:400px;margin:2rem auto;">
  <p class="section-label">Acceso</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">Entrar al club</h1>
  <div class="card-warm card-warm-body">
    <form method="post">{% csrf_token %}
      {{ form.as_p }}
      <button class="btn-primary-warm w-100" style="margin-top:0.5rem;">Entrar</button>
    </form>
    {% if club_settings.google_login_enabled and club_settings.google_client_id and club_settings.google_client_secret %}
    <hr class="divider">
    <a href="/accounts/google/login/" class="btn-outline-warm w-100" style="text-align:center;display:block;">Entrar con Google</a>
    {% endif %}
  </div>
  <p style="text-align:center;font-size:0.875rem;color:var(--ink-light);margin-top:1.25rem;">
    No tienes cuenta? <a href="/registro/" style="color:var(--ink);">Registrate</a>
  </p>
</div>
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# auth/register.html
# ─────────────────────────────────────────────
files[f"{BASE}/auth/register.html"] = """
{% extends 'base.html' %}
{% block content %}
<div style="max-width:440px;margin:2rem auto;">
  <p class="section-label">Unete</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">Crear cuenta</h1>
  <div class="card-warm card-warm-body">
    <form method="post">{% csrf_token %}
      {{ form.as_p }}
      <button class="btn-primary-warm w-100" style="margin-top:0.5rem;">Crear cuenta</button>
    </form>
  </div>
  <p style="text-align:center;font-size:0.875rem;color:var(--ink-light);margin-top:1.25rem;">Tu cuenta quedara pendiente de aprobacion por un administrador.</p>
  <p style="text-align:center;font-size:0.875rem;color:var(--ink-light);">Ya tienes cuenta? <a href="/login/" style="color:var(--ink);">Entrar</a></p>
</div>
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# dashboard.html
# ─────────────────────────────────────────────
files[f"{BASE}/dashboard.html"] = """
{% extends 'base.html' %}
{% block content %}
<div class="row g-4">
  <div class="col-lg-3">
    <div class="card-warm card-warm-body position-sticky" style="top:1rem;">
      <p class="section-label">Panel de control</p>
      <nav class="side-nav">
        <a class="{% if seccion == 'inicio' %}active{% endif %}" href="/dashboard/?seccion=inicio">Inicio</a>
        <a class="{% if seccion == 'stats' %}active{% endif %}" href="/dashboard/?seccion=stats">Estadisticas</a>
        <a class="{% if seccion == 'libros' %}active{% endif %}" href="/dashboard/?seccion=libros">Libros</a>
        <a class="{% if seccion == 'eventos' %}active{% endif %}" href="/dashboard/?seccion=eventos">Eventos</a>
        <a class="{% if seccion == 'usuarios' %}active{% endif %}" href="/dashboard/?seccion=usuarios">Usuarios {% if users_pending.count %}<span class="badge-warm future">{{ users_pending.count }}</span>{% endif %}</a>
        <a class="{% if seccion == 'resenas' %}active{% endif %}" href="/dashboard/?seccion=resenas">Resenas {% if pending_reviews_count %}<span class="badge-warm future">{{ pending_reviews_count }}</span>{% endif %}</a>
        <a class="{% if seccion == 'integraciones' %}active{% endif %}" href="/dashboard/?seccion=integraciones">Integraciones</a>
        <a class="{% if seccion == 'perfil' %}active{% endif %}" href="/dashboard/?seccion=perfil">Mi perfil</a>
      </nav>
    </div>
  </div>
  <div class="col-lg-9">

    {% if seccion == 'inicio' %}
    <p class="section-label">Personalizacion</p>
    <h2 style="margin-bottom:1.5rem;">Configuracion del club</h2>
    <div class="card-warm card-warm-body mb-4">
      <form action="/dashboard/configuracion/" method="post" class="row g-3">{% csrf_token %}
        <input type="hidden" name="seccion" value="inicio">
        <div class="col-md-6"><label class="form-label">Nombre del club</label>{{ settings_form.name }}</div>
        <div class="col-md-6"><label class="form-label">URL del logo</label>{{ settings_form.logo_url }}</div>
        <div class="col-12"><label class="form-label">Descripcion publica</label>{{ settings_form.description }}</div>
        <div class="col-md-4"><label class="form-label">Color principal</label>{{ settings_form.primary_color }}</div>
        <div class="col-md-4"><label class="form-label">Color secundario</label>{{ settings_form.accent_color }}</div>
        <div class="col-md-4"><label class="form-label">Tag de afiliado Amazon</label>{{ settings_form.affiliate_tag }}</div>
        <div class="col-12"><button class="btn-primary-warm">Guardar</button></div>
      </form>
    </div>
    {% endif %}

    {% if seccion == 'stats' %}
    <p class="section-label">Resumen</p>
    <h2 style="margin-bottom:1.5rem;">Estadisticas</h2>
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3"><div class="card-warm card-warm-body" style="text-align:center;"><div style="font-size:1.75rem;font-family:var(--serif);font-weight:600;">{{ stats.total_books }}</div><div style="font-size:0.75rem;color:var(--ink-light);">Libros totales</div></div></div>
      <div class="col-6 col-md-3"><div class="card-warm card-warm-body" style="text-align:center;"><div style="font-size:1.75rem;font-family:var(--serif);font-weight:600;color:#2D6A2D;">{{ stats.books_read }}</div><div style="font-size:0.75rem;color:var(--ink-light);">Leidos</div></div></div>
      <div class="col-6 col-md-3"><div class="card-warm card-warm-body" style="text-align:center;"><div style="font-size:1.75rem;font-family:var(--serif);font-weight:600;color:#7A4F0D;">{{ stats.total_votes }}</div><div style="font-size:0.75rem;color:var(--ink-light);">Votos emitidos</div></div></div>
      <div class="col-6 col-md-3"><div class="card-warm card-warm-body" style="text-align:center;"><div style="font-size:1.75rem;font-family:var(--serif);font-weight:600;">{{ stats.approved_users }}</div><div style="font-size:0.75rem;color:var(--ink-light);">Miembros activos</div></div></div>
    </div>
    {% if stats.top_voted %}
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Libros mas votados</p>
      {% for item in stats.top_voted %}
      <div class="d-flex justify-content-between align-items-center py-2 {% if not forloop.last %}border-bottom{% endif %}" style="border-color:var(--parchment-3) !important;">
        <div><strong style="font-family:var(--serif);">{{ item.title }}</strong><span style="font-size:0.8125rem;color:var(--ink-light);margin-left:0.5rem;">{{ item.author }}</span></div>
        <span class="badge-warm future">{{ item.vote_count }} voto{{ item.vote_count|pluralize:"s" }}</span>
      </div>
      {% endfor %}
    </div>
    {% endif %}
    {% if stats.recent_reviews %}
    <div class="card-warm card-warm-body">
      <p class="section-label">Resenas recientes</p>
      {% for r in stats.recent_reviews %}
      <div class="py-2 {% if not forloop.last %}border-bottom{% endif %}" style="border-color:var(--parchment-3) !important;">
        <div class="d-flex justify-content-between"><strong style="font-size:0.875rem;">{{ r.book.title }}</strong><span class="stars" style="font-size:0.8125rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}★{% else %}☆{% endif %}{% endfor %}</span></div>
        <div style="font-size:0.8125rem;color:var(--ink-light);">{{ r.user.username }} &middot; {{ r.created_at|date:"j M" }}</div>
        <p style="font-size:0.875rem;margin:0.25rem 0 0;">{{ r.comment|truncatechars:120 }}</p>
      </div>
      {% endfor %}
    </div>
    {% endif %}
    {% endif %}

    {% if seccion == 'libros' %}
    <p class="section-label">Gestion</p>
    <h2 style="margin-bottom:1.5rem;">Libros</h2>
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Agregar libro</p>
      <form action="/libros/nuevo/" method="post">{% csrf_token %}{{ book_form.as_p }}<button class="btn-primary-warm">Guardar libro</button></form>
    </div>
    {% for b in books %}
    <div class="card-warm card-warm-body mb-2">
      <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
        <div>
          <strong style="font-family:var(--serif);">{{ b.title }}</strong>
          <span class="badge-warm {% if b.status == 'reading' %}reading{% elif b.status == 'completed' %}completed{% else %}future{% endif %} ms-2">{{ b.get_status_display }}</span>
          <div style="font-size:0.8125rem;color:var(--ink-light);">{{ b.author }}</div>
        </div>
        <div class="d-flex gap-2">
          <a href="/libros/{{ b.id }}/" class="btn-outline-warm" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Ver</a>
          <form action="/libros/{{ b.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar este libro?')">
            {% csrf_token %}<button class="btn-danger-warm" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Eliminar</button>
          </form>
        </div>
      </div>
      <form action="/libros/{{ b.id }}/editar/" method="post" class="row g-2 mt-2">{% csrf_token %}
        <div class="col-md-5"><input class="form-control" name="title" value="{{ b.title }}"></div>
        <div class="col-md-4"><input class="form-control" name="author" value="{{ b.author }}"></div>
        <div class="col-md-2">
          <select class="form-select" name="status">
            <option value="completed" {% if b.status == "completed" %}selected{% endif %}>Leido</option>
            <option value="reading" {% if b.status == "reading" %}selected{% endif %}>Leyendo</option>
            <option value="future" {% if b.status == "future" %}selected{% endif %}>Por leer</option>
          </select>
        </div>
        <div class="col-md-1"><button class="btn-primary-warm w-100" style="padding:0.45rem 0.5rem;">OK</button></div>
      </form>
    </div>
    {% endfor %}
    {% endif %}

    {% if seccion == 'eventos' %}
    <p class="section-label">Gestion</p>
    <h2 style="margin-bottom:1.5rem;">Eventos</h2>
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Agregar evento</p>
      <form action="/eventos/nuevo/" method="post">{% csrf_token %}{{ event_form.as_p }}<button class="btn-primary-warm">Guardar evento</button></form>
    </div>
    {% for e in events_all %}
    <div class="card-warm card-warm-body mb-2">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <strong style="font-family:var(--serif);">{{ e.title }}</strong>
          <div style="font-size:0.8125rem;color:var(--ink-light);">{{ e.event_type }} &middot; {{ e.starts_at|date:"j M Y, H:i" }}</div>
        </div>
        <form action="/eventos/{{ e.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar este evento?')">
          {% csrf_token %}<button class="btn-danger-warm" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Eliminar</button>
        </form>
      </div>
    </div>
    {% endfor %}
    {% endif %}

    {% if seccion == 'usuarios' %}
    <p class="section-label">Gestion</p>
    <h2 style="margin-bottom:1.5rem;">Usuarios</h2>
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Invitar usuario</p>
      <form action="/admin/invitar/" method="post" class="row g-2">{% csrf_token %}
        <div class="col-md-4"><label class="form-label">Nombre completo</label><input class="form-control" name="name" placeholder="Ana Torres" required></div>
        <div class="col-md-4"><label class="form-label">Correo</label><input class="form-control" name="email" type="email" required></div>
        <div class="col-md-2"><label class="form-label">Rol</label><select class="form-select" name="role"><option value="user">Usuario</option><option value="admin">Admin</option></select></div>
        <div class="col-md-2 d-flex align-items-end"><button class="btn-primary-warm w-100">Invitar</button></div>
      </form>
    </div>
    {% if users_pending %}
    <div class="card-warm card-warm-body mb-4" style="border-color:#F0D295;">
      <p class="section-label">Pendientes de aprobacion</p>
      {% for u in users_pending %}
      <div class="d-flex justify-content-between align-items-center py-2 {% if not forloop.last %}border-bottom{% endif %}" style="border-color:var(--parchment-3) !important;">
        <div><strong>{{ u.username }}</strong><span style="font-size:0.8125rem;color:var(--ink-light);margin-left:0.5rem;">{{ u.email }}</span></div>
        <form action="/usuarios/{{ u.id }}/aprobar/" method="post" style="margin:0;">{% csrf_token %}<button class="btn-primary-warm" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Aprobar</button></form>
      </div>
      {% endfor %}
    </div>
    {% endif %}
    <div class="card-warm card-warm-body">
      <p class="section-label">Miembros actuales</p>
      {% for u in users_all %}
      <div class="py-3 {% if not forloop.last %}border-bottom{% endif %}" style="border-color:var(--parchment-3) !important;">
        <form action="/usuarios/{{ u.id }}/editar/" method="post" class="row g-2 align-items-end">{% csrf_token %}
          <div class="col-md-3"><label class="form-label">Nombre</label><input class="form-control" name="full_name" value="{{ u.full_name }}"></div>
          <div class="col-md-4"><label class="form-label">Correo</label><input class="form-control" name="email" value="{{ u.email }}"></div>
          <div class="col-md-3"><label class="form-label">Libro favorito</label><input class="form-control" name="favorite_book" value="{{ u.favorite_book }}"></div>
          <div class="col-md-2 d-flex gap-1">
            <button class="btn-primary-warm flex-fill" style="font-size:0.8125rem;padding:0.4rem 0;">OK</button>
          </div>
        </form>
        <form action="/usuarios/{{ u.id }}/eliminar/" method="post" style="margin:0.5rem 0 0;" onsubmit="return confirm('Eliminar a {{ u.username }}?')">
          {% csrf_token %}<button class="btn-danger-warm" style="font-size:0.8125rem;padding:0.3rem 0.75rem;">Eliminar usuario</button>
        </form>
      </div>
      {% endfor %}
    </div>
    {% endif %}

    {% if seccion == 'resenas' %}
    <p class="section-label">Moderacion</p>
    <h2 style="margin-bottom:1.5rem;">Resenas</h2>
    {% for r in reviews_all %}
    <div class="card-warm card-warm-body mb-3">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <div><strong style="font-family:var(--serif);">{{ r.book.title }}</strong><span style="font-size:0.8125rem;color:var(--ink-light);margin-left:0.5rem;">{{ r.user.username }}</span></div>
        <span class="stars" style="font-size:0.875rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}★{% else %}☆{% endif %}{% endfor %}</span>
      </div>
      <p style="font-size:0.9375rem;margin-bottom:0.75rem;">{{ r.comment }}</p>
      {% if r.is_approved %}<span class="badge-warm reading mb-2">Aprobada</span>{% elif r.is_flagged %}<span class="badge-warm future mb-2">Marcada</span>{% else %}<span class="badge-warm mb-2">Pendiente</span>{% endif %}
      <div class="d-flex gap-2 flex-wrap mt-2">
        <form action="/resenas/{{ r.id }}/aprobar/" method="post" style="margin:0;" class="d-flex gap-1">
          {% csrf_token %}<input name="moderation_note" class="form-control" style="width:160px;font-size:0.8125rem;" placeholder="Nota opcional">
          <button class="btn-primary-warm" style="font-size:0.8125rem;">Aprobar</button>
        </form>
        <form action="/resenas/{{ r.id }}/marcar/" method="post" style="margin:0;" class="d-flex gap-1">
          {% csrf_token %}<input name="moderation_note" class="form-control" style="width:160px;font-size:0.8125rem;" placeholder="Motivo" required>
          <button class="btn-outline-warm" style="font-size:0.8125rem;">Marcar</button>
        </form>
        <form action="/resenas/{{ r.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar resena?')">
          {% csrf_token %}<button class="btn-danger-warm" style="font-size:0.8125rem;">Eliminar</button>
        </form>
      </div>
    </div>
    {% empty %}<p style="color:var(--ink-light);">No hay resenas.</p>{% endfor %}
    {% endif %}

    {% if seccion == 'integraciones' %}
    <p class="section-label">Integraciones</p>
    <h2 style="margin-bottom:1.5rem;">Google y redes sociales</h2>
    {% if settings_form.google_login_enabled %}
    <div class="card-warm card-warm-body mb-4">
      <p class="section-label">Google OAuth</p>
      <form action="/dashboard/configuracion/" method="post" class="row g-3">{% csrf_token %}
        <input type="hidden" name="seccion" value="integraciones">
        <div class="col-12 d-flex align-items-center gap-2">{{ settings_form.google_login_enabled }}<label class="form-label mb-0">Habilitar inicio de sesion con Google</label></div>
        <div class="col-md-6"><label class="form-label">Google Client ID</label>{{ settings_form.google_client_id }}</div>
        <div class="col-md-6"><label class="form-label">Google Client Secret</label>{{ settings_form.google_client_secret }}</div>
        <div class="col-12"><button class="btn-primary-warm">Guardar</button></div>
      </form>
    </div>
    {% endif %}
    <div class="card-warm card-warm-body">
      <p class="section-label">Redes sociales</p>
      <form action="/integraciones/redes/nueva/" method="post" class="row g-2 mb-3">{% csrf_token %}
        <div class="col-md-4"><label class="form-label">Red social</label>{{ social_form.network }}</div>
        <div class="col-md-6"><label class="form-label">URL</label>{{ social_form.url }}</div>
        <div class="col-md-2 d-flex align-items-end"><button class="btn-primary-warm w-100">Agregar</button></div>
      </form>
      {% for link in social_links %}
      <div class="d-flex justify-content-between align-items-center py-2 {% if not forloop.last %}border-bottom{% endif %}" style="border-color:var(--parchment-3) !important;">
        <span style="font-size:0.875rem;">{{ link.network }} &mdash; {{ link.url }}</span>
        <form action="/integraciones/redes/{{ link.id }}/eliminar/" method="post" style="margin:0;">{% csrf_token %}<button class="btn-danger-warm" style="font-size:0.8125rem;padding:0.25rem 0.6rem;">Eliminar</button></form>
      </div>
      {% empty %}<p style="color:var(--ink-light);margin:0;font-size:0.875rem;">Sin redes registradas.</p>{% endfor %}
    </div>
    {% endif %}

    {% if seccion == 'perfil' %}
    <p class="section-label">Tu cuenta</p>
    <h2 style="margin-bottom:1.5rem;">Mi perfil</h2>
    <div class="card-warm card-warm-body" style="max-width:520px;">
      <form action="/perfil/editar/" method="post">{% csrf_token %}
        {{ profile_form.as_p }}
        <button class="btn-primary-warm mt-2">Guardar perfil</button>
      </form>
    </div>
    {% endif %}

  </div>
</div>
{% endblock %}
""".strip()

# ─────────────────────────────────────────────
# Escribir todos los archivos
# ─────────────────────────────────────────────
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK  {path}")

print("\nTodos los templates escritos correctamente.")