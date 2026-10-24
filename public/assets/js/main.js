/* Autotrasporti Piccinini – script del sito (nessuna dipendenza, nessun tracciamento) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var ridotto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = function () { return window.innerWidth < 768; };

  /* ---------- Intestazione: sparisce scorrendo in giù, ricompare in su ---------- */
  var header = document.querySelector('.header');
  var ultimaY = window.scrollY;
  function aggiornaHeader() {
    if (!header) return;
    var y = window.scrollY;
    var aperto = header.classList.contains('menu-aperto') || header.querySelector('.ha-sotto.aperto');
    if (y < 80 || aperto || ridotto) header.classList.remove('nascosto');
    else if (y > ultimaY + 4) header.classList.add('nascosto');
    else if (y < ultimaY - 4) header.classList.remove('nascosto');
    ultimaY = y;
  }

  /* ---------- Menu mobile ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var aperto = header.classList.toggle('menu-aperto');
      menuBtn.setAttribute('aria-expanded', aperto ? 'true' : 'false');
      header.classList.remove('nascosto');
    });
  }
  /* Sottomenu Servizi */
  document.querySelectorAll('.ha-sotto').forEach(function (li) {
    var b = li.querySelector('.sotto-btn');
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var aperto = li.classList.toggle('aperto');
      b.setAttribute('aria-expanded', aperto ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!li.contains(e.target)) { li.classList.remove('aperto'); b.setAttribute('aria-expanded', 'false'); }
    });
    li.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { li.classList.remove('aperto'); b.setAttribute('aria-expanded', 'false'); b.focus(); }
    });
  });
  /* Chiudi il menu mobile quando si sceglie un'ancora */
  document.querySelectorAll('.nav a[href*="#"]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (header) { header.classList.remove('menu-aperto'); if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------- Parallax leggero (dimezzato su mobile) ---------- */
  var par = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  function aggiornaParallax() {
    if (ridotto || !par.length) return;
    var h = window.innerHeight;
    var f = mobile() ? 0.5 : 1;
    par.forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      if (box.bottom < -100 || box.top > h + 100) return;
      var forza = parseFloat(el.getAttribute('data-parallax')) || 0.12;
      var centro = box.top + box.height / 2 - h / 2;
      var dy = -centro * forza * f;
      var max = box.height * 0.08;
      dy = Math.max(-max, Math.min(max, dy));
      el.style.transform = 'translate3d(0,' + (dy - box.height * 0.08) + 'px,0)';
    });
  }

  var inCoda = false;
  function alloScroll() {
    if (inCoda) return;
    inCoda = true;
    requestAnimationFrame(function () { aggiornaHeader(); aggiornaParallax(); inCoda = false; });
  }
  window.addEventListener('scroll', alloScroll, { passive: true });
  window.addEventListener('resize', alloScroll);
  aggiornaParallax();

  /* ---------- Titoli che salgono parola per parola ---------- */
  var titoli = document.querySelectorAll('[data-parole]');
  titoli.forEach(function (t) {
    if (ridotto) return;
    var parole = t.textContent.trim().split(/\s+/);
    t.setAttribute('aria-label', t.textContent.trim());
    t.textContent = '';
    parole.forEach(function (p, i) {
      var esterno = document.createElement('span');
      esterno.className = 'parola';
      esterno.setAttribute('aria-hidden', 'true');
      var interno = document.createElement('span');
      interno.textContent = p;
      interno.style.transitionDelay = (i * 0.06) + 's';
      esterno.appendChild(interno);
      t.appendChild(esterno);
      if (i < parole.length - 1) t.appendChild(document.createTextNode(' '));
    });
  });

  /* ---------- Blocchi che compaiono allo scroll (IntersectionObserver) ---------- */
  if ('IntersectionObserver' in window && !ridotto) {
    var io = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (!v.isIntersecting) return;
        if (v.target.hasAttribute('data-parole')) v.target.classList.add('titolo-visto');
        else v.target.classList.add('visto');
        io.unobserve(v.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    document.querySelectorAll('.rivela, [data-parole]').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rivela').forEach(function (el) { el.classList.add('visto'); });
    titoli.forEach(function (t) { t.classList.add('titolo-visto'); });
  }

  /* ---------- Galleria a schermo intero ---------- */
  var lb = document.querySelector('.lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('.lightbox-cap');
    document.querySelectorAll('[data-grande]').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        lbImg.src = b.getAttribute('data-grande');
        lbImg.alt = img ? img.alt : '';
        lbCap.textContent = img ? img.alt : '';
        lb.showModal();
      });
    });
    lb.querySelector('.lightbox-chiudi').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lightbox-in')) lb.close(); });
    lb.addEventListener('close', function () { lbImg.removeAttribute('src'); });
  }

  /* ---------- Modulo: servizio preselezionato da ?servizio= ---------- */
  var selServ = document.querySelector('form[name="preventivo"] [name="servizio"][data-mappa]');
  if (selServ) {
    try {
      var chiave = new URLSearchParams(location.search).get('servizio');
      var mappa = JSON.parse(selServ.getAttribute('data-mappa'));
      if (chiave && mappa[chiave]) selServ.value = mappa[chiave];
    } catch (err) { /* parametro non valido: si ignora */ }
  }

  /* ---------- Selettore "quale servizio fa per te" ---------- */
  var sel = document.querySelector('[data-selettore]');
  var datiEl = document.getElementById('sel-dati');
  if (sel && datiEl) {
    var D = JSON.parse(datiEl.textContent);
    var risposte = {};
    var passo = 0;
    var passi = sel.querySelectorAll('[data-passo]');
    var contatore = sel.querySelector('.sel-passo span:first-child');
    var pallini = sel.querySelector('.sel-passo span:last-child');
    var indietro = sel.querySelector('.sel-indietro');

    function mostra(n) {
      passo = n;
      passi.forEach(function (p, i) { p.hidden = i !== n; });
      var tot = D.domande;
      if (n < tot) {
        contatore.textContent = D.etichettaPasso.replace('{n}', n + 1).replace('{t}', tot);
        var s = '';
        for (var i = 0; i < tot; i++) s += i <= n ? '●' : '○';
        pallini.textContent = s;
      } else {
        contatore.textContent = n === tot ? D.etichettaDati : D.etichettaEsito;
        pallini.textContent = '●●●';
      }
      indietro.hidden = n === 0;
      var focus = passi[n].querySelector('legend, h3');
      if (focus && n > 0) { focus.setAttribute('tabindex', '-1'); focus.focus({ preventScroll: true }); }
    }

    sel.querySelectorAll('.opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var q = b.getAttribute('data-q');
        risposte[q] = b.getAttribute('data-v');
        b.closest('fieldset').querySelectorAll('.opt').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        mostra(passo + 1);
      });
    });
    indietro.addEventListener('click', function () { if (passo > 0) mostra(passo - 1); });

    function consiglio() {
      var r = risposte;
      if (r.stato === 'bagnato') return 'asciugatura';
      if (r.stato === 'rotto') return 'aspirazione';
      if (r.bisogno === 'formato') return 'imballi';
      if (r.bisogno === 'recupero') return 'aspirazione';
      if (r.bisogno === 'stoccare') return 'deposito';
      if (r.forma === 'container') return 'deposito';
      if (r.forma === 'imballato') return 'imballi';
      return 'trasporti';
    }

    sel.querySelector('[data-calcola]').addEventListener('click', function () {
      var k = consiglio();
      var s = D.servizi[k];
      sel.querySelector('.sel-esito h3').textContent = s.nome;
      sel.querySelector('.sel-esito p').textContent = s.perche;
      var link = sel.querySelector('[data-scheda]');
      link.href = s.url;
      sel.setAttribute('data-esito', k);
      mostra(passi.length - 1);
    });

    sel.querySelector('[data-precompila]').addEventListener('click', function () {
      var k = sel.getAttribute('data-esito');
      var form = document.querySelector('form[name="preventivo"]');
      if (!form) return;
      var s = D.servizi[k];
      var campoServ = form.querySelector('[name="servizio"]');
      if (campoServ) campoServ.value = s.nome;
      var q = sel.querySelector('[name="sel-quantita"]').value.trim();
      var l = sel.querySelector('[name="sel-luogo"]').value.trim();
      var righe = [D.testoModulo.replace('{s}', s.nome)];
      ['forma', 'bisogno', 'stato'].forEach(function (k2) { if (risposte[k2]) righe.push('- ' + D.etichette[k2][risposte[k2]]); });
      if (q) righe.push(D.quantita + ': ' + q);
      if (l) righe.push(D.luogo + ': ' + l);
      var msg = form.querySelector('[name="messaggio"]');
      if (msg) msg.value = righe.join('\n');
      form.scrollIntoView({ behavior: ridotto ? 'auto' : 'smooth', block: 'start' });
      var primo = form.querySelector('[name="nome"]');
      if (primo) setTimeout(function () { primo.focus({ preventScroll: true }); }, ridotto ? 0 : 600);
    });

    mostra(0);
  }
})();
