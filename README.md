# www.transilospiccinini.com

Sito di **Autotrasporti Piccinini S.r.l.** (Interporto di Parma, Fontevivo PR), rifatto da zero a partire dal sito Wix precedente.
Sito statico HTML/CSS/JS, nessun framework, nessuna build su Netlify: viene pubblicata la cartella `public/` così com'è.

## Struttura

```
public/                  ← cartella pubblicata da Netlify
  index.html             home italiana
  en/                    versione inglese (stesse pagine, slug inglesi)
  trasporti/ deposito/ cambio-imballi/ aspirazione/ lavaggio/ asciugatura-vagliatura/
  storia/ qualita/ consulenze/ contatti/
  privacy-policy/ cookie-policy/ grazie/   (+ en/privacy-policy/, en/cookie-policy/, en/thank-you/)
  404.html  sitemap.xml  robots.txt  llms.txt
  assets/css/style.css   unico foglio di stile
  assets/js/main.js      unico script (nessuna libreria, nessun tracciamento)
  assets/fonts/          Archivo (variabile, larghezza 62–125%) e IBM Plex Mono – licenza OFL inclusa
  assets/img/            foto in WebP (800 e 1600 px), virate sui toni del sito (duotono 30%, hero 18%, attestati senza viraggio)
  assets/docs/           PDF: politiche aziendali, codice etico, scheda impianto fotovoltaico (PNRR)
sorgenti/                ← generatore delle pagine (non pubblicato)
  testi.py               dati aziendali, percorsi, testi dei servizi
  servizi_dettaglio.py   specifiche, passi, gallerie e FAQ di ogni servizio
  pagine.py              home, storia, qualità, consulenze, contatti, selettore
  legale.py              privacy e cookie policy (IT + traduzione EN)
  build.py               genera le pagine HTML in public/
netlify.toml             redirect 301 dal vecchio sito, intestazioni di sicurezza, cache
```

### Modificare un testo
1. Cambia il testo in `sorgenti/*.py` (ogni testo è presente in italiano e in inglese).
2. Rigenera: `python3 sorgenti/build.py` (serve Python 3.12+ con Pillow).
3. Fai commit di `sorgenti/` e `public/`.

`build.py` calcola anche il numero di versione di CSS e JS (`style.css?v=…`, `main.js?v=…`) dal contenuto dei file:
dopo ogni modifica a CSS o JS va rilanciato, così i browser scaricano subito la versione nuova.

### Sostituire una foto
Le immagini hanno cache di un anno: se cambi una foto **usa un nome di file nuovo** e aggiorna il riferimento nei sorgenti.
Ogni foto serve in due larghezze (`nome-800.webp`, `nome-1600.webp`).

## Modulo di contatto
Netlify Forms, modulo `preventivo` (home e pagina Contatti, in entrambe le lingue, stessi campi):
`nome`, `azienda`, `email`, `telefono`, `servizio`, `messaggio`, `privacy` (obbligatoria) + campo nascosto `lingua` e campo trappola `sito-web` contro lo spam.
Dopo l'invio si arriva a `/grazie/` o `/en/thank-you/`.
**Da fare nel pannello Netlify:** Forms → abilitare il rilevamento dei moduli e impostare la notifica e-mail verso `ass.clienti@transilospiccinini.com`.

Il selettore "Quale servizio fa per te" (home) fa 3 domande + 2 dati facoltativi, consiglia un servizio e precompila il modulo.
I link "Richiedi un preventivo" delle pagine servizio aprono i Contatti con il servizio già selezionato (`/contatti/?servizio=deposito`).

## Video
Il sito precedente non conteneva video. Se in futuro si aggiungono, vanno caricati come mp4 locali o con YouTube in modalità `youtube-nocookie.com` / Vimeo con `dnt=1`, solo al clic.

## Statistiche, cookie e privacy
- Nessun cookie, nessuno script di tracciamento, nessun banner. Statistiche con **Netlify Analytics** (dai log del server, da attivare nel pannello Netlify).
- Mappe: nessuna mappa incorporata, solo un link "Apri in Mappe".
- Privacy e cookie policy partono dai testi originali del sito; sono state tolte le parti su Wix, e-commerce, pagamenti e banner e corretti i refusi del modello. **Da far verificare a un consulente privacy.**

## SEO
- Title e description per pagina in IT/EN con parole chiave del settore; `hreflang` IT/EN/x-default, `canonical`, Open Graph.
- Dati strutturati JSON-LD: Organization/LocalBusiness, WebSite, Service, FAQPage, BreadcrumbList, ContactPage.
- `sitemap.xml` con alternate, `robots.txt`, `llms.txt` per i motori AI.
- Orari di apertura non inseriti: non sono indicati sul sito precedente.

## Pubblicazione
Repository GitHub `paoloserviziparma/transilospiccinini.com` → Netlify (Import from GitHub, publish directory `public`, nessun comando di build).
Ogni push su `main` pubblica il sito e consuma crediti Netlify: raggruppare le modifiche.

## Crediti
- Foto: archivio Autotrasporti Piccinini (dal sito precedente). Foto hero ritoccata (rimossi telaio, cartello, catena, paletti e colonnotti).
- Font: Archivo (Omnibus-Type) e IBM Plex Mono (IBM), SIL Open Font License 1.1.
