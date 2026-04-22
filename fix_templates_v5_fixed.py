"""
fix_templates_v5.py
Escribe todos los templates con el sistema de temas completo.
Uso:
    docker compose cp fix_templates_v5.py web:/app/fix_templates_v5.py
    docker compose exec web python /app/fix_templates_v5.py
"""
import os

BASE = "/app/app/templates"
os.makedirs(f"{BASE}/auth", exist_ok=True)

T = {}

# ══════════════════════════════════════════════════════════════
# BASE.HTML — injects theme vars from context
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/base.html"] = """{% load static %}
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="{{ theme_vars.primary }}">
{% if club_settings.meta_description %}<meta name="description" content="{{ club_settings.meta_description }}">{% endif %}
<link rel="manifest" href="/pwa/manifest.json">
{% if club_settings.icon_url %}<link rel="icon" href="{{ club_settings.icon_url }}">
{% else %}<link rel="icon" type="image/svg+xml" href="{% static 'favicon.svg' %}">{% endif %}
<title>{{ club_settings.name }}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{{ theme_vars.fonts }}" rel="stylesheet">
<style>
:root{
  --page:{{ theme_vars.page }};
  --surface:{{ theme_vars.surface }};
  --border:{{ theme_vars.border }};
  --border2:{{ theme_vars.border2 }};
  --primary:{{ theme_vars.primary }};
  --accent:{{ theme_vars.accent }};
  --accent-bg:{{ theme_vars.accent_bg }};
  --accent-bdr:{{ theme_vars.accent_bdr }};
  --ink:{{ theme_vars.ink }};
  --ink-mid:{{ theme_vars.ink_mid }};
  --ink-light:{{ theme_vars.ink_light }};
  --serif:{{ theme_vars.serif }};
  --sans:{{ theme_vars.sans }};
  --r:8px;--rl:14px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--sans);font-size:15px;background:var(--page);color:var(--ink-mid);min-height:100vh;-webkit-font-smoothing:antialiased;}
h1,h2,h3,h4{font-family:var(--serif);color:var(--ink);font-weight:600;line-height:1.2;}
a{color:inherit;text-decoration:none;}
p{line-height:1.65;}
textarea,input,select,button{font-family:var(--sans);}

/* NAV */
.cl-nav{background:var(--surface);border-bottom:1px solid var(--border);height:56px;display:flex;align-items:center;padding:0 1.5rem;gap:1.25rem;position:sticky;top:0;z-index:200;}
.cl-logomark{width:32px;height:32px;background:var(--primary);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.cl-brand{font-family:var(--serif);font-size:1rem;font-weight:600;color:var(--ink);letter-spacing:-.01em;}
.cl-navlink{font-size:.8125rem;color:var(--ink-light);padding:4px 10px;border-radius:6px;transition:color .12s,background .12s;}
.cl-navlink:hover{color:var(--ink);background:var(--accent-bg);}

/* BUTTONS */
.btn{font-size:.8125rem;font-weight:500;border-radius:var(--r);padding:8px 16px;cursor:pointer;border:none;display:inline-block;transition:opacity .12s,transform .1s;line-height:1.4;white-space:nowrap;}
.btn:active{transform:scale(.98);}
.btn-dark{background:var(--primary);color:var(--page);}
.btn-dark:hover{opacity:.88;color:var(--page);}
.btn-ghost{background:transparent;color:var(--ink-light);border:1px solid var(--border2);}
.btn-ghost:hover{background:var(--accent-bg);color:var(--ink);}
.btn-accent{background:var(--accent);color:var(--surface);}
.btn-accent:hover{opacity:.88;color:var(--surface);}
.btn-danger{background:#8B2020;color:#fff;}
.btn-danger:hover{opacity:.88;color:#fff;}
.btn-sm{padding:5px 12px;font-size:.75rem;}

/* CARDS */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden;}
.card-body{padding:1.25rem 1.5rem;}
.card-header{padding:.75rem 1.5rem;border-bottom:1px solid var(--border);background:var(--accent-bg);display:flex;align-items:center;justify-content:space-between;}
.card-header-label{font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);}

/* FORMS */
.field{margin-bottom:1rem;}
.lbl{font-size:.75rem;font-weight:500;color:var(--ink-light);display:block;margin-bottom:5px;letter-spacing:.02em;}
.inp,.sel,.txa{font-size:.875rem;color:var(--ink);background:var(--surface);border:1px solid var(--border2);border-radius:var(--r);padding:9px 13px;width:100%;outline:none;transition:border-color .12s,box-shadow .12s;-webkit-appearance:none;appearance:none;}
.inp:focus,.sel:focus,.txa:focus{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 15%,transparent);}
.txa{resize:vertical;min-height:80px;line-height:1.6;}
.hint{font-size:.6875rem;color:var(--ink-light);margin-top:4px;line-height:1.5;}

/* CHIPS */
.chip{display:inline-flex;align-items:center;padding:3px 10px;border-radius:20px;font-size:.6875rem;font-weight:500;white-space:nowrap;}
.chip-reading{background:#EBF5EB;color:#2D5A2D;}
.chip-future{background:var(--accent-bg);color:var(--accent);border:1px solid var(--accent-bdr);}
.chip-done{background:#EEF0F8;color:#2D3A6A;}
.chip-muted{background:var(--page);color:var(--ink-light);border:1px solid var(--border);}

/* EYEBROW */
.eyebrow{font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:.375rem;}

/* SIDEBAR NAV */
.sidenav-item{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:var(--r);font-size:.875rem;color:var(--ink-light);transition:background .12s,color .12s;margin-bottom:2px;}
.sidenav-item:hover{background:var(--accent-bg);color:var(--ink);}
.sidenav-item.active{background:var(--accent-bg);color:var(--ink);font-weight:500;border-left:2px solid var(--accent);border-radius:0 var(--r) var(--r) 0;padding-left:10px;}
.badge-count{background:var(--accent-bg);color:var(--accent);border:1px solid var(--accent-bdr);font-size:.625rem;padding:1px 6px;border-radius:10px;font-weight:600;}

/* ALERTS */
.alert{padding:.75rem 1rem;border-radius:var(--r);font-size:.875rem;margin-bottom:1rem;}
.alert-info{background:var(--accent-bg);border:1px solid var(--accent-bdr);color:var(--ink);}

/* GRID */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;}
@media(max-width:680px){.g2,.g3,.g4{grid-template-columns:1fr;}}
@media(max-width:900px){.g3{grid-template-columns:1fr 1fr;}.g4{grid-template-columns:1fr 1fr;}}

/* STATS */
.stat{background:var(--surface);border:1px solid var(--border);border-radius:var(--rl);padding:1rem;text-align:center;}
.stat-num{font-family:var(--serif);font-size:1.75rem;font-weight:600;color:var(--ink);line-height:1;}
.stat-lbl{font-size:.6875rem;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-light);margin-top:4px;}

details summary{list-style:none;cursor:pointer;}
details summary::-webkit-details-marker{display:none;}

/* FOOTER */
.cl-footer{border-top:1px solid var(--border);padding:1.5rem;text-align:center;font-size:.8125rem;color:var(--ink-light);background:var(--surface);margin-top:3rem;}
.cl-footer a{color:var(--ink-light);}
.cl-footer a:hover{color:var(--ink);}

@media(max-width:768px){.hide-mobile{display:none!important;}}
</style>
</head>
<body>

<nav class="cl-nav">
  <div class="cl-logomark">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <rect x="3" y="4" width="12" height="2" rx="1" fill="white" fill-opacity=".9"/>
      <rect x="3" y="8" width="12" height="2" rx="1" fill="white" fill-opacity=".9"/>
      <rect x="3" y="12" width="8" height="2" rx="1" fill="white" fill-opacity=".9"/>
    </svg>
  </div>
  {% if club_settings.nav_logo %}
    <a href="/"><img src="{{ club_settings.nav_logo }}" alt="{{ club_settings.name }}" style="height:30px;width:auto;object-fit:contain;max-width:140px;"></a>
  {% else %}
    <a href="/" class="cl-brand">{{ club_settings.name }}</a>
  {% endif %}
  <div class="hide-mobile" style="display:flex;gap:2px;margin-left:.25rem;">
    <a href="/libros/" class="cl-navlink">Libros</a>
    <a href="/eventos/" class="cl-navlink">Eventos</a>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;align-items:center;">
    {% if user.is_authenticated %}
      <a href="/dashboard/" class="btn btn-ghost">Panel</a>
      <form action="/logout/" method="post" style="margin:0;">{% csrf_token %}
        <button class="btn btn-dark">Salir</button>
      </form>
    {% else %}
      <a href="/login/" class="btn btn-ghost">{{ club_settings.effective_cta_login }}</a>
      <a href="/registro/" class="btn btn-dark">{{ club_settings.effective_cta_register }}</a>
    {% endif %}
  </div>
