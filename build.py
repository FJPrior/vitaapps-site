#!/usr/bin/env python3
"""Genera el sitio estático de vitaapps.io.

Fuente de los textos legales (privacy-policy.md y support.md):
  Lumos Wallet: ../Budget/docs/
  Argo:    _docs/argo/ (Jekyll no publica carpetas que empiezan con _)
Uso:  python3 build.py   (luego commit + push desde GitHub Desktop)
"""
import datetime
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
YEAR = datetime.date.today().year
EMAIL = "support@vitaapps.io"

# Cada app tiene su ruta, sus textos legales y su color. Lumos usa el azul base del CSS.
APPS = {
    "lumos": {
        "name": "Lumos Wallet",
        "path": "/lumos-wallet/",
        "docs": ROOT.parent / "Budget" / "docs",
        "og_image": "lumos-icon.png",
        "css": "",
    },
    "argo": {
        "name": "Argo",
        "path": "/argo/",
        "docs": ROOT / "_docs" / "argo",
        "og_image": "argo-og.png",
        # Turquesa de Argo (#0A8FA8), un poco más oscuro en texto y botones para que se lea bien.
        "css": ":root{--accent:#077c92;--accent-soft:#e1f3f6;--accent-ink:#fff}"
               "@media (prefers-color-scheme:dark){:root{--accent:#3cc3d9;--accent-soft:#0f2a30;--accent-ink:#03222a}}"
               ".hero-mark{width:min(240px,56vw);margin:0 auto;border-radius:22.5%;box-shadow:0 30px 60px -20px rgba(8,80,96,.35)}\n",
    },
}

# ---------------------------------------------------------------- markdown mínimo

def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w/\">])([\w.+-]+@[\w-]+\.[\w.]+\w)", r'<a href="mailto:\1">\1</a>', text)
    return text


def markdown(md):
    """Encabezados, párrafos, listas, negritas y enlaces. Un párrafo que empieza con una
    línea en negritas sola ("**¿Pregunta?**" + respuesta) se vuelve una pregunta frecuente."""
    out, title = [], ""
    for block in re.split(r"\n\s*\n", md.strip()):
        lines = block.strip().split("\n")
        first = lines[0]
        if first.startswith("# "):
            title = first[2:].strip()
            continue
        if first.startswith("## "):
            text = first[3:].strip()
            anchor = re.sub(r"[^a-z0-9áéíóúñü]+", "-", text.lower()).strip("-")
            out.append(f'<h2 id="{anchor}">{inline(text)}</h2>')
            continue
        if all(l.startswith("- ") for l in lines):
            items = "".join(f"<li>{inline(l[2:])}</li>" for l in lines)
            out.append(f"<ul>{items}</ul>")
            continue
        m = re.fullmatch(r"\*\*(.+)\*\*", first)
        if m and len(lines) > 1:
            answer = inline(" ".join(lines[1:]))
            out.append(f'<details class="faq"><summary>{inline(m.group(1))}</summary><p>{answer}</p></details>')
            continue
        out.append(f"<p>{inline(' '.join(lines))}</p>")
    return title, "\n".join(out)

# ---------------------------------------------------------------- plantilla

