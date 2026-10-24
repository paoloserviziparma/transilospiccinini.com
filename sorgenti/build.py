# -*- coding: utf-8 -*-
"""Genera le pagine statiche del sito in ../public.
Uso: python3 sorgenti/build.py   (dalla cartella del repository)
Il sito pubblicato è solo HTML/CSS/JS statico: Netlify non esegue alcuna build.
"""
import hashlib, json, os, html
from testi import DOMINIO, AZIENDA, PERCORSI, SERVIZI_ORDINE, UI, SERVIZI, CONSULENZA_SEL
from servizi_dettaglio import DETTAGLI
from pagine import HOME, STORIA, QUALITA, CONSULENZE, CONTATTI, GRAZIE, ERRORE, SELETTORE
from legale import PRIVACY, COOKIE
from servizi_extra import EXTRA, ALT

LINGUA = "it"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(BASE, "public")
A = AZIENDA
e = html.escape


def ver(rel):
    with open(os.path.join(PUB, rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


V_CSS = ver("assets/css/style.css")
V_JS = ver("assets/js/main.js")


def img(nome, alt, cls="", sizes="100vw", par=None, eager=False, larghezze=(800, 1600)):
    """<img> WebP con srcset; par = forza parallax."""
    alt = ALT.get(LINGUA, {}).get(nome, alt)
    srcset = ", ".join(f"/assets/img/{nome}-{w}.webp {w}w" for w in larghezze)
    src = f"/assets/img/{nome}-{larghezze[-1]}.webp"
    attr = f' class="{cls}"' if cls else ""
    attr += f' data-parallax="{par}"' if par else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    from PIL import Image
    with Image.open(os.path.join(PUB, src.lstrip("/"))) as im:
        w, h = im.size
    return f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load}{attr}>'


def url(chiave, lang):
    return PERCORSI[chiave][lang]


ICONA_GIU = '<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
ICONA_MENU = '<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><path d="M3 7h20M3 13h20M3 19h20" stroke="currentColor" stroke-width="2"/></svg>'


def header(lang, chiave):
    u = UI[lang]
    altra = "en" if lang == "it" else "it"
    sotto = "".join(
        f'<li><a href="{url(k, lang)}"{" aria-current=\"page\"" if k == chiave else ""}>{SERVIZI[k][lang]["nome"]}</a></li>'
        for k in SERVIZI_ORDINE)
    voce = lambda k: f'<li><a href="{url(k, lang)}"{" aria-current=\"page\"" if k == chiave else ""}>{u[k]}</a></li>'
    lingue = (f'<a href="{url(chiave, "it")}" lang="it" hreflang="it"{" aria-current=\"true\"" if lang=="it" else ""} aria-label="Italiano">IT</a>'
              f'<a href="{url(chiave, "en")}" lang="en" hreflang="en"{" aria-current=\"true\"" if lang=="en" else ""} aria-label="English">EN</a>')
    return f'''<a class="skip" href="#contenuto">{u["salta"]}</a>
<header class="header">
<div class="wrap header-in">
<a class="logo" href="{url("home", lang)}" aria-label="{A["breve"]}, {u["home"]}"><img src="/assets/img/logo-piccinini.png" alt="Piccinini" width="148" height="120"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{u["menu"]}">{ICONA_MENU}</button>
<nav class="nav" id="nav" aria-label="{u["menu_principale"]}">
<ul>
<li class="ha-sotto"><button class="sotto-btn" type="button" aria-expanded="false">{u["servizi"]} {ICONA_GIU}</button><ul class="sotto">{sotto}</ul></li>
{voce("storia")}
{voce("qualita")}
{voce("consulenze")}
{voce("contatti")}
</ul>
<div class="lingue">{lingue}</div>
<a class="btn btn-p" href="{url("contatti", lang)}#preventivo">{u["preventivo"]}</a>
</nav>
</div>
</header>'''


def footer(lang):
    u = UI[lang]
    serv = "".join(f'<a href="{url(k, lang)}">{SERVIZI[k][lang]["nome"]}</a>' for k in SERVIZI_ORDINE)
    dati = u["dati_societari"].format(**A)
    return f'''<footer class="footer">
<div class="wrap">
<div class="footer-alto">
<div><img src="/assets/img/logo-piccinini-bianco.png" alt="Piccinini" width="148" height="120" loading="lazy">
<p>{A["nome"]}<br>{A["via"]} · {A["localita"]}<br>{A["cap"]} {A["comune"]} ({A["prov"]})<br>
{u["telefono"]} <a href="tel:{A["tel_link"]}">{A["tel"]}</a> · {u["fax"]} {A["fax"]}<br>
<a href="mailto:{A["email_clienti"]}">{A["email_clienti"]}</a></p></div>
<nav aria-label="{u["servizi"]}"><span class="t">{u["servizi"]}</span>{serv}</nav>
<nav aria-label="{u["azienda"]}"><span class="t">{u["azienda"]}</span>
<a href="{url("storia", lang)}">{u["storia"]}</a>
<a href="{url("qualita", lang)}">{u["qualita_cert"]}</a>
<a href="{url("consulenze", lang)}">{u["consulenze"]}</a>
<a href="{url("contatti", lang)}">{u["contatti"]}</a>
<a href="/assets/docs/politiche-aziendali.pdf">{u["pdf_politiche"]}</a>
<a href="/assets/docs/codice-etico.pdf">{u["pdf_codice"]}</a></nav>
</div>
<div class="footer-basso"><span>© {A["nome"]} · {dati}</span>
<span><a href="{url("privacy", lang)}">{u["privacy"]}</a> · <a href="{url("cookie", lang)}">{u["cookie"]}</a></span></div>
</div>
</footer>'''


def org_ld(lang):
    return {
        "@type": ["Organization", "LocalBusiness"],
        "@id": DOMINIO + "/#azienda",
        "name": A["nome"],
        "alternateName": ["Piccinini Transilos", "Transilos Piccinini"],
        "url": DOMINIO + "/",
        "logo": DOMINIO + "/assets/img/logo-piccinini.png",
        "image": DOMINIO + "/assets/img/og-image.jpg",
        "telephone": "+39 0521 615186",
        "faxNumber": "+39 0521 679228",
        "email": A["email_clienti"],
        "vatID": "IT" + A["piva"],
        "taxID": A["piva"],
        "address": {"@type": "PostalAddress", "streetAddress": "Via Parigi, 8 – Interporto di Parma, Loc. Bianconese",
                    "postalCode": A["cap"], "addressLocality": A["comune"], "addressRegion": A["prov"], "addressCountry": "IT"},
        "areaServed": {"@type": "Country", "name": "Italia" if lang == "it" else "Italy"},
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+39 0521 615186", "email": A["email_clienti"], "availableLanguage": ["it"]},
            {"@type": "ContactPoint", "contactType": "billing support", "email": A["email_amm"]},
        ],
    }