</nav>

<main style="max-width:1200px;margin:0 auto;padding:2rem 1.5rem;">
  {% if messages %}{% for message in messages %}
    <div class="alert alert-info">{{ message }}</div>
  {% endfor %}{% endif %}
  {% block content %}{% endblock %}
</main>

<footer class="cl-footer">
  {% if club_settings.footer_text %}<p style="margin-bottom:.5rem;">{{ club_settings.footer_text }}</p>{% endif %}
  <div style="display:flex;justify-content:center;align-items:center;gap:1rem;flex-wrap:wrap;">
    {% if club_settings.footer_powered_by_name %}
      Powered by <a href="{{ club_settings.footer_powered_by_url }}" target="_blank" rel="noopener">{{ club_settings.footer_powered_by_name }}</a>
    {% else %}
      Powered by <a href="https://goldtech.mx" target="_blank" rel="noopener">Gold Tech Mx</a>
    {% endif %}
    &nbsp;&middot;&nbsp;
    <a href="https://github.com/bobybonillamx/club_lectura" target="_blank" rel="noopener">GitHub</a>
    {% if club_settings.footer_custom_link_text and club_settings.footer_custom_link_url %}
      &nbsp;&middot;&nbsp;
      <a href="{{ club_settings.footer_custom_link_url }}" target="_blank" rel="noopener">{{ club_settings.footer_custom_link_text }}</a>
    {% endif %}
  </div>
</footer>

<script>if('serviceWorker' in navigator) navigator.serviceWorker.register('/pwa/sw.js');</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/home.html"] = """{% extends 'base.html' %}
{% block content %}

{% if club_settings.cover_image_url %}
<div style="margin:-2rem -1.5rem 2rem;height:320px;overflow:hidden;position:relative;">
  <img src="{{ club_settings.cover_image_url }}" alt="{{ club_settings.name }}" style="width:100%;height:100%;object-fit:cover;display:block;">
  <div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.65) 0%,transparent 60%);"></div>
  <div style="position:absolute;bottom:2rem;left:2rem;">
    <p class="eyebrow" style="color:rgba(255,255,255,.75);">{% if club_settings.home_welcome_text %}{{ club_settings.home_welcome_text }}{% else %}Bienvenido{% endif %}</p>
    <h1 style="font-size:2.25rem;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.4);">{{ club_settings.name }}</h1>
    {% if club_settings.description %}<p style="color:rgba(255,255,255,.85);max-width:480px;font-size:.9375rem;margin-top:.375rem;">{{ club_settings.description }}</p>{% endif %}
  </div>
</div>
{% else %}
<section style="padding:1.5rem 0 2rem;">
  <p class="eyebrow">{% if club_settings.home_welcome_text %}{{ club_settings.home_welcome_text }}{% else %}Bienvenido{% endif %}</p>
  <h1 style="font-size:2rem;margin-bottom:.375rem;">{{ club_settings.name }}</h1>
  {% if club_settings.description %}<p style="color:var(--ink-light);max-width:520px;font-size:.9375rem;">{{ club_settings.description }}</p>{% endif %}
</section>
{% endif %}

<div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem;max-width:600px;margin-bottom:2rem;">
  <div class="card card-body">
    <p class="eyebrow" style="margin-bottom:.375rem;">Leyendo ahora</p>
    {% if current_book %}
      <p style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);font-weight:600;margin-bottom:2px;">{{ current_book.title }}</p>
      <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;">{{ current_book.author }}</p>
    {% else %}<p style="font-size:.875rem;color:var(--ink-light);">Sin libro activo</p>{% endif %}
  </div>
  <div class="card card-body">
    <p class="eyebrow" style="margin-bottom:.375rem;">Proximo evento</p>
    {% if next_event %}
      <p style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);font-weight:600;margin-bottom:2px;">{{ next_event.title }}</p>
      <p style="font-size:.8125rem;color:var(--ink-light);">{{ next_event.starts_at|date:"j M, H:i" }}</p>
    {% else %}<p style="font-size:.875rem;color:var(--ink-light);">Sin eventos proximos</p>{% endif %}
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 300px;gap:2rem;">
  <div>
    <p class="eyebrow" style="margin-bottom:1rem;">Biblioteca del club</p>
    {% for book in books %}
    <div class="card" style="margin-bottom:.875rem;display:flex;">
      {% if book.cover_url %}
        <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:72px;height:108px;object-fit:cover;flex-shrink:0;border-radius:14px 0 0 14px;">
      {% else %}
        <div style="width:72px;height:108px;background:var(--accent-bg);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">&#128214;</div>
      {% endif %}
      <div style="flex:1;padding:1rem 1.125rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;margin-bottom:.5rem;">
          <div>
            <h3 style="font-size:.9375rem;margin-bottom:2px;">{{ book.title }}</h3>
            <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;">{{ book.author }}</p>
          </div>
          <span class="chip {% if book.status == 'reading' %}chip-reading{% elif book.status == 'completed' %}chip-done{% else %}chip-future{% endif %}">{{ book.get_status_display }}</span>
        </div>
        {% if book.status == 'future' and book.allow_voting %}
        <div style="background:var(--accent-bg);border:1px solid var(--accent-bdr);border-radius:var(--r);padding:.5rem .75rem;margin-bottom:.5rem;font-size:.8125rem;color:var(--accent);">
          Votacion abierta &middot; {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}
        </div>
        {% endif %}
        <div style="display:flex;gap:.75rem;align-items:center;flex-wrap:wrap;">
          <a href="/libros/{{ book.id }}/" class="btn btn-ghost btn-sm">Ver detalle</a>
          {% if book.amazon_url %}<a href="{{ book.amazon_url }}" target="_blank" rel="noopener" style="font-size:.8125rem;color:var(--ink-light);">Amazon &#8599;</a>{% endif %}
          {% if book.pdf_url %}{% if user.is_authenticated and user.is_approved or user.is_superuser %}
          <a href="{{ book.pdf_url }}" target="_blank" rel="noopener" style="font-size:.8125rem;color:var(--ink-light);">PDF &#8599;</a>
          {% endif %}{% endif %}
        </div>
        {% with approved=book.reviews.all %}{% if approved %}
        <div style="margin-top:.75rem;padding-top:.75rem;border-top:1px solid var(--border);">
          {% for review in approved %}{% if review.is_approved %}
          <p style="font-size:.8125rem;color:var(--ink-light);line-height:1.5;">
            <span style="color:var(--accent);">{% for i in "12345" %}{% if forloop.counter <= review.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
            <strong style="color:var(--ink);margin:0 3px;">{{ review.user.username }}</strong>&mdash; {{ review.comment|truncatechars:90 }}
          </p>
          {% endif %}{% endfor %}
        </div>
        {% endif %}{% endwith %}
      </div>
    </div>
    {% empty %}<p style="color:var(--ink-light);">Aun no hay libros registrados.</p>{% endfor %}
  </div>

  <aside>
    <div class="card card-body" style="margin-bottom:1rem;">
      <p class="eyebrow" style="margin-bottom:.875rem;">Proximos eventos</p>
      {% for event in events %}
      <div style="padding:.625rem 0;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
        <p style="font-family:var(--serif);font-size:.875rem;color:var(--ink);font-weight:600;margin-bottom:2px;">{{ event.title }}</p>
        <p style="font-size:.75rem;color:var(--ink-light);">{{ event.event_type }} &middot; {{ event.starts_at|date:"j M" }}</p>
        {% if event.location %}<p style="font-size:.75rem;color:var(--ink-light);">{{ event.location }}</p>{% endif %}
      </div>
      {% empty %}<p style="font-size:.875rem;color:var(--ink-light);">Sin eventos proximos.</p>{% endfor %}
    </div>
    {% if links %}
    <div class="card card-body" style="margin-bottom:1rem;">
      <p class="eyebrow" style="margin-bottom:.75rem;">Redes del club</p>
      {% for link in links %}
      <a href="{{ link.url }}" target="_blank" rel="noopener" style="display:block;font-size:.875rem;color:var(--ink-light);padding:3px 0;">&#8599; {{ link.network }}</a>
      {% endfor %}
    </div>
    {% endif %}
    <button class="btn btn-ghost" style="width:100%;" onclick="navigator.share?navigator.share({title:document.title,url:location.href}):alert('Comparte: '+location.href)">Compartir club</button>
  </aside>
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# BOOKS PAGE
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/books_page.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;">
  <div><p class="eyebrow" style="margin-bottom:.25rem;">Biblioteca</p><h1 style="font-size:1.75rem;">Libros del club</h1></div>
</div>
<form method="get" action="/libros/" style="display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:2rem;">
  <input type="text" name="q" value="{{ query|default:'' }}" class="inp" placeholder="Buscar por titulo o autor..." style="max-width:280px;width:100%;">
  <select name="estado" class="sel" style="max-width:170px;width:100%;" onchange="this.form.submit()">
    <option value="">Todos los estados</option>
    <option value="completed" {% if estado == 'completed' %}selected{% endif %}>Leidos</option>
    <option value="reading" {% if estado == 'reading' %}selected{% endif %}>Leyendo</option>
    <option value="future" {% if estado == 'future' %}selected{% endif %}>En votacion</option>
  </select>
  <button class="btn btn-dark" type="submit">Buscar</button>
  {% if query or estado %}<a href="/libros/" class="btn btn-ghost">Limpiar</a>{% endif %}
</form>
{% for book in books %}
<a href="/libros/{{ book.id }}/" style="display:block;text-decoration:none;margin-bottom:.75rem;">
  <div class="card" style="{% if book.status == 'future' and book.allow_voting %}border-color:var(--accent-bdr);{% endif %}transition:box-shadow .15s;" onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,.07)'" onmouseout="this.style.boxShadow=''">
    {% if book.status == 'future' and book.allow_voting %}
    <div style="background:var(--accent-bg);border-bottom:1px solid var(--accent-bdr);padding:.375rem 1.25rem;font-size:.75rem;color:var(--accent);display:flex;align-items:center;gap:.5rem;">
      &#128717; <strong>Votacion abierta</strong> &mdash; {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }} &middot; Entra para votar
    </div>
    {% endif %}
    <div style="display:flex;align-items:center;">
      {% if book.cover_url %}
        <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:48px;height:72px;object-fit:cover;flex-shrink:0;">
      {% else %}
        <div style="width:48px;height:72px;background:var(--accent-bg);display:flex;align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;">&#128214;</div>
      {% endif %}
      <div style="flex:1;padding:.875rem 1.125rem;display:flex;justify-content:space-between;align-items:center;gap:.75rem;">
        <div>
          <p style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);margin-bottom:2px;">{{ book.title }}</p>
          <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;">{{ book.author }}</p>
        </div>
        <span class="chip {% if book.status == 'reading' %}chip-reading{% elif book.status == 'completed' %}chip-done{% else %}chip-future{% endif %}">{{ book.get_status_display }}</span>
      </div>
    </div>
  </div>