CSS = """
:root{--bg:#f5f6f8;--surface:#fff;--fg:#14161a;--muted:#5f6571;--line:#e3e6eb;--accent:#1c69ee;--accent-soft:#e8f0fe;--accent-ink:#fff;--radius:20px;--shadow:0 1px 2px rgba(16,24,40,.04),0 8px 24px rgba(16,24,40,.06)}
@media (prefers-color-scheme:dark){:root{--bg:#0b0c0f;--surface:#15171c;--fg:#f2f3f5;--muted:#9aa1ad;--line:#262a31;--accent:#5b9bff;--accent-soft:#16233b;--accent-ink:#06142b;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.site{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:saturate(180%) blur(16px);-webkit-backdrop-filter:saturate(180%) blur(16px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.brand{display:flex;align-items:center;gap:10px;color:var(--fg);font-weight:700;letter-spacing:-.01em}
.brand:hover{text-decoration:none}
.brand-mark{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#08baf4,#2152d9);display:grid;place-items:center;color:#fff;font-size:15px;font-weight:800}
nav.site a{color:var(--muted);margin-left:22px;font-size:15px}
nav.site a:hover,nav.site a[aria-current]{color:var(--fg);text-decoration:none}
h1,h2,h3{letter-spacing:-.02em;line-height:1.15}
.hero{padding:88px 0 56px}
.hero h1{font-size:clamp(2.4rem,6vw,4rem);margin:0 0 18px;font-weight:800}
.lead{font-size:clamp(1.1rem,2.2vw,1.35rem);color:var(--muted);max-width:640px;margin:0}
.eyebrow{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-bottom:14px}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-weight:600;font-size:16px;border:1px solid var(--line);background:var(--surface);color:var(--fg)}
.btn:hover{text-decoration:none;border-color:var(--muted)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.primary:hover{filter:brightness(1.07)}
.pill{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-weight:600;font-size:14px}
.pill::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
section{padding:56px 0}
section h2{font-size:clamp(1.7rem,3.6vw,2.4rem);margin:0 0 12px}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:32px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:26px;box-shadow:var(--shadow)}
.card h3{font-size:1.15rem;margin:14px 0 6px}
.card p{margin:0;color:var(--muted);font-size:16px}
.ico{width:44px;height:44px;border-radius:12px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center}
.ico svg{width:24px;height:24px}
.app-card{display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.app-card img{width:96px;height:96px;border-radius:22px;box-shadow:var(--shadow)}
.app-card .txt{flex:1;min-width:220px}
.app-card h3{margin:0 0 4px;font-size:1.5rem}
.app-card+.app-card{margin-top:18px}
.split{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
@media (max-width:820px){.split{grid-template-columns:1fr}.hero{padding-top:56px}}
.app-id{display:flex;align-items:center;gap:16px;margin-bottom:22px}
.app-id img{width:72px;height:72px;border-radius:17px;box-shadow:var(--shadow)}
.app-id strong{display:block;font-size:1.25rem}
.app-id span{color:var(--muted);font-size:15px}
.phone{position:relative;width:min(320px,80vw);margin:0 auto;border-radius:52px;padding:12px;background:#0d0e11;box-shadow:0 30px 60px -20px rgba(16,24,40,.35),0 0 0 2px #2a2d33 inset}
.phone img{border-radius:42px;width:100%}
.glow{position:absolute;inset:-40px -60px;z-index:-1;background:radial-gradient(closest-side,color-mix(in srgb,var(--accent) 28%,transparent),transparent);filter:blur(10px)}
main{overflow-x:clip}
.band{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.checks{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.checks li{display:flex;gap:12px;align-items:flex-start}
.checks li::before{content:"✓";flex:none;width:26px;height:26px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-weight:700;font-size:14px;margin-top:2px}
.cta{text-align:center}
.cta p{color:var(--muted);max-width:560px;margin:0 auto}
.cta .btns{justify-content:center}
.doc{max-width:760px;padding:56px 20px 72px}
.doc .back{font-size:15px;color:var(--muted)}
.doc h1{font-size:clamp(2rem,5vw,2.8rem);margin:14px 0 8px}
.doc .meta{color:var(--muted);margin:0 0 28px}
.doc h2{font-size:1.35rem;margin:40px 0 10px;padding-top:8px}
.doc p,.doc li{color:var(--fg)}
.doc ul{padding-left:22px}
.doc li{margin:8px 0}
.doc .intro p{margin:0}
.doc .intro{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px 24px;box-shadow:var(--shadow)}
.contact{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;background:var(--accent-soft);border-radius:var(--radius);padding:22px 24px;margin:8px 0 32px}
.contact p{margin:0}
.faq{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:0 20px;margin:12px 0;box-shadow:var(--shadow)}
.faq summary{cursor:pointer;list-style:none;padding:18px 28px 18px 0;font-weight:600;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:0;top:14px;font-size:22px;color:var(--muted);font-weight:400}
.faq[open] summary::after{content:"−"}
.faq p{margin:0 0 18px;color:var(--muted)}
footer.site{border-top:1px solid var(--line);padding:32px 0 44px;color:var(--muted);font-size:14px}
footer.site .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer.site a{color:var(--muted);margin-left:18px}
footer.site a:first-child{margin-left:0}
@media (max-width:520px){nav.site a{margin-left:14px;font-size:14px}.hide-sm{display:none}}
"""