def briciole_ld(voci):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMINIO + p} for i, (n, p) in enumerate(voci)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}}
        for q, r in faq if "SEGNAPOSTO" not in r and "PLACEHOLDER" not in r]}


def pagina(lang, chiave, title, desc, corpo, ld=None, og_img="og-image.jpg", noindex=False, percorso=None, alternati=True):
    u = UI[lang]
    perc = percorso or url(chiave, lang)
    canon = DOMINIO + perc
    alt = ""
    if alternati and chiave in PERCORSI:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}{url(chiave, l)}">' for l in ("it", "en"))
        alt += f'<link rel="alternate" hreflang="x-default" href="{DOMINIO}{url(chiave, "it")}">'
    grafo = [org_ld(lang), {"@type": "WebSite", "@id": DOMINIO + "/#sito", "url": DOMINIO + "/", "name": A["breve"], "inLanguage": ["it", "en"], "publisher": {"@id": DOMINIO + "/#azienda"}}]
    grafo += ld or []
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{canon}">
{alt}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{A["breve"]}">
<meta property="og:locale" content="{u["locale"]}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMINIO}/assets/img/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#171795">
<link rel="icon" href="/assets/img/icona-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icona-180.png">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={V_CSS}">
<script type="application/ld+json">{ldjson}</script>
</head>
<body>
{header(lang, chiave)}
<main id="contenuto">
{corpo}
</main>
{footer(lang)}
<dialog class="lightbox" aria-label="{u["galleria"]}"><div class="lightbox-in"><button class="lightbox-chiudi" type="button" aria-label="{u["chiudi"]}">×</button><img alt=""><p class="lightbox-cap"></p></div></dialog>
<script src="/assets/js/main.js?v={V_JS}" defer></script>
</body>
</html>
'''


def scrivi(perc, contenuto):
    if perc.endswith("/"):
        perc += "index.html"
    dest = os.path.join(PUB, perc.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(contenuto)


# ------------------------------------------------------------------ blocchi
def testata(lang, chiave, riga, h1, lead, foto=None, alt="", cta=True, briciole=None):
    u = UI[lang]
    br = briciole or [(u["home"], url("home", lang))]
    br_html = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in br)
    br_html += f'<li><span aria-current="page">{e(h1)}</span></li>'
    btn = f'<div class="btns entra entra-4" style="margin-top:32px"><a class="btn btn-l" href="{url("contatti", lang)}#preventivo">{u["preventivo_lungo"]} →</a></div>' if cta else ""
    f = f'<div class="testata-foto">{img(foto, alt, par="0.14", eager=True, sizes="100vw")}</div>' if foto else ""
    return f'''<section class="testata">
<div class="wrap">
<nav class="briciole entra entra-1" aria-label="Breadcrumb"><ol>{br_html}</ol></nav>
<h1 class="entra entra-2"><span class="riga-locale">{e(riga)}</span>{e(h1)}</h1>
<p class="lead entra entra-3">{lead}</p>
{btn}
</div>
{f}
</section>'''


def faq_html(lang, faq, titolo=None, kicker=None):
    u = UI[lang]
    voci = "".join(f'<details class="faq"><summary>{e(q)}</summary><div class="r"><p>{r}</p></div></details>' for q, r in faq)
    return f'''<section class="sez sez-bianca">