</a>
{% empty %}<p style="color:var(--ink-light);padding:2rem 0;">No se encontraron libros con estos filtros.</p>{% endfor %}
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# BOOK DETAIL
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/book_detail.html"] = """{% extends 'base.html' %}
{% block content %}
<a href="/libros/" class="btn btn-ghost btn-sm" style="margin-bottom:1.5rem;display:inline-block;">&#8592; Volver</a>
<div style="display:grid;grid-template-columns:200px 1fr;gap:2rem;margin-bottom:2rem;">
  <div>
    {% if book.cover_url %}
      <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:12px;max-width:200px;">
    {% else %}
      <div style="width:100%;aspect-ratio:2/3;background:var(--accent-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:3rem;max-width:200px;">&#128214;</div>
    {% endif %}
  </div>
  <div>
    <span class="chip {% if book.status == 'reading' %}chip-reading{% elif book.status == 'completed' %}chip-done{% else %}chip-future{% endif %}" style="margin-bottom:.75rem;display:inline-flex;">{{ book.get_status_display }}</span>
    <h1 style="font-size:1.75rem;margin-bottom:.25rem;">{{ book.title }}</h1>
    {% if book.author %}<p style="font-size:1rem;color:var(--ink-light);font-style:italic;margin-bottom:1rem;">{{ book.author }}</p>{% endif %}
    {% if book.description %}<p style="line-height:1.75;color:var(--ink-mid);max-width:580px;margin-bottom:1.25rem;">{{ book.description }}</p>{% endif %}
    <div style="display:flex;flex-wrap:wrap;gap:.625rem;margin-bottom:1.5rem;">
      {% if book.amazon_url %}<a href="{{ book.amazon_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Ver en Amazon &#8599;</a>{% endif %}
      {% if book.external_video_url %}<a href="{{ book.external_video_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Video &#8599;</a>{% endif %}
      {% if book.pdf_url %}
        {% if user.is_authenticated %}
          {% if user.is_approved or user.is_superuser %}
            <a href="{{ book.pdf_url }}" class="btn btn-accent btn-sm" target="_blank" rel="noopener">&#128196; Descargar PDF</a>
          {% else %}
            <span class="chip chip-muted">PDF disponible para miembros aprobados</span>
          {% endif %}
        {% else %}
          <a href="/login/" class="btn btn-ghost btn-sm">Inicia sesion para acceder al PDF</a>
        {% endif %}
      {% endif %}
    </div>
    {% if book.status == 'future' and book.allow_voting %}
    <div style="background:var(--accent-bg);border:1px solid var(--accent-bdr);border-radius:12px;padding:1.25rem 1.5rem;max-width:460px;">
      <p class="eyebrow" style="margin-bottom:.5rem;">Votacion abierta</p>
      <p style="font-family:var(--serif);font-size:1.0625rem;color:var(--ink);margin-bottom:.375rem;">Quieres que leamos este libro?</p>
      <p style="font-size:.875rem;color:var(--ink-light);margin-bottom:1rem;">Puedes votar por todos los libros que quieras. El mas votado sera el proximo.</p>
      <p style="font-size:1.5rem;font-family:var(--serif);font-weight:600;color:var(--accent);margin-bottom:.875rem;">{{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}</p>
      {% if user_vote %}
        <p style="font-size:.9375rem;color:#2D5A2D;">&#10003; Ya votaste por este libro</p>
      {% elif user.is_authenticated %}
        {% if user.is_approved or user.is_superuser %}
        <form action="/libros/{{ book.id }}/votar/" method="post">{% csrf_token %}
          <input type="hidden" name="next" value="/libros/{{ book.id }}/">
          <button class="btn btn-accent">Votar por este libro</button>
        </form>
        {% else %}
          <p style="font-size:.875rem;color:var(--ink-light);">Tu cuenta esta pendiente de aprobacion para votar.</p>
        {% endif %}
      {% else %}
        <a href="/login/" class="btn btn-ghost">Inicia sesion para votar</a>
      {% endif %}
    </div>
    {% endif %}
  </div>
</div>
<hr style="border:none;border-top:1px solid var(--border);margin:0 0 2rem;">
<div style="display:grid;grid-template-columns:1fr 360px;gap:2rem;">
  <div>
    <p class="eyebrow" style="margin-bottom:1rem;">Resenas</p>
    {% for review in approved_reviews %}
    <div class="card card-body" style="margin-bottom:.875rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.375rem;">
        <strong style="font-size:.9375rem;color:var(--ink);">{{ review.user.username }}</strong>
        <span style="color:var(--accent);font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= review.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
      </div>
      <p style="font-size:.9375rem;color:var(--ink-mid);line-height:1.6;margin-bottom:.375rem;">{{ review.comment }}</p>
      <p style="font-size:.75rem;color:var(--ink-light);">{{ review.created_at|date:"j M Y" }}</p>
    </div>
    {% empty %}<p style="color:var(--ink-light);">Aun no hay resenas aprobadas.</p>{% endfor %}
  </div>
  {% if user.is_authenticated %}{% if user.is_approved or user.is_superuser %}
  <div>
    <div class="card">
      <div class="card-header"><span class="card-header-label">Escribe tu resena</span></div>
      <div class="card-body">
        <form action="/libros/{{ book.id }}/resena/" method="post">{% csrf_token %}
          <div class="field"><label class="lbl">Calificacion</label>
            <select name="rating" class="sel">
              <option value="5">&#9733;&#9733;&#9733;&#9733;&#9733; Excelente</option>
              <option value="4">&#9733;&#9733;&#9733;&#9733;&#9734; Muy bueno</option>
              <option value="3">&#9733;&#9733;&#9733;&#9734;&#9734; Bueno</option>
              <option value="2">&#9733;&#9733;&#9734;&#9734;&#9734; Regular</option>
              <option value="1">&#9733;&#9734;&#9734;&#9734;&#9734; No me gusto</option>
            </select>
          </div>
          <div class="field"><label class="lbl">Tu comentario</label>
            <textarea name="comment" class="txa" rows="4" placeholder="Que te parecio el libro?" required></textarea>
          </div>
          <button class="btn btn-dark">Enviar resena</button>
          <p class="hint" style="margin-top:.5rem;">Pasa por moderacion antes de publicarse.</p>
        </form>
      </div>
    </div>
  </div>
  {% endif %}{% endif %}
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# EVENTS PAGE
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/events_page.html"] = """{% extends 'base.html' %}
{% block content %}
<p class="eyebrow" style="margin-bottom:.375rem;">Agenda</p>
<h1 style="font-size:1.75rem;margin-bottom:2rem;">Eventos del club</h1>
<p class="eyebrow" style="margin-bottom:.875rem;">Proximos</p>
{% for e in upcoming %}
<div class="card card-body" style="margin-bottom:.875rem;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap;">
    <div>
      <h3 style="font-size:1.0625rem;margin-bottom:.25rem;">{{ e.title }}</h3>
      <p style="font-size:.8125rem;color:var(--ink-light);">
        <span class="chip chip-muted" style="margin-right:.375rem;">{{ e.event_type }}</span>
        {{ e.starts_at|date:"j M Y, H:i" }}{% if e.location %} &middot; {{ e.location }}{% endif %}
      </p>
      {% if e.description %}<p style="font-size:.9375rem;color:var(--ink-mid);margin-top:.5rem;line-height:1.6;">{{ e.description }}</p>{% endif %}
    </div>
    {% if e.external_video_url %}<a href="{{ e.external_video_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Ver video &#8599;</a>{% endif %}
  </div>
</div>
{% empty %}<p style="color:var(--ink-light);margin-bottom:1.5rem;">Sin eventos proximos.</p>{% endfor %}
<hr style="border:none;border-top:1px solid var(--border);margin:1.5rem 0;">
<p class="eyebrow" style="margin-bottom:.875rem;">Pasados</p>
{% for e in past %}
<div class="card card-body" style="margin-bottom:.625rem;opacity:.72;">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
    <div>
      <strong style="font-family:var(--serif);color:var(--ink);">{{ e.title }}</strong>
      <span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ e.event_type }} &middot; {{ e.starts_at|date:"j M Y" }}</span>
    </div>
    {% if e.external_video_url %}<a href="{{ e.external_video_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Video</a>{% endif %}
  </div>