def page(path, title, description, body, doc=False, app="lumos"):
    a = APPS[app]
    # "Soporte" lleva al soporte de la app en la que estás; en celular se oculta (está en el pie).
    nav_items = [(APPS["lumos"]["path"], "Lumos Wallet", ""), (APPS["argo"]["path"], "Argo", ""),
                 (a["path"] + "soporte/", "Soporte", ' class="hide-sm"')]
    nav = "".join(
        f'<a href="{href}"{cls}{" aria-current=page" if href == path else ""}>{label}</a>' for href, label, cls in nav_items
    )
    main = f'<main class="wrap doc">{body}</main>' if doc else f"<main>{body}</main>"
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://vitaapps.io/assets/{a["og_image"]}">
<link rel="canonical" href="https://vitaapps.io{path}">
<link rel="icon" href="/assets/apple-touch-icon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#f5f6f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0c0f" media="(prefers-color-scheme: dark)">
<style>{CSS}{a["css"]}</style>
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/"><span class="brand-mark">V</span>Vita Apps</a>
<nav class="site">{nav}</nav>
</div></header>
{main}
<footer class="site"><div class="wrap">
<span>© {YEAR} Vita Apps</span>
<span><a href="{a["path"]}privacidad/">Privacidad</a><a href="{a["path"]}soporte/">Soporte</a><a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
</body>
</html>
"""

# ---------------------------------------------------------------- íconos (trazos simples)

def icon(d):
    return f'<span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg></span>'

I_GAUGE = '<path d="M12 14l4-4"/><path d="M3.3 17a9 9 0 1 1 17.4 0"/>'
I_JAR = '<path d="M8 3h8M9 3v3.5L6 9v10a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V9l-3-2.5V3"/><path d="M6 14h12"/>'
I_BOLT = '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'
I_CAL = '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 10h18"/>'
I_PIE = '<path d="M21 12A9 9 0 1 1 12 3v9z"/><path d="M15 3.5A9 9 0 0 1 20.5 9H15z"/>'
I_LOCK = '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
I_EYE = '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'
I_HEART = '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>'
I_PIN = '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'
I_USERS = '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.2a6.5 6.5 0 0 1 3.5 5.8"/>'
I_MERGE = '<path d="M3 5c6 0 7 7 13 7h5"/><path d="M3 19c6 0 7-7 13-7"/><path d="M18 9l3 3-3 3"/>'
I_CASH = '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>'
I_REPEAT = '<path d="M17 2l4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>'
I_CHART = '<path d="M3 3v18h18"/><path d="M8 17v-4M12 17V8M16 17v-6M20 17V5"/>'
I_BELL = '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'
I_LINK = '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'

I_SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'
I_TICKET = '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/><path d="M13 5v2M13 11v2M13 17v2"/>'
I_VOTE = '<path d="M9 12l2 2 4-4"/><path d="M5 7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v12H5z"/><path d="M22 19H2"/>'
I_BAG = '<path d="M6 20a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2"/><path d="M8 18V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v14"/><path d="M10 20h4"/><circle cx="16" cy="20" r="2"/><circle cx="8" cy="20" r="2"/>'
I_BED = '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M12 4v6M2 18h20"/>'
I_GLOBE = '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
I_TASKS = '<path d="M3 17l2 2 4-4"/><path d="M3 7l2 2 4-4"/><path d="M13 6h8M13 12h8M13 18h8"/>'

def cards(items):
    return '<div class="grid">' + "".join(
        f'<div class="card">{icon(i)}<h3>{t}</h3><p>{p}</p></div>' for i, t, p in items
    ) + "</div>"

# ---------------------------------------------------------------- páginas

def landing():
    body = f"""
<div class="wrap">
<section class="hero">
<span class="eyebrow">Vita Apps</span>
<h1>Apps sencillas para<br>un día a día más claro.</h1>
<p class="lead">Hacemos apps para iPhone pensadas en México: pocas pantallas, números que se entienden y tu información siempre bajo tu control.</p>
<div class="btns"><a class="btn primary" href="/lumos-wallet/">Conoce Lumos Wallet</a><a class="btn" href="mailto:{EMAIL}">Escríbenos</a></div>
</section>

<section>
<span class="eyebrow">Nuestras apps</span>
<div class="card app-card">
<img src="/assets/lumos-icon.png" alt="Ícono de Lumos Wallet" width="96" height="96">
<div class="txt"><h3>Lumos Wallet</h3><p>Tu presupuesto personal en un solo número: lo que de verdad puedes gastar este mes, sin tocar tus pagos fijos ni tus metas.</p></div>
<a class="btn primary" href="/lumos-wallet/">Ver la app</a>
</div>
<div class="card app-card">
<img src="/assets/argo-icon.png" alt="Ícono de Argo" width="96" height="96">
<div class="txt"><h3>Argo</h3><p>Viajes y gastos en grupo: planeen el itinerario, voten, armen la maleta y lleven la cuenta de quién pagó y quién le debe a quién, al centavo. También para el depa o tu pareja.</p><p style="margin-top:12px"><span class="pill">Próximamente</span></p></div>
<a class="btn primary" href="/argo/">Ver la app</a>
</div>
</section>