<div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 320px"><p class="kicker">{u["faq"]}</p><h2 class="h2 h2-lato" data-parole>{e(titolo or u["faq"])}</h2></div>
<div style="flex:2 1 620px" class="rivela">{voci}</div>
</div>
</section>'''


def galleria_html(lang, nomi, alts, titolo=None):
    if not nomi:
        return ""
    u = UI[lang]
    voci = "".join(
        f'<button type="button" data-grande="/assets/img/{n}-1600.webp" aria-label="{u["ingrandisci"]}: {e(ALT[lang].get(n, alts.get(n, "")))}">'
        f'{img(n, alts.get(n, ""), sizes="(max-width:700px) 82vw, 600px")}</button>' for n in nomi)
    return f'''<section class="sez" style="padding-top:0">
<div class="wrap"><p class="kicker">{u["galleria"]}</p>
<div class="galleria rivela" role="list">{voci}</div></div>
</section>'''


def tabella_html(righe, intest=None, cls="tab tab-spec", etichette=("", "")):
    th = f'<thead><tr><th scope="col">{e(intest[0])}</th><th scope="col">{e(intest[1])}</th></tr></thead>' if intest else ""
    l1, l2 = intest if intest else etichette
    corpo = "".join(f'<tr><td data-label="{e(l1)}">{e(a)}</td><td data-label="{e(l2)}">{e(b)}</td></tr>' for a, b in righe)
    return f'<table class="{cls}">{th}<tbody>{corpo}</tbody></table>'


def modulo_html(lang, scelto=None):
    u = UI[lang]
    opzioni = [SERVIZI[k][lang]["nome_modulo"] for k in SERVIZI_ORDINE] + [CONSULENZA_SEL[lang]["nome"], u["f_altro"]]
    opt = "".join(f'<option{" selected" if o == scelto else ""}>{e(o)}</option>' for o in opzioni)
    azione = url("grazie", lang)
    return f'''<form class="modulo rivela" name="preventivo" method="POST" action="{azione}" data-netlify="true" netlify-honeypot="sito-web" aria-label="{u["contatti_titolo"]}">
<input type="hidden" name="form-name" value="preventivo">
<input type="hidden" name="lingua" value="{lang}">
<p class="trappola" aria-hidden="true"><label>{u["f_trappola"]} <input name="sito-web" tabindex="-1" autocomplete="off"></label></p>
<label class="campo">{u["f_nome"]} *<input type="text" name="nome" autocomplete="name" required></label>
<label class="campo">{u["f_azienda"]}<input type="text" name="azienda" autocomplete="organization"></label>
<label class="campo">{u["f_email"]} *<input type="email" name="email" autocomplete="email" required></label>
<label class="campo">{u["f_tel"]}<input type="tel" name="telefono" autocomplete="tel"></label>
<label class="campo tutta">{u["f_servizio"]}<select name="servizio" data-mappa="{e(json.dumps({k: SERVIZI[k][lang]['nome_modulo'] for k in SERVIZI_ORDINE}, ensure_ascii=False))}">{opt}</select></label>
<label class="campo tutta">{u["f_messaggio"]} *<textarea name="messaggio" rows="5" required placeholder="{e(u["f_msg_ph"])}"></textarea></label>
<label class="consenso tutta"><input type="checkbox" name="privacy" value="accettata" required> <span>{u["f_privacy"].format(url=url("privacy", lang))} *</span></label>
<div class="tutta" style="display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap"><button type="submit" class="btn btn-p">{u["f_invia"]} →</button><span style="font-size:13px;color:var(--muto)">* {u["f_obbl"]}</span></div>
</form>'''


def contatti_html(lang, titolo=None, lead=None, h1=False):
    u = UI[lang]
    tag = "h1" if h1 else "h2"
    return f'''<section class="sez" id="preventivo">
<div class="wrap split split-contatti">
<div>
<p class="kicker">{u["contatti"]}</p>
<{tag} class="h2" data-parole>{e(titolo or u["contatti_titolo"])}</{tag}>
<p class="lead" style="margin:20px 0 28px">{lead or u["contatti_lead"]}</p>
<address style="font-style:normal;font-size:17px;line-height:1.7;margin-bottom:28px"><a href="{A["mappe"]}" rel="noopener" target="_blank" style="color:var(--ink);text-decoration:none">{A["via"]} · {A["localita"]}<br>{A["cap"]} {A["comune"]} ({A["prov"]})</a><br><a href="{A["mappe"]}" rel="noopener" target="_blank" style="font-size:15px;font-weight:600">{u["apri_mappe"]} ↗</a></address>
<dl class="dati">
<div><dt>{u["telefono"]}</dt><dd><a href="tel:{A["tel_link"]}">{A["tel"]}</a></dd></div>
<div><dt>{u["ass_clienti"]}</dt><dd><a href="mailto:{A["email_clienti"]}">{A["email_clienti"]}</a></dd></div>
<div><dt>{u["deposito"]}</dt><dd><a href="mailto:{A["email_deposito"]}">{A["email_deposito"]}</a></dd></div>
<div><dt>{u["amministrazione"]}</dt><dd><a href="mailto:{A["email_amm"]}">{A["email_amm"]}</a></dd></div>
<div><dt>{u["fax"]}</dt><dd>{A["fax"]}</dd></div>
</dl>
</div>
{modulo_html(lang)}
</div>
</section>'''


def altri_servizi(lang, escludi):
    u = UI[lang]
    schede = "".join(scheda(lang, k, i) for i, k in enumerate(SERVIZI_ORDINE) if k != escludi)
    return f'''<section class="sez" style="padding-top:0">
