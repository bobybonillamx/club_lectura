"""
fix_templates_v3.py
Escribe todos los templates del proyecto con el diseno mejorado.
Uso:
    docker compose cp fix_templates_v3.py web:/app/fix_templates_v3.py
    docker compose exec web python /app/fix_templates_v3.py
"""
import os

BASE = "/app/app/templates"
os.makedirs(f"{BASE}/auth", exist_ok=True)

T = {}

# ══════════════════════════════════════════════════════════════
# BASE.HTML
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/base.html"] = """{% load static %}
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="{{ club_settings.primary_color }}">
<link rel="manifest" href="/pwa/manifest.json">
{% if club_settings.icon_url %}
<link rel="icon" href="{{ club_settings.icon_url }}">
{% else %}
<link rel="icon" type="image/svg+xml" href="{% static 'favicon.svg' %}">
{% endif %}
<title>{{ club_settings.name }}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#1A0F0A;--ink-mid:#3D2B1F;--ink-light:#7A6252;
  --amber:#B87333;--amber-bg:#FDF3E3;--amber-bdr:#F0D8A8;
  --green-bg:#EBF5EB;--green-txt:#2D5A2D;
  --blue-bg:#EEF0F8;--blue-txt:#2D3A6A;
  --red-bg:#FBEAEA;--red-txt:#7A1F1F;
  --page:#F7F3EE;--surface:#FFFFFF;
  --border:#EAE0D5;--border2:#DDD4C8;
  --serif:'Lora',Georgia,serif;
  --sans:'Inter',system-ui,sans-serif;
  --r:8px;--rl:14px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--sans);font-size:15px;font-weight:400;background:var(--page);color:var(--ink-mid);min-height:100vh;-webkit-font-smoothing:antialiased;}
h1,h2,h3,h4{font-family:var(--serif);color:var(--ink);font-weight:600;line-height:1.2;}
a{color:inherit;text-decoration:none;}
p{line-height:1.65;margin-bottom:0;}