</div>
{% empty %}<p style="color:var(--ink-light);">Sin eventos pasados.</p>{% endfor %}
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# DASHBOARD — with theme selector in inicio
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/dashboard.html"] = """{% extends 'base.html' %}{% load theme_tags %}
{% block content %}
<div style="display:grid;grid-template-columns:220px 1fr;gap:1.5rem;align-items:start;">

  <aside style="position:sticky;top:72px;">
    <div class="card card-body" style="padding:1rem;">
      <p class="eyebrow" style="margin-bottom:.75rem;">Panel de control</p>
      <a href="/dashboard/?seccion=inicio"        class="sidenav-item {% if seccion == 'inicio'        %}active{% endif %}">Inicio</a>
      <a href="/dashboard/?seccion=stats"         class="sidenav-item {% if seccion == 'stats'         %}active{% endif %}">Estadisticas</a>
      <a href="/dashboard/?seccion=libros"        class="sidenav-item {% if seccion == 'libros'        %}active{% endif %}">Libros</a>
      <a href="/dashboard/?seccion=eventos"       class="sidenav-item {% if seccion == 'eventos'       %}active{% endif %}">Eventos</a>
      <a href="/dashboard/?seccion=usuarios"      class="sidenav-item {% if seccion == 'usuarios'      %}active{% endif %}">
        Usuarios {% if users_pending.count %}<span class="badge-count">{{ users_pending.count }}</span>{% endif %}
      </a>
      <a href="/dashboard/?seccion=resenas"       class="sidenav-item {% if seccion == 'resenas'       %}active{% endif %}">
        Resenas {% if pending_reviews_count %}<span class="badge-count">{{ pending_reviews_count }}</span>{% endif %}
      </a>
      <a href="/dashboard/?seccion=integraciones" class="sidenav-item {% if seccion == 'integraciones' %}active{% endif %}">Integraciones</a>
      <a href="/dashboard/?seccion=correos"       class="sidenav-item {% if seccion == 'correos'       %}active{% endif %}">Correos</a>
      <a href="/dashboard/?seccion=apariencia"    class="sidenav-item {% if seccion == 'apariencia'    %}active{% endif %}">Apariencia</a>
      <a href="/dashboard/?seccion=perfil"        class="sidenav-item {% if seccion == 'perfil'        %}active{% endif %}">Mi perfil</a>
    </div>
  </aside>

  <div>

    <!-- ══ INICIO ══ -->
    {% if seccion == 'inicio' %}
    <h2 style="margin-bottom:1.5rem;">Configuracion del club</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Identidad</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="inicio">
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Nombre del club</label><input class="inp" name="name" value="{{ cfg.name }}"></div>
            <div class="field"><label class="lbl">Meta descripcion (SEO)</label><input class="inp" name="meta_description" value="{{ cfg.meta_description }}" placeholder="Describe tu club para Google..."><p class="hint">Max 160 caracteres recomendado.</p></div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Descripcion publica</label>
            <textarea class="txa" name="description" rows="2">{{ cfg.description }}</textarea>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Mensaje de bienvenida (encabezado de la home)</label>
            <input class="inp" name="home_welcome_text" value="{{ cfg.home_welcome_text }}" placeholder="Bienvenido">
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Imagen de portada (hero de la home)</label>
            <input class="inp" name="cover_image_url" value="{{ cfg.cover_image_url }}" placeholder="https://...">
            <p class="hint">Imagen horizontal 1400x500px o mayor. Si se deja vacio se muestra solo el texto.</p>
            {% if cfg.cover_image_url %}<img src="{{ cfg.cover_image_url }}" style="margin-top:.75rem;width:100%;max-height:100px;object-fit:cover;border-radius:var(--r);border:1px solid var(--border);">{% endif %}
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field">
              <label class="lbl">Logo navbar (rectangular)</label>
              <input class="inp" name="logo_url" value="{{ cfg.logo_url }}" placeholder="https://...">
              <p class="hint">PNG transparente, max 300x80px.</p>
            </div>
            <div class="field">
              <label class="lbl">Icono PWA / favicon (cuadrado)</label>
              <input class="inp" name="icon_url" value="{{ cfg.icon_url }}" placeholder="https://...">
              <p class="hint">512x512px. Acceso directo en movil. Usado en navbar si no hay logo.</p>
            </div>
          </div>
          {% if cfg.nav_logo or cfg.icon_url %}
          <div style="display:flex;gap:1rem;padding:.875rem 1rem;background:var(--page);border-radius:var(--r);margin-bottom:1rem;">
            {% if cfg.nav_logo %}<div style="text-align:center;"><p class="hint" style="margin-bottom:4px;">Logo navbar</p><img src="{{ cfg.nav_logo }}" style="height:36px;width:auto;max-width:160px;object-fit:contain;"></div>{% endif %}
            {% if cfg.icon_url %}<div style="text-align:center;"><p class="hint" style="margin-bottom:4px;">Icono PWA</p><img src="{{ cfg.icon_url }}" style="width:44px;height:44px;object-fit:cover;border-radius:10px;border:1px solid var(--border);"></div>{% endif %}
          </div>
          {% endif %}
          <button class="btn btn-dark">Guardar identidad</button>
        </form>
      </div>
    </div>

    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Textos del sitio</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="inicio">
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Boton de registro</label><input class="inp" name="cta_register_text" value="{{ cfg.cta_register_text }}" placeholder="Registro"></div>
            <div class="field"><label class="lbl">Boton de login</label><input class="inp" name="cta_login_text" value="{{ cfg.cta_login_text }}" placeholder="Entrar"></div>
          </div>
          <button class="btn btn-dark">Guardar textos</button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><span class="card-header-label">Redes sociales</span></div>
      <div class="card-body">
        <form action="/integraciones/redes/nueva/" method="post" style="margin-bottom:1rem;">{% csrf_token %}
          <div style="display:grid;grid-template-columns:1fr 2fr auto;gap:.75rem;align-items:end;">
            <div class="field" style="margin-bottom:0;"><label class="lbl">Red social</label><input class="inp" name="network" placeholder="Instagram..."></div>
            <div class="field" style="margin-bottom:0;"><label class="lbl">URL</label><input class="inp" name="url" type="url" placeholder="https://..."></div>
            <button class="btn btn-ghost">Agregar</button>
          </div>
        </form>
        {% if social_links %}
        <div style="border-top:1px solid var(--border);padding-top:.875rem;">
          {% for link in social_links %}
          <div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem 0;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
            <div><span style="font-weight:500;font-size:.875rem;color:var(--ink);">{{ link.network }}</span><a href="{{ link.url }}" target="_blank" rel="noopener" style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ link.url|truncatechars:40 }}</a></div>
            <form action="/integraciones/redes/{{ link.id }}/eliminar/" method="post" style="margin:0;">{% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button></form>
          </div>
          {% endfor %}
        </div>
        {% else %}<p style="font-size:.875rem;color:var(--ink-light);">Sin redes registradas.</p>{% endif %}
      </div>
    </div>
    {% endif %}

    <!-- ══ APARIENCIA ══ -->
    {% if seccion == 'apariencia' %}
    <h2 style="margin-bottom:.5rem;">Apariencia</h2>
    <p style="color:var(--ink-light);font-size:.875rem;margin-bottom:1.5rem;">Elige un tema predefinido. Si quieres ajustes finos sobre el tema, puedes sobreescribir los colores despues.</p>

    <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
      <input type="hidden" name="seccion" value="apariencia">

      <div class="card" style="margin-bottom:1.25rem;">
        <div class="card-header"><span class="card-header-label">Tema predefinido</span></div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.875rem;margin-bottom:1.25rem;">

            {% for theme_key, theme_label in theme_choices %}
            <label style="cursor:pointer;">
              <input type="radio" name="theme" value="{{ theme_key }}" {% if cfg.theme == theme_key %}checked{% endif %} style="position:absolute;opacity:0;width:0;height:0;">
              <div style="border:2px solid {% if cfg.theme == theme_key %}var(--accent){% else %}var(--border){% endif %};border-radius:12px;overflow:hidden;transition:border-color .15s;" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='{% if cfg.theme == theme_key %}var(--accent){% else %}var(--border){% endif %}'">
                <div style="height:80px;background:{{ theme_key|theme_page_color }};padding:.75rem;display:flex;flex-direction:column;justify-content:space-between;">
                  <div style="height:12px;background:{{ theme_key|theme_primary_color }};border-radius:4px;width:60%;opacity:.9;"></div>
                  <div>
                    <div style="height:8px;background:{{ theme_key|theme_ink_color }};border-radius:3px;width:80%;opacity:.7;margin-bottom:4px;"></div>
                    <div style="height:6px;background:{{ theme_key|theme_ink_color }};border-radius:3px;width:55%;opacity:.4;"></div>
                  </div>
                  <div style="height:14px;background:{{ theme_key|theme_primary_color }};border-radius:4px;width:40%;"></div>
                </div>
                <div style="padding:.625rem .75rem;background:white;">
                  <p style="font-size:.8125rem;font-weight:500;color:#111;margin-bottom:1px;">{{ theme_label }}</p>
                  {% if cfg.theme == theme_key %}<p style="font-size:.6875rem;color:var(--accent);">Activo</p>{% endif %}
                </div>
              </div>
            </label>
            {% endfor %}

          </div>
          <button class="btn btn-dark" type="submit">Aplicar tema</button>
        </div>
      </div>

      <div class="card">
        <div class="card-header"><span class="card-header-label">Ajustes finos de color (opcional)</span></div>
        <div class="card-body">
          <p style="font-size:.875rem;color:var(--ink-light);margin-bottom:1rem;">Sobreescribe colores especificos del tema. Dejar en blanco para usar los del tema seleccionado.</p>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field">
              <label class="lbl">Color primario (botones, nav icon)</label>
              <div style="display:flex;gap:.5rem;align-items:center;">
                <input type="color" class="inp" name="primary_color" value="{{ cfg.primary_color|default:'#3D2B1F' }}" style="width:52px;height:42px;padding:3px 6px;cursor:pointer;flex-shrink:0;">
                <input type="text" class="inp" id="primary_color_hex" value="{{ cfg.primary_color }}" placeholder="Dejar vacio para usar el del tema" style="flex:1;" oninput="document.querySelector('[name=primary_color]').value=this.value">
              </div>
            </div>
            <div class="field">
              <label class="lbl">Color acento (links, chips, eyebrows)</label>
              <div style="display:flex;gap:.5rem;align-items:center;">
                <input type="color" class="inp" name="accent_color" value="{{ cfg.accent_color|default:'#B87333' }}" style="width:52px;height:42px;padding:3px 6px;cursor:pointer;flex-shrink:0;">
                <input type="text" class="inp" id="accent_color_hex" value="{{ cfg.accent_color }}" placeholder="Dejar vacio para usar el del tema" style="flex:1;" oninput="document.querySelector('[name=accent_color]').value=this.value">
              </div>
            </div>
          </div>
          <div style="display:flex;gap:.75rem;">
            <button class="btn btn-dark" type="submit">Guardar colores</button>
            <a href="/dashboard/reset-colores/" class="btn btn-ghost btn-sm">Restablecer colores del tema</a>
          </div>
        </div>
      </div>
    </form>

    <div class="card" style="margin-top:1.25rem;">
      <div class="card-header"><span class="card-header-label">Footer</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="apariencia">
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Powered by — nombre</label><input class="inp" name="footer_powered_by_name" value="{{ cfg.footer_powered_by_name }}" placeholder="Gold Tech Mx"></div>
            <div class="field"><label class="lbl">Powered by — URL</label><input class="inp" name="footer_powered_by_url" value="{{ cfg.footer_powered_by_url }}" type="url" placeholder="https://goldtech.mx"></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Link adicional — texto</label><input class="inp" name="footer_custom_link_text" value="{{ cfg.footer_custom_link_text }}" placeholder="Terminos de uso"></div>
            <div class="field"><label class="lbl">Link adicional — URL</label><input class="inp" name="footer_custom_link_url" value="{{ cfg.footer_custom_link_url }}" type="url" placeholder="https://..."></div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Texto libre del footer</label>
            <input class="inp" name="footer_text" value="{{ cfg.footer_text }}" placeholder="Copyright 2025 Mi Club de Lectura">
          </div>
          <button class="btn btn-dark">Guardar footer</button>
        </form>
      </div>
    </div>
    {% endif %}

    <!-- ══ STATS ══ -->
    {% if seccion == 'stats' %}
    <h2 style="margin-bottom:1.5rem;">Estadisticas</h2>
    <div class="g4" style="margin-bottom:1.5rem;">
      <div class="stat"><div class="stat-num">{{ stats.total_books }}</div><div class="stat-lbl">Libros totales</div></div>
      <div class="stat"><div class="stat-num" style="color:#2D6A2D;">{{ stats.books_read }}</div><div class="stat-lbl">Leidos</div></div>
      <div class="stat"><div class="stat-num" style="color:var(--accent);">{{ stats.total_votes }}</div><div class="stat-lbl">Votos</div></div>
      <div class="stat"><div class="stat-num">{{ stats.approved_users }}</div><div class="stat-lbl">Miembros</div></div>
    </div>
    {% if stats.top_voted %}
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Mas votados</span></div>
      <div class="card-body" style="padding:0;">
        {% for item in stats.top_voted %}
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div><span style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);">{{ item.title }}</span><span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;font-style:italic;">{{ item.author }}</span></div>
          <span class="chip chip-future">{{ item.vote_count }} voto{{ item.vote_count|pluralize:"s" }}</span>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
    {% if stats.recent_reviews %}
    <div class="card">
      <div class="card-header"><span class="card-header-label">Resenas recientes</span></div>
      <div class="card-body" style="padding:0;">
        {% for r in stats.recent_reviews %}
        <div style="padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
            <span style="font-family:var(--serif);font-size:.875rem;font-weight:600;color:var(--ink);">{{ r.book.title }}</span>
            <span style="color:var(--accent);font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
          </div>
          <p style="font-size:.8125rem;color:var(--ink-light);">{{ r.user.username }} &middot; {{ r.created_at|date:"j M" }}</p>
          <p style="font-size:.875rem;color:var(--ink-mid);margin-top:4px;">{{ r.comment|truncatechars:120 }}</p>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
    {% endif %}

    <!-- ══ LIBROS ══ -->
    {% if seccion == 'libros' %}
    <h2 style="margin-bottom:1.5rem;">Libros</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Agregar libro</span></div>
      <div class="card-body">
        <form action="/libros/nuevo/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Titulo *</label><input class="inp" name="title" required></div>
            <div class="field"><label class="lbl">Autor</label><input class="inp" name="author" placeholder="Se busca automaticamente"></div>
          </div>
          <div class="g3" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Estado</label><select class="sel" name="status"><option value="future">Por leer / Votacion</option><option value="reading">Leyendo</option><option value="completed">Leido</option></select></div>
            <div class="field"><label class="lbl">Visibilidad</label><select class="sel" name="visibility"><option value="public">Publico</option><option value="private">Solo miembros</option><option value="admins">Solo admins</option></select></div>
            <div class="field"><label class="lbl">Votos</label><select class="sel" name="allow_voting"><option value="True">Permitidos</option><option value="False">Desactivados</option></select></div>
          </div>
          <div class="field" style="margin-bottom:1rem;"><label class="lbl">Descripcion</label><textarea class="txa" name="description" rows="2" placeholder="Se busca automaticamente"></textarea></div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">URL portada</label><input class="inp" name="cover_url" type="url"></div>
            <div class="field"><label class="lbl">URL Amazon</label><input class="inp" name="amazon_url" type="url"></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">URL PDF (solo miembros activos)</label><input class="inp" name="pdf_url" type="url"></div>
            <div class="field"><label class="lbl">URL video</label><input class="inp" name="external_video_url" type="url"></div>
          </div>
          <div style="display:flex;align-items:center;gap:1rem;">
            <button class="btn btn-dark">Guardar libro</button>
            <label style="display:flex;align-items:center;gap:.5rem;font-size:.875rem;color:var(--ink-light);cursor:pointer;">
              <input type="checkbox" name="reemplazar_leyendo_actual" style="accent-color:var(--accent);width:16px;height:16px;">
              Mover libros "Leyendo" a "Leido"
            </label>
          </div>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><span class="card-header-label">Libros registrados</span></div>
      {% for b in books %}
      <div style="border-bottom:{% if not forloop.last %}1px solid var(--border){% else %}none{% endif %};">
        <div style="display:flex;">
          {% if b.cover_url %}<img src="{{ b.cover_url }}" alt="" style="width:52px;height:78px;object-fit:cover;flex-shrink:0;">
          {% else %}<div style="width:52px;height:78px;background:var(--accent-bg);display:flex;align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;">&#128214;</div>{% endif %}
          <div style="flex:1;padding:.875rem 1rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;flex-wrap:wrap;">
              <div>
                <span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ b.title }}</span>
                <span style="font-size:.8125rem;color:var(--ink-light);font-style:italic;margin-left:.5rem;">{{ b.author }}</span>
                <span class="chip {% if b.status == 'reading' %}chip-reading{% elif b.status == 'completed' %}chip-done{% else %}chip-future{% endif %}" style="margin-left:.5rem;">{{ b.get_status_display }}</span>
              </div>
              <div style="display:flex;gap:.5rem;">
                <a href="/libros/{{ b.id }}/" class="btn btn-ghost btn-sm">Ver</a>
                <form action="/libros/{{ b.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar?')">{% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button></form>
              </div>
            </div>
            <details style="margin-top:.75rem;">
              <summary style="font-size:.8125rem;color:var(--accent);display:inline-flex;align-items:center;gap:4px;">&#9998; Editar</summary>
              <form action="/libros/{{ b.id }}/editar/" method="post" style="margin-top:.75rem;">{% csrf_token %}
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">Titulo</label><input class="inp" name="title" value="{{ b.title }}"></div>
                  <div class="field"><label class="lbl">Autor</label><input class="inp" name="author" value="{{ b.author }}"></div>
                </div>
                <div class="g3" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">Estado</label><select class="sel" name="status"><option value="future" {% if b.status == "future" %}selected{% endif %}>Por leer</option><option value="reading" {% if b.status == "reading" %}selected{% endif %}>Leyendo</option><option value="completed" {% if b.status == "completed" %}selected{% endif %}>Leido</option></select></div>
                  <div class="field"><label class="lbl">Visibilidad</label><select class="sel" name="visibility"><option value="public" {% if b.visibility == "public" %}selected{% endif %}>Publico</option><option value="private" {% if b.visibility == "private" %}selected{% endif %}>Solo miembros</option><option value="admins" {% if b.visibility == "admins" %}selected{% endif %}>Solo admins</option></select></div>
                  <div class="field"><label class="lbl">Votos</label><select class="sel" name="allow_voting"><option value="True" {% if b.allow_voting %}selected{% endif %}>Permitidos</option><option value="False" {% if not b.allow_voting %}selected{% endif %}>Desactivados</option></select></div>
                </div>
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">URL portada</label><input class="inp" name="cover_url" value="{{ b.cover_url }}" type="url"></div>
                  <div class="field"><label class="lbl">URL Amazon</label><input class="inp" name="amazon_url" value="{{ b.amazon_url }}" type="url"></div>
                </div>
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">URL PDF</label><input class="inp" name="pdf_url" value="{{ b.pdf_url }}" type="url"></div>
                  <div class="field"><label class="lbl">URL video</label><input class="inp" name="external_video_url" value="{{ b.external_video_url }}" type="url"></div>
                </div>
                <div class="field" style="margin-bottom:.75rem;"><label class="lbl">Descripcion</label><textarea class="txa" name="description" rows="2">{{ b.description }}</textarea></div>
                <button class="btn btn-dark btn-sm">Guardar cambios</button>
              </form>
            </details>
          </div>
        </div>
      </div>
      {% empty %}<div style="padding:2rem 1.5rem;color:var(--ink-light);font-size:.875rem;">Sin libros registrados.</div>{% endfor %}
    </div>
    {% endif %}

    <!-- ══ EVENTOS ══ -->
    {% if seccion == 'eventos' %}
    <h2 style="margin-bottom:1.5rem;">Eventos</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Agregar evento</span></div>
      <div class="card-body">
        <form action="/eventos/nuevo/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Titulo *</label><input class="inp" name="title" required></div>
            <div class="field"><label class="lbl">Tipo</label><input class="inp" name="event_type" placeholder="Sesion, intercambio, cine..."></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Fecha y hora *</label><input class="inp" name="starts_at" type="datetime-local" required></div>
            <div class="field"><label class="lbl">Visibilidad</label><select class="sel" name="visibility"><option value="public">Publico</option><option value="private">Solo miembros</option><option value="admins">Solo admins</option></select></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Lugar</label><input class="inp" name="location" placeholder="Direccion o link"></div>
            <div class="field"><label class="lbl">Video</label><input class="inp" name="external_video_url" type="url"></div>
          </div>
          <div class="field" style="margin-bottom:1rem;"><label class="lbl">Descripcion</label><textarea class="txa" name="description" rows="2"></textarea></div>
          <button class="btn btn-dark">Guardar evento</button>
        </form>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><span class="card-header-label">Eventos registrados</span></div>
      {% for e in events_all %}
      <div style="border-bottom:{% if not forloop.last %}1px solid var(--border){% else %}none{% endif %};padding:.875rem 1.5rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;flex-wrap:wrap;">
          <div>
            <span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ e.title }}</span>
            <span class="chip chip-muted" style="margin-left:.5rem;">{{ e.event_type }}</span>
            <div style="font-size:.8125rem;color:var(--ink-light);margin-top:3px;">{{ e.starts_at|date:"j M Y, H:i" }}{% if e.location %} &middot; {{ e.location }}{% endif %}</div>
          </div>
          <form action="/eventos/{{ e.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar?')">{% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button></form>
        </div>
        <details style="margin-top:.75rem;">
          <summary style="font-size:.8125rem;color:var(--accent);display:inline-flex;align-items:center;gap:4px;">&#9998; Editar</summary>
          <form action="/eventos/{{ e.id }}/editar/" method="post" style="margin-top:.75rem;">{% csrf_token %}
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Titulo</label><input class="inp" name="title" value="{{ e.title }}"></div>
              <div class="field"><label class="lbl">Tipo</label><input class="inp" name="event_type" value="{{ e.event_type }}"></div>
            </div>
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Fecha y hora</label><input class="inp" name="starts_at" type="datetime-local" value="{{ e.starts_at|date:'Y-m-d' }}T{{ e.starts_at|date:'H:i' }}"></div>
              <div class="field"><label class="lbl">Visibilidad</label><select class="sel" name="visibility"><option value="public" {% if e.visibility == "public" %}selected{% endif %}>Publico</option><option value="private" {% if e.visibility == "private" %}selected{% endif %}>Solo miembros</option><option value="admins" {% if e.visibility == "admins" %}selected{% endif %}>Solo admins</option></select></div>
            </div>
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Lugar</label><input class="inp" name="location" value="{{ e.location }}"></div>
              <div class="field"><label class="lbl">Video</label><input class="inp" name="external_video_url" value="{{ e.external_video_url }}" type="url"></div>
            </div>
            <div class="field" style="margin-bottom:.75rem;"><label class="lbl">Descripcion</label><textarea class="txa" name="description" rows="2">{{ e.description }}</textarea></div>
            <button class="btn btn-dark btn-sm">Guardar</button>
          </form>
        </details>
      </div>
      {% empty %}<div style="padding:2rem 1.5rem;color:var(--ink-light);font-size:.875rem;">Sin eventos.</div>{% endfor %}
    </div>
    {% endif %}

    <!-- ══ USUARIOS ══ -->
    {% if seccion == 'usuarios' %}
    <h2 style="margin-bottom:1.5rem;">Usuarios</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Invitar usuario</span></div>
      <div class="card-body">
        <form action="/admin/invitar/" method="post">{% csrf_token %}
          <div style="display:grid;grid-template-columns:1fr 1fr 140px auto;gap:.75rem;align-items:end;">
            <div class="field" style="margin-bottom:0;"><label class="lbl">Nombre completo</label><input class="inp" name="name" required></div>
            <div class="field" style="margin-bottom:0;"><label class="lbl">Correo</label><input class="inp" name="email" type="email" required></div>
            <div class="field" style="margin-bottom:0;"><label class="lbl">Rol</label><select class="sel" name="role"><option value="user">Usuario</option><option value="admin">Admin</option></select></div>
            <button class="btn btn-dark">Invitar</button>
          </div>
        </form>
      </div>
    </div>
    {% if users_pending %}
    <div class="card" style="margin-bottom:1.25rem;border-color:var(--accent-bdr);">
      <div class="card-header"><span class="card-header-label">Pendientes ({{ users_pending.count }})</span></div>
      <div class="card-body" style="padding:0;">
        {% for u in users_pending %}
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div><span style="font-weight:500;color:var(--ink);">{{ u.username }}</span><span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ u.email }}</span></div>
          <form action="/usuarios/{{ u.id }}/aprobar/" method="post" style="margin:0;">{% csrf_token %}<button class="btn btn-accent btn-sm">Aprobar</button></form>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
    <div class="card">
      <div class="card-header"><span class="card-header-label">Miembros ({{ users_all|length }})</span></div>
      <div class="card-body" style="padding:0;">
        {% for u in users_all %}
        <div style="padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem;">
            <div>
              <span style="font-weight:500;color:var(--ink);">{{ u.username }}</span>
              <span style="font-size:.75rem;color:var(--ink-light);margin-left:.5rem;">{{ u.role }}</span>
              {% if u.is_approved %}<span class="chip chip-reading" style="margin-left:.5rem;font-size:.625rem;">activo</span>{% else %}<span class="chip chip-muted" style="margin-left:.5rem;font-size:.625rem;">pendiente</span>{% endif %}
            </div>
            <form action="/usuarios/{{ u.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar a {{ u.username }}?')">{% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button></form>
          </div>
          <form action="/usuarios/{{ u.id }}/editar/" method="post">{% csrf_token %}
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:.75rem;align-items:end;">
              <div class="field" style="margin-bottom:0;"><label class="lbl">Nombre</label><input class="inp" name="full_name" value="{{ u.full_name }}"></div>
              <div class="field" style="margin-bottom:0;"><label class="lbl">Correo</label><input class="inp" name="email" value="{{ u.email }}"></div>
              <div class="field" style="margin-bottom:0;"><label class="lbl">Libro favorito</label><input class="inp" name="favorite_book" value="{{ u.favorite_book }}"></div>
              <button class="btn btn-ghost btn-sm">Guardar</button>
            </div>
          </form>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}

    <!-- ══ RESENAS ══ -->
    {% if seccion == 'resenas' %}
    <h2 style="margin-bottom:1.5rem;">Moderacion de resenas</h2>
    {% for r in reviews_all %}
    <div class="card" style="margin-bottom:1rem;">
      <div class="card-body">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem;">
          <div><span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ r.book.title }}</span><span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">por {{ r.user.username }}</span></div>
          <div style="display:flex;align-items:center;gap:.5rem;">
            <span style="color:var(--accent);font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
            {% if r.is_approved %}<span class="chip chip-reading" style="font-size:.625rem;">Aprobada</span>{% elif r.is_flagged %}<span class="chip chip-future" style="font-size:.625rem;">Marcada</span>{% else %}<span class="chip chip-muted" style="font-size:.625rem;">Pendiente</span>{% endif %}
          </div>
        </div>
        <p style="font-size:.9375rem;color:var(--ink-mid);margin-bottom:1rem;line-height:1.55;">{{ r.comment }}</p>
        <div style="display:flex;gap:.75rem;flex-wrap:wrap;">
          <form action="/resenas/{{ r.id }}/aprobar/" method="post" style="margin:0;display:flex;gap:.5rem;">{% csrf_token %}
            <input class="inp" name="moderation_note" placeholder="Nota opcional" style="width:150px;font-size:.8125rem;padding:6px 10px;">
            <button class="btn btn-accent btn-sm">Aprobar</button>
          </form>
          <form action="/resenas/{{ r.id }}/marcar/" method="post" style="margin:0;display:flex;gap:.5rem;">{% csrf_token %}
            <input class="inp" name="moderation_note" placeholder="Motivo" required style="width:150px;font-size:.8125rem;padding:6px 10px;">
            <button class="btn btn-ghost btn-sm">Marcar</button>
          </form>
          <form action="/resenas/{{ r.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar?')">{% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button></form>
        </div>
      </div>
    </div>
    {% empty %}<div class="card card-body" style="color:var(--ink-light);">Sin resenas.</div>{% endfor %}
    {% endif %}

    <!-- ══ INTEGRACIONES ══ -->
    {% if seccion == 'integraciones' %}
    <h2 style="margin-bottom:1.5rem;">Integraciones</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Dominio publico</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div class="field" style="max-width:400px;">
            <label class="lbl">Dominio del sitio (sin https://)</label>
            <input class="inp" name="public_domain" value="{{ cfg.public_domain }}" placeholder="miclub.com">
            <p class="hint">Con Cloudflare Tunnel pon el dominio configurado en el tunel. Se usa en correos y PWA.</p>
          </div>
          <p style="font-size:.8125rem;color:var(--ink-light);margin-bottom:1rem;">URL actual: <strong style="color:var(--ink);">{{ cfg.public_url }}</strong></p>
          <button class="btn btn-dark">Guardar</button>
        </form>
      </div>
    </div>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header"><span class="card-header-label">Amazon afiliados</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div class="field" style="max-width:360px;">
            <label class="lbl">Tag de afiliado</label>
            <input class="inp" name="affiliate_tag" value="{{ cfg.affiliate_tag }}" placeholder="tu-tag-20">
            <p class="hint">Si se deja vacio se usara el tag predeterminado del sistema.</p>
          </div>
          <button class="btn btn-dark" style="margin-top:.5rem;">Guardar</button>
        </form>
      </div>
    </div>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-header">
        <span class="card-header-label">Servidor de correo SMTP</span>
        {% if cfg.smtp_configured %}<span class="chip chip-reading" style="font-size:.625rem;">Configurado</span>{% else %}<span class="chip chip-muted" style="font-size:.625rem;">Sin configurar</span>{% endif %}
      </div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Servidor SMTP</label><input class="inp" name="smtp_host" value="{{ cfg.smtp_host }}" placeholder="smtp.gmail.com"></div>
            <div class="field"><label class="lbl">Puerto</label><input class="inp" name="smtp_port" type="number" value="{{ cfg.smtp_port }}"></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Usuario</label><input class="inp" name="smtp_user" value="{{ cfg.smtp_user }}" placeholder="tu@gmail.com"></div>
            <div class="field"><label class="lbl">Contrasena / App Password</label><input class="inp" name="smtp_password" type="password" value="{{ cfg.smtp_password }}"></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Remitente</label><input class="inp" name="email_from" value="{{ cfg.email_from }}" placeholder="Mi Club &lt;club@midominio.com&gt;"></div>
            <div class="field" style="display:flex;align-items:flex-end;padding-bottom:.25rem;">
              <label style="display:flex;align-items:center;gap:.5rem;font-size:.875rem;color:var(--ink-mid);cursor:pointer;">
                <input type="checkbox" name="smtp_use_tls" {% if cfg.smtp_use_tls %}checked{% endif %} style="accent-color:var(--accent);width:18px;height:18px;">
                Usar TLS
              </label>
            </div>
          </div>
          <div style="display:flex;gap:.75rem;align-items:center;">
            <button class="btn btn-dark">Guardar SMTP</button>
            {% if cfg.smtp_configured %}<a href="/integraciones/smtp/test/" class="btn btn-ghost btn-sm">Enviar correo de prueba a {{ user.email }}</a>{% endif %}
          </div>
        </form>
      </div>
    </div>
    {% if settings_form.google_login_enabled %}
    <div class="card">
      <div class="card-header"><span class="card-header-label">Google OAuth</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;padding:.75rem 1rem;background:var(--accent-bg);border-radius:var(--r);">
            <input type="checkbox" id="g_en" name="google_login_enabled" {% if cfg.google_login_enabled %}checked{% endif %} style="width:18px;height:18px;accent-color:var(--accent);cursor:pointer;">
            <label for="g_en" style="font-size:.875rem;cursor:pointer;">Habilitar inicio de sesion con Google</label>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Google Client ID</label><input class="inp" name="google_client_id" value="{{ cfg.google_client_id }}"></div>
            <div class="field"><label class="lbl">Google Client Secret</label><input class="inp" name="google_client_secret" type="password" value="{{ cfg.google_client_secret }}"></div>
          </div>
          <p class="hint" style="margin-bottom:1rem;">Redirect URI: <code style="background:var(--page);padding:2px 6px;border-radius:4px;">{{ request.scheme }}://{{ request.get_host }}/accounts/google/login/callback/</code></p>
          <button class="btn btn-dark">Guardar</button>
        </form>
      </div>
    </div>
    {% endif %}
    {% endif %}

    <!-- ══ CORREOS ══ -->
    {% if seccion == 'correos' %}
    <h2 style="margin-bottom:.5rem;">Plantillas de correo</h2>
    <p style="color:var(--ink-light);font-size:.875rem;margin-bottom:1.5rem;">Variables disponibles: <code style="background:var(--accent-bg);padding:1px 6px;border-radius:4px;">{nombre}</code> <code style="background:var(--accent-bg);padding:1px 6px;border-radius:4px;">{club}</code> <code style="background:var(--accent-bg);padding:1px 6px;border-radius:4px;">{url}</code> <code style="background:var(--accent-bg);padding:1px 6px;border-radius:4px;">{usuario}</code> <code style="background:var(--accent-bg);padding:1px 6px;border-radius:4px;">{contrasena}</code></p>
    {% if not cfg.smtp_configured %}
    <div class="alert alert-info" style="margin-bottom:1.5rem;">Para enviar correos configura SMTP en <a href="/dashboard/?seccion=integraciones" style="text-decoration:underline;">Integraciones</a>.</div>
    {% endif %}
    <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
      <input type="hidden" name="seccion" value="correos">
      <div class="card" style="margin-bottom:1.25rem;">
        <div class="card-header"><span class="card-header-label">Bienvenida (al registrarse)</span></div>
        <div class="card-body"><div class="field"><label class="lbl">Texto del correo</label><textarea class="txa" name="email_tpl_welcome" rows="8" style="font-family:monospace;font-size:.8125rem;">{% if cfg.email_tpl_welcome %}{{ cfg.email_tpl_welcome }}{% else %}{{ default_tpl_welcome }}{% endif %}</textarea></div></div>
      </div>
      <div class="card" style="margin-bottom:1.25rem;">
        <div class="card-header"><span class="card-header-label">Cuenta aprobada</span></div>
        <div class="card-body"><div class="field"><label class="lbl">Texto del correo</label><textarea class="txa" name="email_tpl_approved" rows="8" style="font-family:monospace;font-size:.8125rem;">{% if cfg.email_tpl_approved %}{{ cfg.email_tpl_approved }}{% else %}{{ default_tpl_approved }}{% endif %}</textarea></div></div>
      </div>
      <div class="card" style="margin-bottom:1.5rem;">
        <div class="card-header"><span class="card-header-label">Invitacion</span></div>
        <div class="card-body"><div class="field"><label class="lbl">Texto del correo</label><textarea class="txa" name="email_tpl_invitation" rows="10" style="font-family:monospace;font-size:.8125rem;">{% if cfg.email_tpl_invitation %}{{ cfg.email_tpl_invitation }}{% else %}{{ default_tpl_invitation }}{% endif %}</textarea></div></div>
      </div>
      <button class="btn btn-dark">Guardar plantillas</button>
    </form>
    {% endif %}

    <!-- ══ PERFIL ══ -->
    {% if seccion == 'perfil' %}
    <h2 style="margin-bottom:1.5rem;">Mi perfil</h2>
    <div class="card" style="max-width:540px;">
      <div class="card-header"><span class="card-header-label">Datos personales</span></div>
      <div class="card-body">
        <form action="/perfil/editar/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Nombre completo</label><input class="inp" name="full_name" value="{{ user.full_name }}"></div>
            <div class="field"><label class="lbl">Correo</label><input class="inp" name="email" type="email" value="{{ user.email }}"></div>
          </div>
          <div class="field" style="margin-bottom:1rem;"><label class="lbl">Libro favorito</label><input class="inp" name="favorite_book" value="{{ user.favorite_book }}"></div>
          <div class="field" style="margin-bottom:1rem;"><label class="lbl">Biografia</label><textarea class="txa" name="bio" rows="3">{{ user.bio }}</textarea></div>
          <div class="field" style="margin-bottom:1.25rem;">
            <label class="lbl">URL foto de perfil</label>
            <input class="inp" name="avatar_url" type="url" value="{{ user.avatar_url }}" placeholder="https://...">
            {% if user.avatar_url %}<div style="margin-top:.75rem;display:flex;align-items:center;gap:.75rem;"><img src="{{ user.avatar_url }}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid var(--border);"><span class="hint">Foto actual</span></div>{% endif %}
          </div>
          <button class="btn btn-dark">Guardar perfil</button>
        </form>
      </div>
    </div>
    {% endif %}

  </div>
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/auth/login.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:400px;margin:2rem auto;">
  <p class="eyebrow" style="margin-bottom:.375rem;">Acceso</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">Entrar al club</h1>
  <div class="card card-body">
    <form method="post">{% csrf_token %}{{ form.as_p }}
      <button class="btn btn-dark" style="width:100%;margin-top:.5rem;">{{ club_settings.effective_cta_login }}</button>
    </form>
    {% if club_settings.google_login_enabled and club_settings.google_client_id and club_settings.google_client_secret %}
    <div style="display:flex;align-items:center;gap:.75rem;margin:1rem 0;">
      <div style="flex:1;height:1px;background:var(--border);"></div><span style="font-size:.8125rem;color:var(--ink-light);">o</span><div style="flex:1;height:1px;background:var(--border);"></div>
    </div>
    <a href="/accounts/google/login/" class="btn btn-ghost" style="width:100%;text-align:center;display:block;">Entrar con Google</a>
    {% endif %}
  </div>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);margin-top:1.25rem;">No tienes cuenta? <a href="/registro/" style="color:var(--ink);font-weight:500;">{{ club_settings.effective_cta_register }}</a></p>
</div>
{% endblock %}"""

T[f"{BASE}/auth/register.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:440px;margin:2rem auto;">
  <p class="eyebrow" style="margin-bottom:.375rem;">Unete</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">{{ club_settings.effective_cta_register }}</h1>
  <div class="card card-body">
    <form method="post">{% csrf_token %}{{ form.as_p }}
      <button class="btn btn-dark" style="width:100%;margin-top:.5rem;">Crear cuenta</button>
    </form>
  </div>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);margin-top:1rem;">Tu cuenta quedara pendiente de aprobacion.</p>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);">Ya tienes cuenta? <a href="/login/" style="color:var(--ink);font-weight:500;">{{ club_settings.effective_cta_login }}</a></p>
</div>
{% endblock %}"""

T[f"{BASE}/pending_users.html"] = """{% extends 'base.html' %}
{% block content %}
<h2 style="margin-bottom:1.5rem;">Usuarios pendientes</h2>
{% for u in users %}
<div class="card card-body" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem;">
  <div><span style="font-weight:500;color:var(--ink);">{{ u.username }}</span><span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ u.email }}</span></div>
  <form action="/usuarios/{{ u.id }}/aprobar/" method="post" style="margin:0;">{% csrf_token %}<button class="btn btn-accent btn-sm">Aprobar</button></form>
</div>
{% empty %}<div class="card card-body" style="color:var(--ink-light);">Sin usuarios pendientes.</div>{% endfor %}
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# WRITE
# ══════════════════════════════════════════════════════════════
for path, content in T.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"OK  {path}")

print(f"\n{len(T)} templates escritos. Recarga el navegador.")