<div class="wrap"><h2 class="h2" style="margin-bottom:32px" data-parole>{u["altri_servizi"]}</h2>
<div class="griglia rivela">{schede}</div></div></section>'''


def scheda(lang, k, i):
    s = SERVIZI[k]
    t = s[lang]
    return (f'<a class="card" href="{url(k, lang)}">{img(s["foto"], t["alt"], sizes="(max-width:700px) 100vw, 420px")}'
            f'<div class="card-c"><span class="n">0{SERVIZI_ORDINE.index(k)+1}</span><h3>{e(t["nome"])}</h3><p>{e(t["breve"])}</p>'
            f'<span class="piu">{UI[lang]["scopri"]} →</span></div></a>')


def selettore_html(lang):
    S = SELETTORE[lang]
    passi = ""
    for q in S["domande"]:
        opz = "".join(f'<button type="button" class="opt" data-q="{q["id"]}" data-v="{v}" aria-pressed="false">{e(t)}</button>' for v, t in q["opzioni"])
        passi += f'<div data-passo><fieldset><legend>{e(q["testo"])}</legend>{opz}</fieldset></div>'
    passi += f'''<div data-passo hidden><fieldset><legend>{e(S["dati_titolo"])}</legend>
<label>{e(S["quantita"])}<input name="sel-quantita" type="text" placeholder="{e(S["quantita_ph"])}"></label>
<label>{e(S["luogo"])}<input name="sel-luogo" type="text" placeholder="{e(S["luogo_ph"])}"></label></fieldset>
<div class="sel-nav" style="margin-top:20px"><button type="button" class="btn btn-l" data-calcola>{e(S["mostra"])} →</button></div></div>
<div data-passo hidden class="sel-esito" aria-live="polite"><p class="kicker" style="margin:0">{e(S["consiglio"])}</p><h3 tabindex="-1"></h3><p></p>
<div class="btns" style="margin-top:24px"><button type="button" class="btn btn-l" data-precompila>{e(S["precompila"])} →</button><a class="btn btn-o" data-scheda href="#">{e(S["vedi"])}</a></div></div>'''
    dati = {
        "domande": len(S["domande"]),
        "etichettaPasso": S["passo"], "etichettaDati": S["passo_dati"], "etichettaEsito": S["passo_esito"],
        "testoModulo": S["testo_modulo"], "quantita": S["quantita"], "luogo": S["luogo"],
        "etichette": {q["id"]: dict(q["opzioni"]) for q in S["domande"]},
        "servizi": {k: {"nome": SERVIZI[k][lang]["nome_modulo"], "perche": SERVIZI[k][lang]["perche"], "url": url(k, lang)} for k in SERVIZI_ORDINE},
    }
    return f'''<section class="sez sez-blu" id="selettore">
<div class="wrap split">
<div><p class="kicker">{e(S["kicker"])}</p><h2 class="h2" data-parole>{e(S["titolo"])}</h2><p class="lead" style="margin-top:20px">{e(S["lead"])}</p></div>
<div class="sel rivela" data-selettore role="group" aria-label="{e(S["titolo"])}">
<div class="sel-passo"><span></span><span aria-hidden="true"></span></div>
{passi}
<div class="sel-nav"><button type="button" class="sel-indietro" hidden>← {e(S["indietro"])}</button></div>
</div>
</div>
<script type="application/json" id="sel-dati">{json.dumps(dati, ensure_ascii=False)}</script>
</section>'''


# ------------------------------------------------------------------ pagine
def home(lang):
    H = HOME[lang]
    u = UI[lang]
    numeri = "".join(f'<div class="numero rivela"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in H["numeri"])
    tempo = "".join(f'<li><b>{a}</b><span>{e(b)}</span></li>' for a, b in H["tempo"])
    schede = "".join(scheda(lang, k, i) for i, k in enumerate(SERVIZI_ORDINE))
    guida = tabella_html([(a, b) for a, b, _ in H["guida"]], intest=H["guida_intest"], cls="tab")
    # rende cliccabile la colonna servizio
    for a, b, k in H["guida"]:
        guida = guida.replace(f'<td data-label="{e(H["guida_intest"][1])}">{e(b)}</td>', f'<td class="serv" data-label="{e(H["guida_intest"][1])}"><a href="{url(k, lang)}">{e(b)} →</a></td>', 1)
    metodi = ""
    for m in H["metodi"]:
        dl = "".join(f'<div><dt>{e(a)}</dt><dd{" class=\"noi\"" if i == len(m["righe"])-1 else ""}>{e(b)}</dd></div>' for i, (a, b) in enumerate(m["righe"]))
        metodi += f'<div class="metodo rivela"><h3>{e(m["titolo"])}</h3><dl>{dl}</dl></div>'
    cert = "".join(f'<div><span class="a">{e(a)}</span><b>{e(b)}</b><p>{e(c)}</p></div>' for a, b, c in H["cert"])
    corpo = f'''<section class="hero">