/* NAV */
.cl-nav{background:var(--surface);border-bottom:1px solid var(--border);height:56px;display:flex;align-items:center;padding:0 1.5rem;gap:1.25rem;position:sticky;top:0;z-index:200;}
.cl-logomark{width:32px;height:32px;background:var(--ink-mid);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.cl-brand{font-family:var(--serif);font-size:1rem;font-weight:600;color:var(--ink);letter-spacing:-.01em;}
.cl-navlink{font-size:.8125rem;color:var(--ink-light);padding:4px 10px;border-radius:6px;transition:color .12s,background .12s;}
.cl-navlink:hover{color:var(--ink);background:var(--page);}

/* BUTTONS */
.btn{font-family:var(--sans);font-size:.8125rem;font-weight:500;border-radius:var(--r);padding:8px 16px;cursor:pointer;border:none;display:inline-block;transition:opacity .12s,transform .1s;line-height:1.4;white-space:nowrap;}
.btn:active{transform:scale(.98);}
.btn-dark{background:var(--ink-mid);color:#F7F3EE;}
.btn-dark:hover{opacity:.88;color:#F7F3EE;}
.btn-ghost{background:transparent;color:var(--ink-light);border:1px solid var(--border2);}
.btn-ghost:hover{background:var(--page);color:var(--ink);}
.btn-amber{background:var(--amber);color:#FFF8F0;}
.btn-amber:hover{opacity:.88;color:#FFF8F0;}
.btn-red{background:#8B2020;color:#fff;}
.btn-red:hover{opacity:.88;color:#fff;}
.btn-sm{padding:5px 12px;font-size:.75rem;}

/* CARDS */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden;}
.card-body{padding:1.25rem 1.5rem;}
.card-section{padding:.75rem 1.5rem;border-bottom:1px solid var(--border);background:var(--page);}
.card-section-label{font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);}

/* FORMS */
.field{margin-bottom:1rem;}
.field:last-child{margin-bottom:0;}
.lbl{font-size:.75rem;font-weight:500;color:var(--ink-light);display:block;margin-bottom:5px;letter-spacing:.02em;}
.inp,.sel,.txa{font-family:var(--sans);font-size:.875rem;color:var(--ink);background:var(--surface);border:1px solid var(--border2);border-radius:var(--r);padding:9px 13px;width:100%;outline:none;transition:border-color .12s,box-shadow .12s;-webkit-appearance:none;appearance:none;}
.inp:focus,.sel:focus,.txa:focus{border-color:var(--amber);box-shadow:0 0 0 3px rgba(184,115,51,.12);}
.txa{resize:vertical;min-height:80px;}
.inp-hint{font-size:.6875rem;color:var(--ink-light);margin-top:4px;}

/* CHIPS */
.chip{display:inline-flex;align-items:center;padding:3px 10px;border-radius:20px;font-size:.6875rem;font-weight:500;white-space:nowrap;}
.chip-reading{background:var(--green-bg);color:var(--green-txt);}
.chip-future{background:var(--amber-bg);color:#7A4F15;border:1px solid var(--amber-bdr);}
.chip-done{background:var(--blue-bg);color:var(--blue-txt);}
.chip-pending{background:#F5F5F5;color:#555;}

/* DIVIDER */
.div{border:none;border-top:1px solid var(--border);margin:1.5rem 0;}

/* SIDEBAR NAV */
.sidenav-item{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:var(--r);font-size:.875rem;color:var(--ink-light);transition:background .12s,color .12s;margin-bottom:2px;}
.sidenav-item:hover{background:var(--page);color:var(--ink);}
.sidenav-item.active{background:var(--page);color:var(--ink);font-weight:500;border-left:2px solid var(--amber);border-radius:0 var(--r) var(--r) 0;padding-left:10px;}
.badge-count{background:var(--amber-bg);color:#7A4F15;border:1px solid var(--amber-bdr);font-size:.625rem;padding:1px 6px;border-radius:10px;font-weight:600;}

/* ALERTS */
.alert{padding:.75rem 1rem;border-radius:var(--r);font-size:.875rem;margin-bottom:1rem;}
.alert-info{background:var(--amber-bg);border:1px solid var(--amber-bdr);color:#5C3A10;}

/* GRID HELPERS */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;}
@media(max-width:640px){.g2,.g3,.g4{grid-template-columns:1fr;}}
@media(max-width:900px){.g3{grid-template-columns:1fr 1fr;}}

/* BOOK ROW */
.book-row{display:flex;gap:0;border-bottom:1px solid var(--border);}
.book-row:last-child{border-bottom:none;}
.book-thumb{width:56px;flex-shrink:0;background:var(--page);display:flex;align-items:center;justify-content:center;font-size:1.25rem;}
.book-info{flex:1;padding:.875rem 1rem;}

/* STAT CARD */
.stat{background:var(--surface);border:1px solid var(--border);border-radius:var(--rl);padding:1rem;text-align:center;}
.stat-num{font-family:var(--serif);font-size:1.75rem;font-weight:600;color:var(--ink);line-height:1;}
.stat-lbl{font-size:.6875rem;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-light);margin-top:4px;}

/* FOOTER */
.cl-footer{border-top:1px solid var(--border);padding:1.5rem;text-align:center;font-size:.8125rem;color:var(--ink-light);background:var(--surface);margin-top:3rem;}
.cl-footer a{color:var(--ink-light);}
.cl-footer a:hover{color:var(--ink);}

/* RESPONSIVE */
@media(max-width:768px){
  .hide-mobile{display:none!important;}
  .cl-nav{padding:0 1rem;gap:.75rem;}
}
</style>
</head>
<body>

<nav class="cl-nav">
  <div class="cl-logomark">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <rect x="3" y="4" width="12" height="2" rx="1" fill="#F7F3EE"/>
      <rect x="3" y="8" width="12" height="2" rx="1" fill="#F7F3EE"/>
      <rect x="3" y="12" width="8" height="2" rx="1" fill="#F7F3EE"/>
    </svg>
  </div>
  {% if club_settings.nav_logo %}
    <a href="/" style="display:flex;align-items:center;">
      <img src="{{ club_settings.nav_logo }}" alt="{{ club_settings.name }}" style="height:30px;width:auto;object-fit:contain;max-width:140px;">
    </a>
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
      <a href="/login/" class="btn btn-ghost">Entrar</a>
      <a href="/registro/" class="btn btn-dark">Registro</a>
    {% endif %}
  </div>
</nav>

<main style="max-width:1200px;margin:0 auto;padding:2rem 1.5rem;">
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-info">{{ message }}</div>
    {% endfor %}
  {% endif %}
  {% block content %}{% endblock %}
</main>

<footer class="cl-footer">
  Powered by <a href="https://goldtech.mx" target="_blank" rel="noopener">Gold Tech Mx</a>
  &nbsp;&middot;&nbsp;
  <a href="https://github.com/bobybonillamx/club_lectura" target="_blank" rel="noopener">Repositorio en GitHub</a>
</footer>

<script>if('serviceWorker' in navigator) navigator.serviceWorker.register('/pwa/sw.js');</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════
# DASHBOARD.HTML
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/dashboard.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="display:grid;grid-template-columns:220px 1fr;gap:1.5rem;align-items:start;">

  <!-- SIDEBAR -->
  <aside style="position:sticky;top:72px;">
    <div class="card card-body" style="padding:1rem;">
      <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.75rem;">Panel de control</p>
      <a href="/dashboard/?seccion=inicio"        class="sidenav-item {% if seccion == 'inicio'        %}active{% endif %}">Inicio</a>
      <a href="/dashboard/?seccion=stats"         class="sidenav-item {% if seccion == 'stats'         %}active{% endif %}">Estadisticas</a>
      <a href="/dashboard/?seccion=libros"        class="sidenav-item {% if seccion == 'libros'        %}active{% endif %}">Libros</a>
      <a href="/dashboard/?seccion=eventos"       class="sidenav-item {% if seccion == 'eventos'       %}active{% endif %}">Eventos</a>
      <a href="/dashboard/?seccion=usuarios"      class="sidenav-item {% if seccion == 'usuarios'      %}active{% endif %}">
        Usuarios
        {% if users_pending.count %}<span class="badge-count">{{ users_pending.count }}</span>{% endif %}
      </a>
      <a href="/dashboard/?seccion=resenas"       class="sidenav-item {% if seccion == 'resenas'       %}active{% endif %}">
        Resenas
        {% if pending_reviews_count %}<span class="badge-count">{{ pending_reviews_count }}</span>{% endif %}
      </a>
      <a href="/dashboard/?seccion=integraciones" class="sidenav-item {% if seccion == 'integraciones' %}active{% endif %}">Integraciones</a>
      <a href="/dashboard/?seccion=perfil"        class="sidenav-item {% if seccion == 'perfil'        %}active{% endif %}">Mi perfil</a>
    </div>
  </aside>

  <!-- CONTENT -->
  <div>

    <!-- ── INICIO ── -->
    {% if seccion == 'inicio' %}
    <h2 style="margin-bottom:1.5rem;">Configuracion del club</h2>

    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Identidad y apariencia</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="inicio">
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Nombre del club</label><input class="inp" name="name" value="{{ settings_form.name.value|default:'' }}"></div>
            <div class="field"><label class="lbl">Color principal</label><input type="color" class="inp" name="primary_color" value="{{ settings_form.primary_color.value|default:'#6f42c1' }}" style="padding:4px 6px;height:42px;cursor:pointer;"></div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Descripcion publica</label>
            <textarea class="txa" name="description" rows="3">{{ settings_form.description.value|default:'' }}</textarea>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field">
              <label class="lbl">Logo navbar (rectangular)</label>
              <input class="inp" name="logo_url" value="{{ settings_form.logo_url.value|default:'' }}" placeholder="https://...">
              <p class="inp-hint">Imagen horizontal para la barra de navegacion. Recomendado: PNG transparente, max 300x80px.</p>
            </div>
            <div class="field">
              <label class="lbl">Icono PWA (cuadrado)</label>
              <input class="inp" name="icon_url" value="{{ settings_form.icon_url.value|default:'' }}" placeholder="https://...">
              <p class="inp-hint">Imagen cuadrada 512x512px. Se usa como favicon y como icono al agregar a pantalla de inicio. Si logo navbar esta vacio, se usa aqui tambien.</p>
            </div>
          </div>
          {% if club_settings.nav_logo or club_settings.icon_url %}
          <div style="display:flex;gap:1rem;align-items:flex-start;padding:.875rem 1rem;background:var(--page);border-radius:var(--r);margin-bottom:1rem;">
            {% if club_settings.nav_logo %}
            <div style="text-align:center;">
              <p class="inp-hint" style="margin-bottom:4px;">Logo navbar</p>
              <img src="{{ club_settings.nav_logo }}" alt="logo" style="height:40px;width:auto;object-fit:contain;max-width:160px;">
            </div>
            {% endif %}
            {% if club_settings.icon_url %}
            <div style="text-align:center;">
              <p class="inp-hint" style="margin-bottom:4px;">Icono PWA</p>
              <img src="{{ club_settings.icon_url }}" alt="icono" style="width:48px;height:48px;object-fit:cover;border-radius:10px;">
            </div>
            {% endif %}
          </div>
          {% endif %}
          <button class="btn btn-dark">Guardar identidad</button>
        </form>
      </div>
    </div>

    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Redes sociales del club</span></div>
      <div class="card-body">
        <form action="/integraciones/redes/nueva/" method="post" style="margin-bottom:1rem;">{% csrf_token %}
          <div style="display:grid;grid-template-columns:1fr 2fr auto;gap:.75rem;align-items:end;">
            <div class="field" style="margin-bottom:0;">
              <label class="lbl">Red social</label>
              <input class="inp" name="network" placeholder="Instagram, WhatsApp...">
            </div>
            <div class="field" style="margin-bottom:0;">
              <label class="lbl">URL</label>
              <input class="inp" name="url" type="url" placeholder="https://...">
            </div>
            <button class="btn btn-ghost">Agregar</button>
          </div>
        </form>
        {% if social_links %}
        <div style="border-top:1px solid var(--border);padding-top:.875rem;">
          {% for link in social_links %}
          <div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem 0;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
            <div>
              <span style="font-weight:500;font-size:.875rem;color:var(--ink);">{{ link.network }}</span>
              <a href="{{ link.url }}" target="_blank" rel="noopener" style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ link.url|truncatechars:40 }}</a>
            </div>
            <form action="/integraciones/redes/{{ link.id }}/eliminar/" method="post" style="margin:0;">{% csrf_token %}
              <button class="btn btn-ghost btn-sm" style="color:#8B2020;border-color:#DDD4C8;">Eliminar</button>
            </form>
          </div>
          {% endfor %}
        </div>
        {% else %}
        <p style="font-size:.875rem;color:var(--ink-light);">Sin redes registradas aun.</p>
        {% endif %}
      </div>
    </div>
    {% endif %}

    <!-- ── STATS ── -->
    {% if seccion == 'stats' %}
    <h2 style="margin-bottom:1.5rem;">Estadisticas</h2>
    <div class="g4" style="margin-bottom:1.5rem;">
      <div class="stat"><div class="stat-num">{{ stats.total_books }}</div><div class="stat-lbl">Libros totales</div></div>
      <div class="stat"><div class="stat-num" style="color:var(--green-txt);">{{ stats.books_read }}</div><div class="stat-lbl">Leidos</div></div>
      <div class="stat"><div class="stat-num" style="color:var(--amber);">{{ stats.total_votes }}</div><div class="stat-lbl">Votos emitidos</div></div>
      <div class="stat"><div class="stat-num">{{ stats.approved_users }}</div><div class="stat-lbl">Miembros activos</div></div>
    </div>
    {% if stats.top_voted %}
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Libros mas votados</span></div>
      <div class="card-body" style="padding:0;">
        {% for item in stats.top_voted %}
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div>
            <span style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);">{{ item.title }}</span>
            <span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;font-style:italic;">{{ item.author }}</span>
          </div>
          <span class="chip chip-future">{{ item.vote_count }} voto{{ item.vote_count|pluralize:"s" }}</span>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
    {% if stats.recent_reviews %}
    <div class="card">
      <div class="card-section"><span class="card-section-label">Resenas recientes aprobadas</span></div>
      <div class="card-body" style="padding:0;">
        {% for r in stats.recent_reviews %}
        <div style="padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;">
            <span style="font-family:var(--serif);font-size:.875rem;font-weight:600;color:var(--ink);">{{ r.book.title }}</span>
            <span style="color:#B87333;font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
          </div>
          <p style="font-size:.8125rem;color:var(--ink-light);">{{ r.user.username }} &middot; {{ r.created_at|date:"j M" }}</p>
          <p style="font-size:.875rem;color:var(--ink-mid);margin-top:4px;">{{ r.comment|truncatechars:120 }}</p>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
    {% endif %}

    <!-- ── LIBROS ── -->
    {% if seccion == 'libros' %}
    <h2 style="margin-bottom:1.5rem;">Libros</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Agregar libro</span></div>
      <div class="card-body">
        <form action="/libros/nuevo/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Titulo *</label><input class="inp" name="title" placeholder="Titulo del libro" required></div>
            <div class="field"><label class="lbl">Autor</label><input class="inp" name="author" placeholder="Se busca automaticamente si se deja vacio"></div>
          </div>
          <div class="g3" style="margin-bottom:1rem;">
            <div class="field">
              <label class="lbl">Estado</label>
              <select class="sel" name="status">
                <option value="future">Por leer / En votacion</option>
                <option value="reading">Leyendo ahora</option>
                <option value="completed">Ya lo leimos</option>
              </select>
            </div>
            <div class="field">
              <label class="lbl">Visibilidad</label>
              <select class="sel" name="visibility">
                <option value="public">Publico</option>
                <option value="private">Solo miembros</option>
                <option value="admins">Solo admins</option>
              </select>
            </div>
            <div class="field">
              <label class="lbl">Permitir votos</label>
              <select class="sel" name="allow_voting">
                <option value="True">Si</option>
                <option value="False">No</option>
              </select>
            </div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Descripcion</label>
            <textarea class="txa" name="description" rows="2" placeholder="Se busca automaticamente si se deja vacio"></textarea>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">URL portada</label><input class="inp" name="cover_url" type="url" placeholder="Se busca automaticamente si se deja vacio"></div>
            <div class="field"><label class="lbl">URL Amazon</label><input class="inp" name="amazon_url" type="url" placeholder="Se genera automaticamente con tag de afiliado"></div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field">
              <label class="lbl">URL PDF <span style="font-weight:400;color:var(--ink-light);">(solo visible para miembros activos)</span></label>
              <input class="inp" name="pdf_url" type="url" placeholder="https://...">
            </div>
            <div class="field"><label class="lbl">URL video relacionado</label><input class="inp" name="external_video_url" type="url" placeholder="https://youtube.com/..."></div>
          </div>
          <div style="display:flex;align-items:center;gap:1rem;">
            <button class="btn btn-dark">Guardar libro</button>
            <label style="display:flex;align-items:center;gap:.5rem;font-size:.875rem;color:var(--ink-light);cursor:pointer;">
              <input type="checkbox" name="reemplazar_leyendo_actual" style="accent-color:var(--amber);width:16px;height:16px;">
              Mover libros actuales "Leyendo" a "Leido"
            </label>
          </div>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-section"><span class="card-section-label">Libros registrados</span></div>
      {% for b in books %}
      <div style="border-bottom:{% if not forloop.last %}1px solid var(--border){% else %}none{% endif %};">
        <div style="display:flex;gap:0;">
          {% if b.cover_url %}
          <img src="{{ b.cover_url }}" alt="{{ b.title }}" style="width:52px;height:78px;object-fit:cover;flex-shrink:0;">
          {% else %}
          <div style="width:52px;height:78px;background:var(--page);display:flex;align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;">&#128214;</div>
          {% endif %}
          <div style="flex:1;padding:.875rem 1rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;flex-wrap:wrap;">
              <div>
                <span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ b.title }}</span>
                <span style="font-size:.8125rem;color:var(--ink-light);font-style:italic;margin-left:.5rem;">{{ b.author }}</span>
              </div>
              <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;">
                <span class="chip {% if b.status == 'reading' %}chip-reading{% elif b.status == 'completed' %}chip-done{% else %}chip-future{% endif %}">{{ b.get_status_display }}</span>
                <a href="/libros/{{ b.id }}/" class="btn btn-ghost btn-sm">Ver</a>
                <form action="/libros/{{ b.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar {{ b.title }}?')">{% csrf_token %}
                  <button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button>
                </form>
              </div>
            </div>
            <!-- EDIT FORM INLINE -->
            <details style="margin-top:.75rem;">
              <summary style="font-size:.8125rem;color:var(--amber);cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:4px;">
                &#9998; Editar datos
              </summary>
              <form action="/libros/{{ b.id }}/editar/" method="post" style="margin-top:.75rem;">{% csrf_token %}
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">Titulo</label><input class="inp" name="title" value="{{ b.title }}"></div>
                  <div class="field"><label class="lbl">Autor</label><input class="inp" name="author" value="{{ b.author }}"></div>
                </div>
                <div class="g3" style="margin-bottom:.75rem;">
                  <div class="field">
                    <label class="lbl">Estado</label>
                    <select class="sel" name="status">
                      <option value="future"    {% if b.status == "future"    %}selected{% endif %}>Por leer</option>
                      <option value="reading"   {% if b.status == "reading"   %}selected{% endif %}>Leyendo</option>
                      <option value="completed" {% if b.status == "completed" %}selected{% endif %}>Leido</option>
                    </select>
                  </div>
                  <div class="field">
                    <label class="lbl">Visibilidad</label>
                    <select class="sel" name="visibility">
                      <option value="public"  {% if b.visibility == "public"  %}selected{% endif %}>Publico</option>
                      <option value="private" {% if b.visibility == "private" %}selected{% endif %}>Solo miembros</option>
                      <option value="admins"  {% if b.visibility == "admins"  %}selected{% endif %}>Solo admins</option>
                    </select>
                  </div>
                  <div class="field">
                    <label class="lbl">Votos</label>
                    <select class="sel" name="allow_voting">
                      <option value="True"  {% if b.allow_voting %}selected{% endif %}>Permitidos</option>
                      <option value="False" {% if not b.allow_voting %}selected{% endif %}>Desactivados</option>
                    </select>
                  </div>
                </div>
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">URL portada</label><input class="inp" name="cover_url" value="{{ b.cover_url }}" type="url"></div>
                  <div class="field"><label class="lbl">URL Amazon</label><input class="inp" name="amazon_url" value="{{ b.amazon_url }}" type="url"></div>
                </div>
                <div class="g2" style="margin-bottom:.75rem;">
                  <div class="field"><label class="lbl">URL PDF (solo miembros)</label><input class="inp" name="pdf_url" value="{{ b.pdf_url }}" type="url"></div>
                  <div class="field"><label class="lbl">URL video</label><input class="inp" name="external_video_url" value="{{ b.external_video_url }}" type="url"></div>
                </div>
                <div class="field" style="margin-bottom:.75rem;">
                  <label class="lbl">Descripcion</label>
                  <textarea class="txa" name="description" rows="2">{{ b.description }}</textarea>
                </div>
                <button class="btn btn-dark btn-sm">Guardar cambios</button>
              </form>
            </details>
          </div>
        </div>
      </div>
      {% empty %}
      <div style="padding:2rem 1.5rem;color:var(--ink-light);font-size:.875rem;">Aun no hay libros. Agrega el primero arriba.</div>
      {% endfor %}
    </div>
    {% endif %}

    <!-- ── EVENTOS ── -->
    {% if seccion == 'eventos' %}
    <h2 style="margin-bottom:1.5rem;">Eventos</h2>
    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Agregar evento</span></div>
      <div class="card-body">
        <form action="/eventos/nuevo/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Titulo *</label><input class="inp" name="title" placeholder="Nombre del evento" required></div>
            <div class="field">
              <label class="lbl">Tipo de evento</label>
              <input class="inp" name="event_type" placeholder="Sesion, intercambio, cine, restaurante...">
            </div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Fecha y hora *</label><input class="inp" name="starts_at" type="datetime-local" required></div>
            <div class="field">
              <label class="lbl">Visibilidad</label>
              <select class="sel" name="visibility">
                <option value="public">Publico</option>
                <option value="private">Solo miembros</option>
                <option value="admins">Solo admins</option>
              </select>
            </div>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Lugar</label><input class="inp" name="location" placeholder="Direccion o enlace de videollamada"></div>
            <div class="field"><label class="lbl">Video relacionado</label><input class="inp" name="external_video_url" type="url" placeholder="https://..."></div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Descripcion</label>
            <textarea class="txa" name="description" rows="2" placeholder="Detalles del evento..."></textarea>
          </div>
          <button class="btn btn-dark">Guardar evento</button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-section"><span class="card-section-label">Eventos registrados</span></div>
      {% for e in events_all %}
      <div style="border-bottom:{% if not forloop.last %}1px solid var(--border){% else %}none{% endif %};padding:.875rem 1.5rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;flex-wrap:wrap;">
          <div>
            <span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ e.title }}</span>
            <span class="chip chip-pending" style="margin-left:.5rem;">{{ e.event_type }}</span>
            <div style="font-size:.8125rem;color:var(--ink-light);margin-top:3px;">{{ e.starts_at|date:"j M Y, H:i" }}{% if e.location %} &middot; {{ e.location }}{% endif %}</div>
          </div>
          <form action="/eventos/{{ e.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar este evento?')">{% csrf_token %}
            <button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button>
          </form>
        </div>
        <details style="margin-top:.75rem;">
          <summary style="font-size:.8125rem;color:var(--amber);cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:4px;">&#9998; Editar</summary>
          <form action="/eventos/{{ e.id }}/editar/" method="post" style="margin-top:.75rem;">{% csrf_token %}
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Titulo</label><input class="inp" name="title" value="{{ e.title }}"></div>
              <div class="field"><label class="lbl">Tipo</label><input class="inp" name="event_type" value="{{ e.event_type }}"></div>
            </div>
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Fecha y hora</label><input class="inp" name="starts_at" type="datetime-local" value="{{ e.starts_at|date:'Y-m-d' }}T{{ e.starts_at|date:'H:i' }}"></div>
              <div class="field">
                <label class="lbl">Visibilidad</label>
                <select class="sel" name="visibility">
                  <option value="public"  {% if e.visibility == "public"  %}selected{% endif %}>Publico</option>
                  <option value="private" {% if e.visibility == "private" %}selected{% endif %}>Solo miembros</option>
                  <option value="admins"  {% if e.visibility == "admins"  %}selected{% endif %}>Solo admins</option>
                </select>
              </div>
            </div>
            <div class="g2" style="margin-bottom:.75rem;">
              <div class="field"><label class="lbl">Lugar</label><input class="inp" name="location" value="{{ e.location }}"></div>
              <div class="field"><label class="lbl">Video</label><input class="inp" name="external_video_url" value="{{ e.external_video_url }}" type="url"></div>
            </div>
            <div class="field" style="margin-bottom:.75rem;">
              <label class="lbl">Descripcion</label>
              <textarea class="txa" name="description" rows="2">{{ e.description }}</textarea>
            </div>
            <button class="btn btn-dark btn-sm">Guardar cambios</button>
          </form>
        </details>
      </div>
      {% empty %}
      <div style="padding:2rem 1.5rem;color:var(--ink-light);font-size:.875rem;">Sin eventos registrados aun.</div>
      {% endfor %}
    </div>
    {% endif %}

    <!-- ── USUARIOS ── -->
    {% if seccion == 'usuarios' %}
    <h2 style="margin-bottom:1.5rem;">Usuarios</h2>

    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Invitar usuario</span></div>
      <div class="card-body">
        <form action="/admin/invitar/" method="post">{% csrf_token %}
          <div style="display:grid;grid-template-columns:1fr 1fr 140px auto;gap:.75rem;align-items:end;">
            <div class="field" style="margin-bottom:0;"><label class="lbl">Nombre completo</label><input class="inp" name="name" placeholder="Ana Torres" required></div>
            <div class="field" style="margin-bottom:0;"><label class="lbl">Correo electronico</label><input class="inp" name="email" type="email" placeholder="ana@correo.com" required></div>
            <div class="field" style="margin-bottom:0;">
              <label class="lbl">Rol</label>
              <select class="sel" name="role"><option value="user">Usuario</option><option value="admin">Admin</option></select>
            </div>
            <button class="btn btn-dark" style="margin-bottom:0;">Invitar</button>
          </div>
          <p class="inp-hint" style="margin-top:.5rem;">Se genera una contrasena temporal y se envia por correo (si el servidor de correo esta configurado).</p>
        </form>
      </div>
    </div>

    {% if users_pending %}
    <div class="card" style="margin-bottom:1.25rem;border-color:var(--amber-bdr);">
      <div class="card-section" style="background:var(--amber-bg);border-color:var(--amber-bdr);"><span class="card-section-label">Pendientes de aprobacion ({{ users_pending.count }})</span></div>
      <div class="card-body" style="padding:0;">
        {% for u in users_pending %}
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div>
            <span style="font-weight:500;color:var(--ink);">{{ u.username }}</span>
            <span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">{{ u.email }}</span>
          </div>
          <form action="/usuarios/{{ u.id }}/aprobar/" method="post" style="margin:0;">{% csrf_token %}
            <button class="btn btn-amber btn-sm">Aprobar</button>
          </form>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}

    <div class="card">
      <div class="card-section"><span class="card-section-label">Miembros actuales ({{ users_all|length }})</span></div>
      <div class="card-body" style="padding:0;">
        {% for u in users_all %}
        <div style="padding:.875rem 1.5rem;{% if not forloop.last %}border-bottom:1px solid var(--border);{% endif %}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem;">
            <div>
              <span style="font-weight:500;color:var(--ink);">{{ u.username }}</span>
              <span style="font-size:.75rem;color:var(--ink-light);margin-left:.5rem;">{{ u.role }}</span>
              {% if u.is_approved %}<span class="chip chip-reading" style="margin-left:.5rem;font-size:.625rem;">activo</span>{% else %}<span class="chip chip-pending" style="margin-left:.5rem;font-size:.625rem;">pendiente</span>{% endif %}
            </div>
            <form action="/usuarios/{{ u.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar a {{ u.username }}?')">{% csrf_token %}
              <button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button>
            </form>
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

    <!-- ── RESENAS ── -->
    {% if seccion == 'resenas' %}
    <h2 style="margin-bottom:1.5rem;">Moderacion de resenas</h2>
    {% for r in reviews_all %}
    <div class="card" style="margin-bottom:1rem;">
      <div class="card-body">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem;">
          <div>
            <span style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);">{{ r.book.title }}</span>
            <span style="font-size:.8125rem;color:var(--ink-light);margin-left:.5rem;">por {{ r.user.username }}</span>
          </div>
          <div style="display:flex;align-items:center;gap:.5rem;">
            <span style="color:#B87333;font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= r.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
            {% if r.is_approved %}<span class="chip chip-reading" style="font-size:.625rem;">Aprobada</span>
            {% elif r.is_flagged %}<span class="chip chip-future" style="font-size:.625rem;">Marcada</span>
            {% else %}<span class="chip chip-pending" style="font-size:.625rem;">Pendiente</span>{% endif %}
          </div>
        </div>
        <p style="font-size:.9375rem;color:var(--ink-mid);margin-bottom:1rem;line-height:1.55;">{{ r.comment }}</p>
        <div style="display:flex;gap:.75rem;flex-wrap:wrap;align-items:center;">
          <form action="/resenas/{{ r.id }}/aprobar/" method="post" style="margin:0;display:flex;gap:.5rem;align-items:center;">
            {% csrf_token %}
            <input class="inp" name="moderation_note" placeholder="Nota opcional" style="width:180px;font-size:.8125rem;padding:6px 10px;">
            <button class="btn btn-amber btn-sm">Aprobar</button>
          </form>
          <form action="/resenas/{{ r.id }}/marcar/" method="post" style="margin:0;display:flex;gap:.5rem;align-items:center;">
            {% csrf_token %}
            <input class="inp" name="moderation_note" placeholder="Motivo del rechazo" required style="width:180px;font-size:.8125rem;padding:6px 10px;">
            <button class="btn btn-ghost btn-sm">Marcar</button>
          </form>
          <form action="/resenas/{{ r.id }}/eliminar/" method="post" style="margin:0;" onsubmit="return confirm('Eliminar esta resena?')">
            {% csrf_token %}<button class="btn btn-ghost btn-sm" style="color:#8B2020;">Eliminar</button>
          </form>
        </div>
      </div>
    </div>
    {% empty %}
    <div class="card card-body" style="color:var(--ink-light);">No hay resenas por moderar.</div>
    {% endfor %}
    {% endif %}

    <!-- ── INTEGRACIONES ── -->
    {% if seccion == 'integraciones' %}
    <h2 style="margin-bottom:1.5rem;">Integraciones</h2>

    <div class="card" style="margin-bottom:1.25rem;">
      <div class="card-section"><span class="card-section-label">Amazon afiliados</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div style="max-width:420px;">
            <div class="field">
              <label class="lbl">Tag de afiliado Amazon</label>
              <input class="inp" name="affiliate_tag" value="{{ settings_form.affiliate_tag.value|default:'' }}" placeholder="tu-tag-20">
              <p class="inp-hint">
                Si este campo esta vacio se usa el tag del sistema por defecto
                (<strong>{{ default_affiliate_tag }}</strong>).
                Los enlaces de Amazon en todos los libros se actualizan automaticamente.
              </p>
            </div>
          </div>
          <button class="btn btn-dark" style="margin-top:.5rem;">Guardar</button>
        </form>
      </div>
    </div>

    {% if settings_form.google_login_enabled %}
    <div class="card">
      <div class="card-section"><span class="card-section-label">Google OAuth (inicio de sesion)</span></div>
      <div class="card-body">
        <form action="/dashboard/configuracion/" method="post">{% csrf_token %}
          <input type="hidden" name="seccion" value="integraciones">
          <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;padding:.75rem 1rem;background:var(--page);border-radius:var(--r);">
            <input type="checkbox" id="google_enabled" name="google_login_enabled" {% if settings_form.google_login_enabled.value %}checked{% endif %} style="width:18px;height:18px;accent-color:var(--amber);cursor:pointer;">
            <label for="google_enabled" style="font-size:.875rem;color:var(--ink);cursor:pointer;">Habilitar inicio de sesion con Google</label>
          </div>
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Google Client ID</label><input class="inp" name="google_client_id" value="{{ settings_form.google_client_id.value|default:'' }}" placeholder="xxxx.apps.googleusercontent.com"></div>
            <div class="field"><label class="lbl">Google Client Secret</label><input class="inp" name="google_client_secret" value="{{ settings_form.google_client_secret.value|default:'' }}" type="password" placeholder="GOCSPX-..."></div>
          </div>
          <p class="inp-hint" style="margin-bottom:1rem;">Redirect URI para Google Cloud Console: <code style="background:var(--page);padding:2px 6px;border-radius:4px;">{{ request.scheme }}://{{ request.get_host }}/accounts/google/login/callback/</code></p>
          <button class="btn btn-dark">Guardar Google OAuth</button>
        </form>
      </div>
    </div>
    {% endif %}
    {% endif %}

    <!-- ── PERFIL ── -->
    {% if seccion == 'perfil' %}
    <h2 style="margin-bottom:1.5rem;">Mi perfil</h2>
    <div class="card" style="max-width:560px;">
      <div class="card-section"><span class="card-section-label">Datos personales</span></div>
      <div class="card-body">
        <form action="/perfil/editar/" method="post">{% csrf_token %}
          <div class="g2" style="margin-bottom:1rem;">
            <div class="field"><label class="lbl">Nombre completo</label><input class="inp" name="full_name" value="{{ user.full_name }}"></div>
            <div class="field"><label class="lbl">Correo electronico</label><input class="inp" name="email" type="email" value="{{ user.email }}"></div>
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Libro favorito</label>
            <input class="inp" name="favorite_book" value="{{ user.favorite_book }}" placeholder="El libro que mas te ha marcado">
          </div>
          <div class="field" style="margin-bottom:1rem;">
            <label class="lbl">Biografia / Presentacion</label>
            <textarea class="txa" name="bio" rows="3" placeholder="Cuentanos un poco de ti como lector...">{{ user.bio }}</textarea>
          </div>
          <div class="field" style="margin-bottom:1.25rem;">
            <label class="lbl">URL de tu foto de perfil</label>
            <input class="inp" name="avatar_url" type="url" value="{{ user.avatar_url }}" placeholder="https://...">
            {% if user.avatar_url %}
            <div style="margin-top:.75rem;display:flex;align-items:center;gap:.75rem;">
              <img src="{{ user.avatar_url }}" alt="avatar" style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid var(--border);">
              <span class="inp-hint">Foto actual</span>
            </div>
            {% endif %}
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
# HOME
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/home.html"] = """{% extends 'base.html' %}
{% block content %}
<section style="padding:1.5rem 0 2rem;">
  <p style="font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:.5rem;">Bienvenido</p>
  <h1 style="font-size:2rem;margin-bottom:.375rem;">{{ club_settings.name }}</h1>
  {% if club_settings.description %}<p style="color:var(--ink-light);max-width:520px;font-size:.9375rem;">{{ club_settings.description }}</p>{% endif %}