<section>
<span class="eyebrow">Cómo trabajamos</span>
<h2>Lo que puedes esperar de nosotros</h2>
{cards([
    (I_EYE, "Claridad", "Cada número se puede explicar. Si la app te dice algo, puedes tocarlo y ver de dónde sale."),
    (I_LOCK, "Privacidad", "Sin publicidad y sin rastreo. No vendemos tu información y puedes borrarla cuando quieras."),
    (I_PIN, "Hechas para México", "Quincenas, meses sin intereses, fechas de corte: pensadas para cómo se usa el dinero aquí."),
])}
</section>
</div>
"""
    return page("/", "Vita Apps · Apps sencillas para iPhone",
                "Vita Apps hace apps para iPhone pensadas en México. Conoce Lumos Wallet, tu presupuesto personal claro, y Argo, para planear viajes y dividir gastos en grupo.", body)


def product():
    body = f"""
<div class="wrap">
<section class="hero split">
<div>
<div class="app-id"><img src="/assets/lumos-icon.png" alt="" width="72" height="72"><div><strong>Lumos Wallet</strong><span>Finanzas · iPhone</span></div></div>
<h1>¿Cuánto te queda para gastar este mes?</h1>
<p class="lead">Lumos Wallet junta tus cuentas, tu quincena y tus pagos fijos en un solo número: tu <strong>Libre</strong>, o sea, lo que de verdad te queda para gastar.</p>
<div class="btns"><span class="pill">Muy pronto en la App Store</span></div>
</div>
<div style="position:relative"><div class="glow"></div><div class="phone"><img src="/assets/lumos-inicio.jpg" alt="Pantalla de Inicio de Lumos Wallet con el Libre del mes" width="640" height="1390"></div></div>
</section>
</div>

<section class="band"><div class="wrap">
<span class="eyebrow">Qué hace</span>
<h2>Todo lo que necesitas para llegar a fin de mes</h2>
{cards([
    (I_GAUGE, "Tu Libre, sin adivinar", "Tus ingresos menos tus pagos fijos, lo que vas guardando y tu ahorro. Toca el número y ve de dónde sale, y cuánto puedes gastar al día."),
    (I_JAR, "Apartados que se van llenando", "Fondo de emergencia, un viaje, el seguro del coche, el predial: dinos cuánto necesitas y para cuándo, y te decimos cuánto guardar cada mes."),
    (I_BOLT, "Captura en segundos", "Tus pagos con el celular se registran solos. Además: favoritos, widgets, un botón en el Centro de control y tu estado de cuenta en PDF, foto o CSV, leído en tu iPhone."),
    (I_USERS, "Hogar compartido", "Con tu pareja o tus roomies: repartan los gastos de la casa a partes iguales, según ingresos o por categoría, y vean quién le debe a quién. Cada quien conserva lo suyo."),
    (I_PIE, "Reportes y avisos", "En qué se va tu dinero cada mes, límites por categoría y recordatorios antes de cada pago, de tu tarjeta y de tu quincena."),
    (I_PIN, "Pensada para México", "Quincenas, meses sin intereses, fecha de corte y fecha límite de pago, lo que te deben y lo que debes, y cierre de mes."),
])}
</div></section>

<div class="wrap">
<section>
<span class="eyebrow">Privacidad</span>
<h2>Tu información es tuya</h2>
<ul class="checks">
<li>No nos conectamos a tu banco ni pedimos contraseñas bancarias.</li>
<li>Sin publicidad y sin rastreo entre apps.</li>
<li>Bloquea la app con reconocimiento facial y oculta los montos cuando quieras.</li>
<li>Exporta todo o borra tu cuenta desde la app, cuando quieras.</li>
</ul>
<p style="margin-top:22px"><a href="/lumos-wallet/privacidad/">Lee el aviso de privacidad →</a></p>
</section>

<section class="cta">
<h2>¿Tienes preguntas?</h2>
<p>Revisa las preguntas frecuentes o escríbenos. Respondemos lo antes posible.</p>
<div class="btns"><a class="btn primary" href="/lumos-wallet/soporte/">Ir a soporte</a><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></div>
</section>
</div>
"""
    return page("/lumos-wallet/", "Lumos Wallet · Tu presupuesto claro",
                "Lumos Wallet junta tus cuentas, tu quincena y tus pagos fijos en un solo número: lo que de verdad te queda para gastar este mes.", body)


def argo():
    body = f"""