<div class="wrap hero-testo">
<h1 class="entra entra-1"><span class="riga-locale">{e(H["riga_locale"])}</span>{e(H["h1"])}</h1>
<div class="hero-lato"><p class="entra entra-2">{H["lead"]}</p>
<div class="btns entra entra-3"><a class="btn btn-l" href="#preventivo">{u["preventivo_lungo"]} →</a><a class="btn btn-o" href="#servizi">{u["scopri_servizi"]}</a></div></div>
</div>
<div class="hero-foto">{img("hero", H["hero_alt"], par="0.12", eager=True, larghezze=(800, 1200, 2000))}</div>
<div class="numeri"><div class="wrap">{numeri}</div></div>
</section>

<section class="sez" id="chi-siamo">
<div class="wrap split">
<div>
<p class="kicker">{e(H["chi_kicker"])}</p>
<h2 class="h2" data-parole>{e(H["chi_titolo"])}</h2>
<p class="lead rivela" style="margin:24px 0 32px">{H["chi_testo"]}</p>
<ol class="tempo rivela">{tempo}</ol>
<p style="margin-top:28px"><a class="link-freccia" href="{url("storia", lang)}">{e(H["chi_link"])} →</a></p>
</div>
<div class="foto-par foto-sede">{img("sede-capannone", H["sede_alt"], par="0.1", sizes="360px")}</div>
</div>
</section>

<section class="sez" id="servizi" style="padding-top:0">
<div class="wrap">
<div class="testa-sez"><div><p class="kicker">{u["servizi"]}</p><h2 class="h2" data-parole>{e(H["serv_titolo"])}</h2></div><p class="lead">{e(H["serv_lead"])}</p></div>
<div class="griglia rivela">{schede}</div>
</div>
</section>

<section class="sez sez-bianca" id="guida">
<div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 340px"><p class="kicker">{e(H["guida_kicker"])}</p><h2 class="h2 h2-lato" data-parole>{e(H["guida_titolo"])}</h2><p class="lead" style="margin-top:20px">{e(H["guida_lead"])}</p></div>
<div style="flex:2 1 620px" class="rivela">{guida}</div>
</div>
</section>

<section class="sez" id="confronto">
<div class="wrap">
<p class="kicker">{e(H["metodi_kicker"])}</p>
<h2 class="h2" style="max-width:820px;margin-bottom:16px" data-parole>{e(H["metodi_titolo"])}</h2>
<p class="lead" style="max-width:720px;margin-bottom:40px">{e(H["metodi_lead"])}</p>
<div class="griglia">{metodi}</div>
</div>
</section>

{selettore_html(lang)}

<section class="sez sez-notte" id="qualita">
<div class="wrap">
<div class="testa-sez"><div><p class="kicker">{e(H["qual_kicker"])}</p><h2 class="h2" data-parole>{e(H["qual_titolo"])}</h2></div><p class="lead">{e(H["qual_lead"])}</p></div>
<div class="cert rivela">{cert}</div>
<p style="margin-top:32px"><a class="link-freccia" style="color:#fff" href="{url("qualita", lang)}">{e(H["qual_link"])} →</a></p>
</div>
</section>

<section class="sez" id="consulenze">
<div class="wrap split">
<div class="foto-par foto-media">{img("consulenze-3", H["cons_alt"], par="0.1", sizes="420px")}</div>
<div>
<p class="kicker">{u["consulenze"]}</p>
<h2 class="h2" data-parole>{e(H["cons_titolo"])}</h2>
<p class="lead rivela" style="margin:20px 0 28px">{e(H["cons_testo"])}</p>
<div class="btns"><a class="btn btn-p" href="{url("consulenze", lang)}">{e(H["cons_btn"])} →</a></div>
</div>
</div>
</section>

{faq_html(lang, H["faq"], H["faq_titolo"])}