</section>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem;max-width:600px;margin-bottom:2rem;">
  <div class="card card-body">
    <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.375rem;">Leyendo ahora</p>
    {% if current_book %}
      <p style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);font-weight:600;margin-bottom:2px;">{{ current_book.title }}</p>
      <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;">{{ current_book.author }}</p>
    {% else %}<p style="font-size:.875rem;color:var(--ink-light);">Sin libro activo</p>{% endif %}
  </div>
  <div class="card card-body">
    <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.375rem;">Proximo evento</p>
    {% if next_event %}
      <p style="font-family:var(--serif);font-size:.9375rem;color:var(--ink);font-weight:600;margin-bottom:2px;">{{ next_event.title }}</p>
      <p style="font-size:.8125rem;color:var(--ink-light);">{{ next_event.starts_at|date:"j M, H:i" }}</p>
    {% else %}<p style="font-size:.875rem;color:var(--ink-light);">Sin eventos proximos</p>{% endif %}
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 300px;gap:2rem;">
  <div>
    <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:1rem;">Biblioteca del club</p>
    {% for book in books %}
    <div class="card" style="margin-bottom:.875rem;display:flex;">
      {% if book.cover_url %}
        <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:72px;height:108px;object-fit:cover;flex-shrink:0;border-radius:14px 0 0 14px;">
      {% else %}
        <div style="width:72px;height:108px;background:var(--page);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">&#128214;</div>
      {% endif %}
      <div style="flex:1;padding:1rem 1.125rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;margin-bottom:.375rem;">
          <div>
            <h3 style="font-size:.9375rem;margin-bottom:2px;">{{ book.title }}</h3>
            <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;">{{ book.author }}</p>
          </div>
          <span class="chip {% if book.status == 'reading' %}chip-reading{% elif book.status == 'completed' %}chip-done{% else %}chip-future{% endif %}">{{ book.get_status_display }}</span>
        </div>
        {% if book.status == 'future' and book.allow_voting %}
        <div style="background:var(--amber-bg);border:1px solid var(--amber-bdr);border-radius:var(--r);padding:.5rem .75rem;margin:.5rem 0;font-size:.8125rem;color:#7A4F15;">
          Votacion abierta &middot; {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}
        </div>
        {% endif %}
        <div style="display:flex;gap:.75rem;align-items:center;margin-top:.5rem;flex-wrap:wrap;">
          <a href="/libros/{{ book.id }}/" class="btn btn-ghost btn-sm">Ver detalle</a>
          {% if book.amazon_url %}<a href="{{ book.amazon_url }}" target="_blank" rel="noopener" style="font-size:.8125rem;color:var(--ink-light);">Amazon &#8599;</a>{% endif %}
          {% if book.pdf_url and user.is_authenticated and user.is_approved or book.pdf_url and user.is_superuser %}<a href="{{ book.pdf_url }}" target="_blank" style="font-size:.8125rem;color:var(--ink-light);">PDF &#8599;</a>{% endif %}
        </div>
        {% with approved=book.reviews.all %}{% if approved %}
        <div style="margin-top:.75rem;padding-top:.75rem;border-top:1px solid var(--border);">
          {% for review in approved %}{% if review.is_approved %}
          <p style="font-size:.8125rem;color:var(--ink-light);line-height:1.5;">
            <span style="color:#B87333;">{% for i in "12345" %}{% if forloop.counter <= review.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
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
      <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.875rem;">Proximos eventos</p>
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
      <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.75rem;">Redes del club</p>
      {% for link in links %}
      <a href="{{ link.url }}" target="_blank" rel="noopener" style="display:block;font-size:.875rem;color:var(--ink-light);padding:3px 0;text-decoration:none;">&#8599; {{ link.network }}</a>
      {% endfor %}
    </div>
    {% endif %}
    <button class="btn btn-ghost" style="width:100%;" onclick="navigator.share ? navigator.share({title:document.title,url:location.href}) : alert('Comparte: '+location.href)">Compartir club</button>
  </aside>
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# BOOKS PAGE
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/books_page.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;">
  <div>
    <p style="font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:.25rem;">Biblioteca</p>
    <h1 style="font-size:1.75rem;">Libros del club</h1>
  </div>
</div>
<form method="get" action="/libros/" style="display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:2rem;">
  <input type="text" name="q" value="{{ query|default:'' }}" class="inp" placeholder="Buscar por titulo o autor..." style="max-width:280px;width:100%;">
  <select name="estado" class="sel" style="max-width:170px;width:100%;" onchange="this.form.submit()">
    <option value="">Todos los estados</option>
    <option value="completed" {% if estado == 'completed' %}selected{% endif %}>Leidos</option>
    <option value="reading"   {% if estado == 'reading'   %}selected{% endif %}>Leyendo</option>
    <option value="future"    {% if estado == 'future'    %}selected{% endif %}>En votacion</option>
  </select>
  <button class="btn btn-dark" type="submit">Buscar</button>
  {% if query or estado %}<a href="/libros/" class="btn btn-ghost">Limpiar</a>{% endif %}
</form>
{% for book in books %}
<a href="/libros/{{ book.id }}/" style="display:block;text-decoration:none;margin-bottom:.75rem;">
  <div class="card" style="{% if book.status == 'future' and book.allow_voting %}border-color:var(--amber-bdr);{% endif %}transition:box-shadow .15s;" onmouseover="this.style.boxShadow='0 4px 16px rgba(26,15,10,.07)'" onmouseout="this.style.boxShadow=''">
    {% if book.status == 'future' and book.allow_voting %}
    <div style="background:var(--amber-bg);border-bottom:1px solid var(--amber-bdr);padding:.375rem 1.25rem;font-size:.75rem;color:#7A4F15;display:flex;align-items:center;gap:.5rem;">
      <span>&#128717;</span> <strong>Votacion abierta</strong> &mdash; {{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }} &middot; Entra para votar
    </div>
    {% endif %}
    <div style="display:flex;align-items:center;gap:0;">
      {% if book.cover_url %}
        <img src="{{ book.cover_url }}" alt="{{ book.title }}" style="width:48px;height:72px;object-fit:cover;flex-shrink:0;{% if book.status != 'future' or not book.allow_voting %}border-radius:14px 0 0 14px;{% endif %}">
      {% else %}
        <div style="width:48px;height:72px;background:var(--page);display:flex;align-items:center;justify-content:center;font-size:1.25rem;flex-shrink:0;">&#128214;</div>
      {% endif %}
      <div style="flex:1;padding:.875rem 1.125rem;display:flex;justify-content:space-between;align-items:center;gap:.75rem;">
        <div>
          <p style="font-family:var(--serif);font-size:.9375rem;font-weight:600;color:var(--ink);margin-bottom:2px;">{{ book.title }}</p>
          <p style="font-size:.8125rem;color:var(--ink-light);font-style:italic;margin:0;">{{ book.author }}</p>
        </div>
        <span class="chip {% if book.status == 'reading' %}chip-reading{% elif book.status == 'completed' %}chip-done{% else %}chip-future{% endif %}">{{ book.get_status_display }}</span>
      </div>
    </div>
  </div>
</a>
{% empty %}
<p style="color:var(--ink-light);padding:2rem 0;">No se encontraron libros con estos filtros.</p>
{% endfor %}
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
      <div style="width:100%;aspect-ratio:2/3;background:var(--page);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:3rem;max-width:200px;">&#128214;</div>
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
        {% if user.is_authenticated and user.is_approved or user.is_superuser %}
          <a href="{{ book.pdf_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Descargar PDF &#8599;</a>
        {% endif %}
      {% endif %}
    </div>

    {% if book.status == 'future' and book.allow_voting %}
    <div style="background:var(--amber-bg);border:1px solid var(--amber-bdr);border-radius:12px;padding:1.25rem 1.5rem;max-width:460px;">
      <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.5rem;">Votacion abierta</p>
      <p style="font-family:var(--serif);font-size:1.0625rem;color:var(--ink);margin-bottom:.375rem;">Quieres que leamos este libro?</p>
      <p style="font-size:.875rem;color:var(--ink-light);margin-bottom:1rem;">Puedes votar por todos los libros que quieras. El mas votado sera el proximo.</p>
      <p style="font-size:1.5rem;font-family:var(--serif);font-weight:600;color:var(--amber);margin-bottom:.875rem;">{{ book.votes.count }} voto{{ book.votes.count|pluralize:"s" }}</p>
      {% if user_vote %}
        <p style="font-size:.9375rem;color:var(--green-txt);">&#10003; Ya votaste por este libro</p>
      {% elif user.is_authenticated %}
        {% if user.is_approved or user.is_superuser %}
        <form action="/libros/{{ book.id }}/votar/" method="post">{% csrf_token %}
          <input type="hidden" name="next" value="/libros/{{ book.id }}/">
          <button class="btn btn-amber">Votar por este libro</button>
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
    <p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:1rem;">Resenas</p>
    {% for review in approved_reviews %}
    <div class="card card-body" style="margin-bottom:.875rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.375rem;">
        <strong style="font-size:.9375rem;color:var(--ink);">{{ review.user.username }}</strong>
        <span style="color:#B87333;font-size:.875rem;">{% for i in "12345" %}{% if forloop.counter <= review.rating %}&#9733;{% else %}&#9734;{% endif %}{% endfor %}</span>
      </div>
      <p style="font-size:.9375rem;color:var(--ink-mid);line-height:1.6;margin-bottom:.375rem;">{{ review.comment }}</p>
      <p style="font-size:.75rem;color:var(--ink-light);">{{ review.created_at|date:"j M Y" }}</p>
    </div>
    {% empty %}
    <p style="color:var(--ink-light);">Aun no hay resenas aprobadas.</p>
    {% endfor %}
  </div>

  {% if user.is_authenticated %}{% if user.is_approved or user.is_superuser %}
  <div>
    <div class="card" style="background:var(--page);">
      <div class="card-section"><span class="card-section-label">Escribe tu resena</span></div>
      <div class="card-body">
        <form action="/libros/{{ book.id }}/resena/" method="post">{% csrf_token %}
          <div class="field">
            <label class="lbl">Calificacion</label>
            <select name="rating" class="sel">
              <option value="5">&#9733;&#9733;&#9733;&#9733;&#9733; Excelente</option>
              <option value="4">&#9733;&#9733;&#9733;&#9733;&#9734; Muy bueno</option>
              <option value="3">&#9733;&#9733;&#9733;&#9734;&#9734; Bueno</option>
              <option value="2">&#9733;&#9733;&#9734;&#9734;&#9734; Regular</option>
              <option value="1">&#9733;&#9734;&#9734;&#9734;&#9734; No me gusto</option>
            </select>
          </div>
          <div class="field">
            <label class="lbl">Tu comentario</label>
            <textarea name="comment" class="txa" rows="4" placeholder="Que te parecio el libro?" required></textarea>
          </div>
          <button class="btn btn-dark">Enviar resena</button>
          <p class="inp-hint" style="margin-top:.5rem;">Pasa por moderacion antes de publicarse.</p>
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
<p style="font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:.375rem;">Agenda</p>
<h1 style="font-size:1.75rem;margin-bottom:2rem;">Eventos del club</h1>
<p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.875rem;">Proximos</p>
{% for e in upcoming %}
<div class="card card-body" style="margin-bottom:.875rem;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap;">
    <div>
      <h3 style="font-size:1.0625rem;margin-bottom:.25rem;">{{ e.title }}</h3>
      <p style="font-size:.8125rem;color:var(--ink-light);">
        <span class="chip chip-pending" style="margin-right:.375rem;">{{ e.event_type }}</span>
        {{ e.starts_at|date:"j M Y, H:i" }}
        {% if e.location %} &middot; {{ e.location }}{% endif %}
      </p>
      {% if e.description %}<p style="font-size:.9375rem;color:var(--ink-mid);margin-top:.5rem;line-height:1.6;">{{ e.description }}</p>{% endif %}
    </div>
    {% if e.external_video_url %}<a href="{{ e.external_video_url }}" class="btn btn-ghost btn-sm" target="_blank" rel="noopener">Ver video &#8599;</a>{% endif %}
  </div>
</div>
{% empty %}<p style="color:var(--ink-light);margin-bottom:1.5rem;">Sin eventos proximos.</p>{% endfor %}
<hr style="border:none;border-top:1px solid var(--border);margin:1.5rem 0;">
<p style="font-size:.6875rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.875rem;">Pasados</p>
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
# LOGIN
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/auth/login.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:400px;margin:2rem auto;">
  <p style="font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:.375rem;">Acceso</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">Entrar al club</h1>
  <div class="card card-body">
    <form method="post">{% csrf_token %}{{ form.as_p }}
      <button class="btn btn-dark" style="width:100%;margin-top:.5rem;">Entrar</button>
    </form>
    {% if club_settings.google_login_enabled and club_settings.google_client_id and club_settings.google_client_secret %}
    <div style="display:flex;align-items:center;gap:.75rem;margin:1rem 0;">
      <div style="flex:1;height:1px;background:var(--border);"></div>
      <span style="font-size:.8125rem;color:var(--ink-light);">o</span>
      <div style="flex:1;height:1px;background:var(--border);"></div>
    </div>
    <a href="/accounts/google/login/" class="btn btn-ghost" style="width:100%;text-align:center;display:block;">Entrar con Google</a>
    {% endif %}
  </div>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);margin-top:1.25rem;">No tienes cuenta? <a href="/registro/" style="color:var(--ink);font-weight:500;">Registrate</a></p>
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# REGISTER
# ══════════════════════════════════════════════════════════════
T[f"{BASE}/auth/register.html"] = """{% extends 'base.html' %}
{% block content %}
<div style="max-width:440px;margin:2rem auto;">
  <p style="font-size:.6875rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:.375rem;">Unete</p>
  <h1 style="font-size:1.5rem;margin-bottom:1.5rem;">Crear cuenta</h1>
  <div class="card card-body">
    <form method="post">{% csrf_token %}{{ form.as_p }}
      <button class="btn btn-dark" style="width:100%;margin-top:.5rem;">Crear cuenta</button>
    </form>
  </div>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);margin-top:1rem;">Tu cuenta quedara pendiente de aprobacion por un administrador.</p>
  <p style="text-align:center;font-size:.875rem;color:var(--ink-light);">Ya tienes cuenta? <a href="/login/" style="color:var(--ink);font-weight:500;">Entrar</a></p>
</div>
{% endblock %}"""

# ══════════════════════════════════════════════════════════════
# ESCRIBIR ARCHIVOS
# ══════════════════════════════════════════════════════════════
for path, content in T.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"OK  {path}")

print("\nTodos los templates escritos correctamente.")
print("Recarga el navegador - no necesitas hacer rebuild.")