<div class="wrap">
<section class="hero split">
<div>
<div class="app-id"><img src="/assets/argo-icon.png" alt="" width="72" height="72"><div><strong>Argo</strong><span>Viajes y gastos en grupo · iPhone</span></div></div>
<h1>Viajen juntos. Argo hace las cuentas.</h1>
<p class="lead">Planeen el viaje, decidan entre todos y lleven la cuenta de cada gasto en un solo lugar: el itinerario, las votaciones, la maleta, el fondo común y quién le debe a quién, al centavo. También para el depa, tu pareja o la fiesta.</p>
<div class="btns"><span class="pill">Muy pronto en la App Store</span></div>
</div>
<div style="position:relative"><div class="glow"></div><img class="hero-mark" src="/assets/argo-icon.png" alt="" width="240" height="240"></div>
</section>
</div>

<section class="band"><div class="wrap">
<span class="eyebrow">Para el viaje</span>
<h2>Todo el viaje en una sola app</h2>
{cards([
    (I_SUN, "Hoy", "Al abrir el viaje ves en qué día van, qué sigue en el plan y un botón para anotar el gasto en dos toques."),
    (I_CAL, "Itinerario por días", "Arma el plan día por día con horarios, lugares y quién va a cada actividad. El gasto de una actividad se divide solo entre quienes fueron."),
    (I_TICKET, "Pega tu reservación", "Copia el correo de confirmación del vuelo, el Airbnb o el tour, y Argo llena la actividad con la fecha, la clave de reservación y el monto."),
    (I_VOTE, "Votaciones", "¿Qué hotel? ¿Dónde cenamos? Propongan opciones con precio, pros y contras, voten y vean quién falta. Si hay empate, Argo ayuda a desempatar."),
    (I_BAG, "La maleta", "Lo que lleva cada quien y lo que se comparte. Apúntate con «Yo lo llevo», usa plantillas para playa, ciudad o frío y guarda las tuyas. Queda el historial de quién se apuntó."),
    (I_TASKS, "Pendientes", "Reservar el coche, comprar los boletos: asigna cada pendiente a alguien, con fecha, y márcalo cuando esté hecho."),
    (I_JAR, "Fondo del viaje", "La coope: pongan una meta por persona, vean quién ya aportó y paguen los gastos comunes directo del fondo."),
    (I_BED, "Hospedaje por noches", "Si alguien llega un día después o se va antes, paga solo las noches que se quedó."),
    (I_CHART, "Presupuesto y resumen", "Ponle un tope al viaje y ve cuánto pueden gastar por día. Al final, un resumen con el total, lo que tocó por persona y en qué se fue el dinero."),
])}
</div></section>

<div class="wrap">
<section>
<span class="eyebrow">Las cuentas</span>
<h2>Cuentas claras, amistades largas</h2>
{cards([
    (I_USERS, "Un grupo para cada cosa", "El viaje, el depa, tu pareja o una fiesta. Agrega a la gente solo con su nombre, aunque todavía no tenga la app: cuando se una, se queda con su lugar."),
    (I_PIE, "Divide como sea justo", "En partes iguales, por montos, porcentajes, partes o con ajustes, y con varios pagadores. Escanea el ticket y asigna cada artículo a quien lo pidió."),
    (I_GLOBE, "En cualquier moneda", "Anota el gasto en la moneda del lugar y Argo lo convierte con el tipo de cambio del día."),
    (I_MERGE, "Menos pagos para quedar a mano", "Con Simplificar deudas, Argo te sugiere la menor cantidad de pagos para que todos queden en paz."),
    (I_CASH, "Cobra y paga fácil", "Comparte tu CLABE, PayPal u otros métodos, manda un recordatorio amable y anota pagos completos o en abonos."),
    (I_REPEAT, "Gastos que se repiten", "La renta, los servicios y las suscripciones se anotan solos cada semana, mes o año, y pueden rotar quién paga."),
])}
</section>

<section>
<span class="eyebrow">Y además</span>
<h2>Pensada para cómo se hacen las cuentas en la vida real</h2>
<ul class="checks">
<li>Invita con un link, también por WhatsApp.</li>
<li>Anota un gasto escribiendo o dictando una frase: «Tacos 450, pagó Ana».</li>
<li>Avisos cuando alguien agrega un gasto o registra un pago.</li>
<li>Widgets con tu saldo y tu próximo viaje, y atajos de Siri.</li>
<li>En Personas ves cuánto te debe cada quien, sumando todos los grupos.</li>
<li>Reporte del grupo en PDF y CSV para cerrar cuentas.</li>
<li>Funciona sin internet y se sincroniza cuando vuelves a tener señal.</li>
<li>En español e inglés, con pesos, dólares, euros y otras monedas.</li>
</ul>
</section>