{contatti_html(lang)}'''
    ld = [faq_ld(H["faq"])]
    return pagina(lang, "home", H["title"], H["desc"], corpo, ld)


def servizio(lang, k):
    s = SERVIZI[k]
    t = s[lang]
    d = DETTAGLI[k]
    dl = d[lang]
    u = UI[lang]
    X = EXTRA[k][lang]
    voci = "".join(f"<li>{e(x)}</li>" for x in X["in_breve"])
    blocchi = f'''<section class="breve-sez"><div class="wrap"><div class="breve rivela"><h2 class="kicker">{"In breve" if lang == "it" else "At a glance"}</h2><ul>{voci}</ul></div></div></section>'''
    tit, txt, lista = X["per_chi"]
    li = f'<ul>{"".join(f"<li>{e(x)}</li>" for x in lista)}</ul>' if lista else ""
    blocchi += f'''<section class="sez"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 340px"><h2 class="h2 h2-lato" data-parole>{e(tit)}</h2></div>
<div style="flex:2 1 620px" class="testo rivela" ><p style="font-size:18px">{e(txt)}</p>{li}</div></div></section>'''
    if dl.get("tabella"):
        tab = tabella_html(dl["tabella"], intest=dl.get("tabella_intest"), cls="tab tab-spec" if not dl.get("tabella_intest") else "tab",
                           etichette=("", ""))
        blocchi += f'''<section class="sez sez-bianca"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 340px"><p class="kicker">{e(t["nome"])}</p><h2 class="h2 h2-lato" data-parole>{e(dl["tabella_titolo"])}</h2></div>
<div style="flex:2 1 620px" class="rivela">{tab}</div></div></section>'''
    if dl.get("specs"):
        sp = "".join(f'<div class="spec rivela"><h3>{e(a)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></div>' for a, b in dl["specs"])
        tit = dl.get("versioni_titolo")
        h = f'<h2 class="h2" style="margin-bottom:32px" data-parole>{e(tit)}</h2>' if tit else ""
        blocchi += f'<section class="sez"><div class="wrap">{h}<div class="specs">{sp}</div></div></section>'
    passi = "".join(f'<li class="rivela"><b>{e(a)}</b>{e(b)}</li>' for a, b in dl["passi"])
    blocchi += f'<section class="sez"{" style=\"padding-top:0\"" if dl.get("specs") else ""}><div class="wrap"><h2 class="h2" style="margin-bottom:32px" data-parole>{e(dl["passi_titolo"])}</h2><ol class="passi">{passi}</ol></div></section>'
    blocchi += galleria_html(lang, d["galleria"], dl["alt"])
    faq_tutte = dl["faq"] + X["faq"]
    blocchi += faq_html(lang, faq_tutte)
    cta = f'''<section class="sez sez-blu"><div class="wrap split">
<div><h2 class="h2" data-parole>{e(t["nome_modulo"])}: {"parliamone" if lang == "it" else "let’s talk"}</h2></div>
<div><p class="lead" style="margin-bottom:24px">{e(u["contatti_lead"])}</p><div class="btns"><a class="btn btn-l" href="{url("contatti", lang)}?servizio={k}#preventivo">{u["preventivo_lungo"]} →</a><a class="btn btn-o" href="tel:{A["tel_link"]}">{u["telefono"]} {A["tel"]}</a></div></div>
</div></section>'''
    corpo = testata(lang, k, t["riga_locale"], t["h1"], e(t["lead"]), foto=s["foto"], alt=t["alt"],
                    briciole=[(u["home"], url("home", lang)), (u["servizi"], url("home", lang) + "#servizi")]) + blocchi + cta + altri_servizi(lang, k)
    ld = [
        {"@type": "Service", "name": t["h1"], "serviceType": t["nome"], "description": t["desc"], "url": DOMINIO + url(k, lang),
         "provider": {"@id": DOMINIO + "/#azienda"}, "areaServed": {"@type": "Country", "name": "Italia" if lang == "it" else "Italy"},
         "image": DOMINIO + f"/assets/img/{s['foto']}-1600.webp"},
        briciole_ld([(u["home"], url("home", lang)), (t["nome"], url(k, lang))]),
        faq_ld(faq_tutte),
    ]
    return pagina(lang, k, t["title"], t["desc"], corpo, ld)


def semplice(lang, chiave, P, corpo_extra, ld_extra=None, foto=None, alt=""):
    u = UI[lang]
    corpo = testata(lang, chiave, P["riga_locale"], P["h1"], P["lead"], foto=foto, alt=alt, cta=P.get("cta", True)) + corpo_extra
    ld = [briciole_ld([(u["home"], url("home", lang)), (P["h1"], url(chiave, lang))])] + (ld_extra or [])
    return pagina(lang, chiave, P["title"], P["desc"], corpo, ld)


def storia(lang):
    P = STORIA[lang]
    tempo = "".join(f'<li><b>{a}</b><span>{e(b)}</span></li>' for a, b in P["tempo"])
    paragrafi = "".join(f"<p>{x}</p>" for x in P["testo"])
    uffici = "".join(f"<li>{e(x)}</li>" for x in P["uffici"])
    corpo = f'''<section class="sez"><div class="wrap split" style="align-items:flex-start">
<div class="testo rivela" style="flex:1.3 1 520px;font-size:18px">{paragrafi}</div>
<div style="flex:1 1 380px"><h2 class="h2" style="font-size:28px;margin-bottom:20px">{e(P["tempo_titolo"])}</h2><ol class="tempo rivela">{tempo}</ol></div>
</div></section>
<section class="sez" style="padding-top:0"><div class="wrap split">
<div class="foto-par foto-sede">{img("storia-02", P["cento_alt"], par="0.08", sizes="360px")}</div>
<div><p class="kicker">{e(P["foto_kicker"])}</p><h2 class="h2" data-parole>{e(P["foto_titolo"])}</h2><p class="lead" style="margin-top:20px">{e(P["foto_lead"])}</p></div>
</div></section>
{galleria_html(lang, ["storia-%02d" % i for i in range(1, 11) if i != 2], {"storia-%02d" % i: P["storiche_alt"] for i in range(1, 11)})}
<section class="sez sez-bianca" id="sede"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 400px"><p class="kicker">2014</p><h2 class="h2" data-parole>{e(P["sede_titolo"])}</h2></div>
<div style="flex:1.4 1 520px" class="testo rivela"><p>{P["sede_testo"]}</p><ul>{uffici}</ul><p>{P["sede_testo2"]}</p></div>
</div></section>
<div class="sez-bianca">{galleria_html(lang, ["sede-edificio-1", "sede-edificio-2", "sede-taglio-nastro", "sede-persone", "sede-officina", "sede-stanza-1", "sede-stanza-2", "sede-stanza-3"], P["sede_alt"])}</div>
{contatti_html(lang)}'''
    return semplice(lang, "storia", P, corpo, foto="sede-edificio-2", alt=P["testata_alt"])


def qualita(lang):
    P = QUALITA[lang]
    u = UI[lang]
    cert = "".join(f'<div><span class="a">{e(a)}</span><b>{e(b)}</b><p>{e(c)}</p></div>' for a, b, c in P["cert"])
    sicurezza = "".join(f"<li>{e(x)}</li>" for x in P["sicurezza"])
    sost = "".join(f"<li>{x}</li>" for x in P["sostenibilita"])
    att = ["qualita-iso-p1", "qualita-iso-p2", "qualita-sqas-2024", "qualita-sqas", "qualita-michelin", "qualita-att-1", "qualita-att-2"]
    corpo = f'''<section class="sez sez-notte"><div class="wrap">
<p class="kicker">{e(P["cert_kicker"])}</p><h2 class="h2" style="margin-bottom:40px" data-parole>{e(P["cert_titolo"])}</h2>
<div class="cert rivela">{cert}</div></div></section>
<section class="sez"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 380px"><p class="kicker">{e(P["sic_kicker"])}</p><h2 class="h2" data-parole>{e(P["sic_titolo"])}</h2><p class="lead" style="margin-top:20px">{e(P["sic_lead"])}</p></div>
<div style="flex:1.3 1 520px" class="testo rivela"><ul>{sicurezza}</ul><p>{e(P["fiducia"])}</p></div>
</div></section>
<section class="sez sez-bianca"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 380px"><p class="kicker">{e(P["sost_kicker"])}</p><h2 class="h2" data-parole>{e(P["sost_titolo"])}</h2></div>
<div style="flex:1.3 1 520px" class="testo rivela"><ul>{sost}</ul><p class="nota" style="margin-top:24px">{P["pnrr"]}</p></div>
</div></section>
<section class="sez"><div class="wrap"><p class="kicker">{e(P["att_kicker"])}</p><h2 class="h2" style="margin-bottom:28px" data-parole>{e(P["att_titolo"])}</h2></div>
{galleria_html(lang, att, P["att_alt"]).replace('<section class="sez" style="padding-top:0">', '<div>').replace('</section>', '</div>')}
<div class="wrap"><div class="btns" style="margin-top:12px"><a class="btn btn-p" href="/assets/docs/politiche-aziendali.pdf">{u["pdf_politiche"]}</a><a class="btn btn-p" href="/assets/docs/codice-etico.pdf">{u["pdf_codice"]}</a></div></div>
</section>
{contatti_html(lang)}'''
    return semplice(lang, "qualita", P, corpo, foto="bg-storia-qualita", alt=P["testata_alt"])


def consulenze(lang):
    P = CONSULENZE[lang]
    temi = "".join(f"<li>{e(x)}</li>" for x in P["temi"])
    passi = "".join(f'<li class="rivela"><b>{e(a)}</b>{e(b)}</li>' for a, b in P["passi"])
    corpo = f'''<section class="sez"><div class="wrap split" style="align-items:flex-start">