<section class="cta">
<span class="eyebrow">Miembro Fundador</span>
<h2>Un año de Argo Pro incluido</h2>
<p>Si creas tu cuenta antes del 1 de abril de 2027, eres Miembro Fundador: tienes un año de Argo Pro desde el día en que te registras, sin pagar nada y sin poner tarjeta. Pro agrega escanear tickets, alta rápida con una frase, leer reservaciones, el reporte en PDF, turnos en gastos recurrentes y tus propias plantillas de lista de empaque. Lo esencial, incluido todo el planificador de viajes, es gratis para siempre.</p>
</section>

<section>
<span class="eyebrow">Lo que viene</span>
<h2>Pronto en Argo</h2>
<p style="color:var(--muted);margin:0">Todavía no están disponibles, pero ya estamos trabajando en ellas.</p>
{cards([
    (I_LINK, "Argo en la web", "Tus mismos grupos, viajes y saldos desde la computadora."),
    (I_GAUGE, "Conexión con Lumos Wallet", "Lleva tu parte de cada gasto compartido a tu presupuesto en Lumos Wallet."),
])}
</section>

<section>
<span class="eyebrow">Privacidad</span>
<h2>Tu información es tuya</h2>
<ul class="checks">
<li>Argo no mueve dinero: solo lleva la cuenta de quién le debe a quién.</li>
<li>Sin publicidad y sin rastreo entre apps.</li>
<li>Lo que anotas en un grupo solo lo ven las personas de ese grupo.</li>
<li>Exporta todo o borra tu cuenta desde la app, cuando quieras.</li>
</ul>
<p style="margin-top:22px"><a href="/argo/privacidad/">Lee el aviso de privacidad →</a></p>
</section>

<section class="cta">
<h2>¿Tienes preguntas?</h2>
<p>Revisa las preguntas frecuentes o escríbenos. Respondemos lo antes posible.</p>
<div class="btns"><a class="btn primary" href="/argo/soporte/">Ir a soporte</a><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></div>
</section>
</div>
"""
    return page("/argo/", "Argo · Viajes y gastos en grupo",
                "Planeen el viaje y lleven la cuenta juntos: itinerario por días, votaciones, la maleta, el fondo común y quién le debe a quién, al centavo.", body, app="argo")


def legal(path, source, kind, app="lumos"):
    a = APPS[app]
    title, content = markdown((a["docs"] / source).read_text(encoding="utf-8"))
    meta = ""
    m = re.search(r"<p><strong>Última actualización:</strong> ([^<]+)</p>\n?", content)
    if m:
        meta = f'<p class="meta">Última actualización: {m.group(1)}</p>'
        content = content.replace(m.group(0), "")
    if kind == "soporte":
        # El primer párrafo (cómo contactarnos) se vuelve una caja con botón.
        first = re.match(r"<p>(.+?)</p>\n?", content)
        if first:
            content = content[first.end():]
            meta += f'<div class="contact"><p>{first.group(1)}</p><a class="btn primary" href="mailto:{EMAIL}">Escribir a soporte</a></div>'
        description = f"Ayuda y preguntas frecuentes de {a['name']}."
    else:
        first = re.match(r"(<p>.+?</p>)\n?", content)
        if first:
            content = content[first.end():]
            meta += f'<div class="intro">{first.group(1)}</div>'
        description = f"Aviso de privacidad de {a['name']}: qué información usa la app, para qué y cómo borrarla."
    body = f'<a class="back" href="{a["path"]}">← {a["name"]}</a><h1>{inline(title)}</h1>{meta}{content}'
    return page(path, f"{title}", description, body, doc=True, app=app)


def redirect(to, title="Lumos Wallet", keep_query=False):
    # keep_query: also carries ?c=TOKEN, so invite links sent before a rename still work.
    js = f'<script>location.replace("{to}"+location.search+location.hash)</script>' if keep_query else ""
    return f'<!DOCTYPE html><html lang="es-MX"><meta charset="utf-8"><title>{title}</title>{js}<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="https://vitaapps.io{to}"><p><a href="{to}">Continuar a {to}</a></p></html>\n'


def invite():
    # Referral rewards are off in the app for now (App Review); this page only invites.
    body = f"""<div class="wrap"><section class="hero cta">
<img src="/assets/lumos-icon.png" alt="" width="96" height="96" style="border-radius:22px;margin:0 auto 20px;box-shadow:var(--shadow)">
<span class="eyebrow">Te invitaron a Lumos Wallet</span>
<h1>Tu dinero claro en un número.</h1>
<p class="lead" style="margin:0 auto">Lumos Wallet te dice cuánto puedes gastar este mes sin tocar tus pagos fijos ni tus metas. Descárgalo en tu iPhone.</p>
<div class="btns"><a class="btn primary" href="https://apps.apple.com/mx/search?term=Lumos%20Wallet">Buscar en la App Store</a><a class="btn" href="/lumos-wallet/">Conocer Lumos Wallet</a></div>
</section></div>"""
    return page("/i/", "Te invitaron a Lumos Wallet", "Lumos Wallet te dice cuánto puedes gastar este mes. Descárgalo en tu iPhone.", body)


def lumos_delete_account():
    # Google Play pide un enlace web para pedir el borrado de la cuenta sin tener la app.
    body = """<div class="wrap"><section class="hero cta" style="text-align:left;max-width:720px;margin:0 auto">
<span class="eyebrow">Lumos Wallet</span>
<h1>Eliminar tu cuenta</h1>
<p class="lead">Puedes borrar tu cuenta y todos tus datos cuando quieras.</p>
<h2>Desde la app</h2>
<ul>
<li><strong>iPhone:</strong> Menú → Tu cuenta → Eliminar cuenta.</li>
<li><strong>Android y web (app.vitaapps.io):</strong> toca tu ícono de cuenta, arriba a la derecha → Eliminar cuenta.</li>
</ul>
<p>Te pedimos tu contraseña (o Apple) para confirmar que eres tú, y se borra en ese momento.</p>
<h2>Sin la app</h2>
<p>Escríbenos a <a href="mailto:support@vitaapps.io?subject=Eliminar%20mi%20cuenta%20de%20Lumos%20Wallet">support@vitaapps.io</a> desde el correo con el que te registraste, con el asunto "Eliminar mi cuenta". La borramos en un máximo de 30 días y te confirmamos por correo.</p>
<h2>Qué se borra</h2>
<ul>
<li>Tu espacio personal completo: cuentas, movimientos, plan, apartados, préstamos, fotos de comprobantes y ajustes.</li>
<li>Tu usuario para iniciar sesión.</li>
</ul>
<h2>Qué se queda</h2>
<ul>
<li>Si estás en un hogar compartido, sales de él. Lo que registraste en el hogar se queda para las demás personas; si eras la última, el hogar también se borra.</li>
<li>Los reportes de fallos que la app envió de forma anónima pueden conservarse hasta 90 días.</li>
<li>Si tienes Lumos Premium, cancela la suscripción en la tienda donde la compraste; borrar la cuenta no la cancela.</li>
</ul>
</section></div>"""
    return page("/lumos-wallet/eliminar-cuenta/", "Eliminar tu cuenta de Lumos Wallet", "Cómo borrar tu cuenta de Lumos Wallet y todos tus datos, con o sin la app.", body)


def lumos_join():
    # Destino del link de invitación a un hogar compartido (?c=TOKEN). El botón abre la
    # app con lumoswallet://invite/TOKEN; quien no la tiene ve cómo conseguirla. Los
    # links viejos alcanza://invite/... siguen funcionando en la app.
    body = """<div class="wrap"><section class="hero cta">
<img src="/assets/lumos-icon.png" alt="" width="96" height="96" style="border-radius:22px;margin:0 auto 20px;box-shadow:var(--shadow)">
<span class="eyebrow">Te invitaron a un hogar en Lumos Wallet</span>
<h1>Lleven juntos lo de la casa.</h1>
<p class="lead" style="margin:0 auto" id="lead">Abre la invitación en Lumos Wallet para unirte al hogar. Cada quien conserva su espacio personal; solo se comparte lo del hogar.</p>
<div class="btns"><a class="btn primary" id="open" href="/lumos-wallet/">Abrir en Lumos Wallet</a><button class="btn" id="copy" type="button">Copiar código</button></div>
<p style="margin-top:24px;font-size:15px">¿Aún no tienes la app? <a href="https://apps.apple.com/mx/search?term=Lumos%20Wallet">Descárgala en la App Store</a>, crea tu cuenta y vuelve a abrir este link. También puedes pegar el código en Menú → Hogar compartido → Ya tengo un código de invitación. El link funciona una vez y expira en 7 días.</p>
</section></div>
<script>
(function(){var t=(new URLSearchParams(location.search).get('c')||'').replace(/[^0-9A-Za-z]/g,'').slice(0,64);
var open=document.getElementById('open'),copy=document.getElementById('copy');
if(t.length>=16){open.href='lumoswallet://invite/'+t;}else{document.getElementById('lead').textContent='Este link está incompleto. Pide a quien te invitó que te lo vuelva a enviar.';open.style.display='none';copy.style.display='none';}
copy.onclick=function(){if(navigator.clipboard){navigator.clipboard.writeText(t);this.textContent='Copiado';}};})();
</script>"""
    return page("/lumos-wallet/hogar/", "Te invitaron a un hogar en Lumos Wallet", "Únete al hogar compartido en Lumos Wallet para llevar juntos los gastos de la casa.", body)


def argo_join():
    # Destino de los links de invitación a grupos de Argo (?c=TOKEN). Cuando
    # Associated Domains esté activo, iOS abre la app directo y esta página solo
    # la ve quien no tiene la app. Mientras tanto, el botón usa costsplit://.
    body = """<div class="wrap"><section class="hero cta">