<div style="flex:1 1 380px"><p class="kicker">{e(P["temi_kicker"])}</p><h2 class="h2" data-parole>{e(P["temi_titolo"])}</h2></div>
<div style="flex:1.3 1 520px" class="testo rivela" ><ul style="font-size:18px">{temi}</ul></div>
</div></section>
<section class="sez" style="padding-top:0"><div class="wrap"><h2 class="h2" style="margin-bottom:32px" data-parole>{e(P["passi_titolo"])}</h2><ol class="passi">{passi}</ol></div></section>
{galleria_html(lang, ["consulenze-1", "consulenze-2", "consulenze-3"], P["alt"])}
{contatti_html(lang, P["cta_titolo"])}'''
    ld = [{"@type": "Service", "name": P["h1"], "serviceType": P["h1"], "description": P["desc"], "url": DOMINIO + url("consulenze", lang), "provider": {"@id": DOMINIO + "/#azienda"}}]
    return semplice(lang, "consulenze", P, corpo, ld, foto="consulenze-3", alt=P["testata_alt"])


def contatti(lang):
    P = CONTATTI[lang]
    u = UI[lang]
    corpo = f'''<section class="testata"><div class="wrap">
<nav class="briciole entra entra-1" aria-label="Breadcrumb"><ol><li><a href="{url("home", lang)}">{u["home"]}</a></li><li><span aria-current="page">{u["contatti"]}</span></li></ol></nav>
<h1 class="entra entra-2"><span class="riga-locale">{e(P["riga_locale"])}</span>{e(P["h1"])}</h1>
<p class="lead entra entra-3">{e(P["lead"])}</p></div></section>
{contatti_html(lang, P["form_titolo"])}'''
    ld = [briciole_ld([(u["home"], url("home", lang)), (u["contatti"], url("contatti", lang))]),
          {"@type": "ContactPage", "url": DOMINIO + url("contatti", lang), "name": P["title"], "about": {"@id": DOMINIO + "/#azienda"}}]
    return pagina(lang, "contatti", P["title"], P["desc"], corpo, ld)


def legale(lang, chiave, L):
    u = UI[lang]
    corpo = f'''<section class="testata"><div class="wrap">
<nav class="briciole" aria-label="Breadcrumb"><ol><li><a href="{url("home", lang)}">{u["home"]}</a></li><li><span aria-current="page">{e(L["h1"])}</span></li></ol></nav>
<h1>{e(L["h1"])}</h1>{f'<p class="lead">{L["nota"]}</p>' if L.get("nota") else ""}</div></section>
<section class="sez"><div class="wrap"><div class="legale">{L["corpo"]}</div></div></section>'''
    return pagina(lang, chiave, L["title"], L["desc"], corpo)


def grazie(lang):
    G = GRAZIE[lang]
    corpo = f'''<section class="sez"><div class="wrap centro">
<p class="kicker">{e(G["kicker"])}</p><h1 class="h2" style="font-size:clamp(34px,4.6vw,60px)">{e(G["h1"])}</h1>
<p class="lead" style="max-width:60ch">{G["testo"]}</p>
<div class="btns"><a class="btn btn-p" href="{url("home", lang)}">{e(G["btn"])}</a></div></div></section>'''
    return pagina(lang, "grazie", G["title"], G["desc"], corpo, noindex=True)


def errore():
    E = ERRORE
    corpo = f'''<section class="sez"><div class="wrap centro">
<p class="kicker">Errore 404</p><h1 class="h2" style="font-size:clamp(34px,4.6vw,60px)">{e(E["h1"])}</h1>
<p class="lead" style="max-width:60ch">{E["testo"]}</p>
<div class="btns"><a class="btn btn-p" href="/">{e(E["btn"])}</a><a class="btn btn-p" href="/contatti/">{e(E["btn2"])}</a><a class="btn btn-p" href="/en/" lang="en">English</a></div></div></section>'''
    return pagina("it", "home", E["title"], E["desc"], corpo, noindex=True, percorso="/404.html", alternati=False)


# ------------------------------------------------------------------ file di servizio
def sitemap():
    righe = []
    for k, p in PERCORSI.items():
        if k == "grazie":
            continue
        for l in ("it", "en"):
            alt = "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{DOMINIO}{p[l2]}"/>' for l2 in ("it", "en"))
            alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMINIO}{p["it"]}"/>'
            righe.append(f"<url><loc>{DOMINIO}{p[l]}</loc>{alt}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(righe) + "\n</urlset>\n")


def main():
    global LINGUA
    for lang in ("it", "en"):
        LINGUA = lang
        scrivi(url("home", lang), home(lang))
        for k in SERVIZI_ORDINE:
            scrivi(url(k, lang), servizio(lang, k))
        scrivi(url("storia", lang), storia(lang))
        scrivi(url("qualita", lang), qualita(lang))
        scrivi(url("consulenze", lang), consulenze(lang))
        scrivi(url("contatti", lang), contatti(lang))
        scrivi(url("privacy", lang), legale(lang, "privacy", PRIVACY[lang]))
        scrivi(url("cookie", lang), legale(lang, "cookie", COOKIE[lang]))
        scrivi(url("grazie", lang), grazie(lang))
    LINGUA = "it"
    scrivi("/404.html", errore())
    scrivi("/sitemap.xml", sitemap())
    scrivi("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /grazie/\nDisallow: /en/thank-you/\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("Pagine generate in", PUB, "– CSS v", V_CSS, "JS v", V_JS)


if __name__ == "__main__":
    main()