<img src="/assets/argo-icon.png" alt="" width="96" height="96" style="border-radius:22px;margin:0 auto 20px;box-shadow:var(--shadow)">
<span class="eyebrow">Te invitaron a un grupo en Argo</span>
<h1>Cuentas claras con tu grupo.</h1>
<p class="lead" style="margin:0 auto" id="lead">Abre la invitación en Argo para ver el grupo y unirte.</p>
<div class="btns"><a class="btn primary" id="open" href="/argo/">Abrir en Argo</a><button class="btn" id="copy" type="button">Copiar link</button></div>
<p style="margin-top:24px;font-size:15px">¿Aún no tienes la app? Argo llega muy pronto a la App Store. Guarda este link para unirte cuando la instales.</p>
</section></div>
<script>
(function(){var t=(new URLSearchParams(location.search).get('c')||'').replace(/[^0-9A-Za-z]/g,'').slice(0,64);
var open=document.getElementById('open'),copy=document.getElementById('copy');
if(t.length>=16){open.href='costsplit://join/'+t;}else{document.getElementById('lead').textContent='Este link está incompleto. Pide a alguien del grupo que te lo vuelva a enviar.';open.style.display='none';copy.style.display='none';}
copy.onclick=function(){if(navigator.clipboard){navigator.clipboard.writeText(location.href);this.textContent='Copiado';}};})();
</script>"""
    return page("/argo/unirse/", "Te invitaron a Argo", "Únete a tu grupo en Argo para llevar las cuentas de los gastos compartidos.", body, app="argo")


def not_found():
    body = """<div class="wrap"><section class="hero cta"><span class="eyebrow">Error 404</span><h1>Esta página no existe.</h1>
<p class="lead" style="margin:0 auto">Quizá el enlace cambió. Estas sí existen:</p>
<div class="btns"><a class="btn primary" href="/">Inicio</a><a class="btn" href="/lumos-wallet/">Lumos Wallet</a><a class="btn" href="/argo/">Argo</a><a class="btn" href="/lumos-wallet/soporte/">Soporte</a></div></section></div>"""
    return page("/404.html", "Página no encontrada · Vita Apps", "", body)


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("  ", rel)


if __name__ == "__main__":
    print("Generando sitio:")
    write("index.html", landing())
    write("lumos-wallet/index.html", product())
    write("lumos-wallet/privacidad/index.html", legal("/lumos-wallet/privacidad/", "privacy-policy.md", "privacidad"))
    write("lumos-wallet/soporte/index.html", legal("/lumos-wallet/soporte/", "support.md", "soporte"))
    write("argo/index.html", argo())
    write("argo/privacidad/index.html", legal("/argo/privacidad/", "privacy-policy.md", "privacidad", app="argo"))
    write("argo/soporte/index.html", legal("/argo/soporte/", "support.md", "soporte", app="argo"))
    write("alcanza/index.html", redirect("/lumos-wallet/"))
    write("alcanza/privacidad/index.html", redirect("/lumos-wallet/privacidad/"))
    write("alcanza/soporte/index.html", redirect("/lumos-wallet/soporte/"))
    write("i/index.html", invite())
    write("argo/unirse/index.html", argo_join())
    # SplitNest se llamó así hasta octubre de 2026; sus links siguen funcionando.
    write("splitnest/index.html", redirect("/argo/", "Argo"))
    write("splitnest/privacidad/index.html", redirect("/argo/privacidad/", "Argo"))
    write("splitnest/soporte/index.html", redirect("/argo/soporte/", "Argo"))
    write("splitnest/unirse/index.html", redirect("/argo/unirse/", "Argo", keep_query=True))
    write("lumos-wallet/hogar/index.html", lumos_join())
    write("lumos-wallet/eliminar-cuenta/index.html", lumos_delete_account())
    write("404.html", not_found())
