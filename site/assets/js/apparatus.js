/* Aparato de notas al pie — la interacción-firma del sitio.
   Mejora progresiva en TRES estados, y ninguno pierde el porqué:
     sin JS  → todas las notas visibles al pie de su sección;
     angosto → plegadas, cada marcador [n] abre la suya;
     ancho   → AL MARGEN, siempre visibles, junto al bloque que afirma.
   El tercer estado (2026-08-17) existe porque en pantallas grandes la
   columna derecha estaba vacía en todas las páginas de caso: el aparato
   que ya era el diferencial del sitio pasa a ocuparla. */
(function () {
  document.documentElement.classList.add("js");

  var ancho = window.matchMedia("(min-width: 72rem)");
  var items = [];
  var refs = document.querySelectorAll("button.fn-ref");

  /* ⛔ El margen es para las secciones DE TEXTO. Donde hay una rejilla de
     imágenes, el ancho es de las imágenes: una nota flotando obliga a la
     rejilla a empezar debajo (un contenedor de rejilla nunca se solapa con
     un flotante) y abre un hueco vertical del alto de la nota. Medido el
     2026-08-17: la home crecía 1.200 px en huecos. Regla que se mantiene
     sola — si mañana una sección gana una galería, deja de usar el margen. */
  function conMargen(caja) {
    return !caja.querySelector(".cards, .mosaico, .case-lead, .persona");
  }

  /* Sube desde el marcador hasta el hijo DIRECTO de la caja que guarda la
     nota. La nota se inserta después de ese bloque y nunca dentro de una
     rejilla estrecha (una nota flotando dentro de .case-lead se comería la
     mitad de su columna). */
  function bloqueDe(ref, caja) {
    var n = ref;
    while (n && n.parentNode !== caja) n = n.parentNode;
    return n;
  }

  var apagar;
  function destacar(note) {
    note.classList.remove("fn-flash");
    void note.offsetWidth;              /* reinicia la animación */
    note.classList.add("fn-flash");
    note.scrollIntoView({ block: "nearest", behavior: "smooth" });
    clearTimeout(apagar);
    apagar = setTimeout(function () { note.classList.remove("fn-flash"); }, 1300);
  }

  for (var i = 0; i < refs.length; i++) {
    (function (ref) {
      var note = document.getElementById(ref.getAttribute("aria-controls"));
      if (!note) return;
      var caja = note.parentNode;
      var it = {
        ref: ref, note: note, caja: caja,
        sigue: note.nextSibling,          /* su sitio original, para volver */
        bloque: bloqueDe(ref, caja),
        margen: conMargen(caja)
      };
      items.push(it);
      ref.addEventListener("click", function () {
        if (ancho.matches && it.margen) { destacar(note); return; }
        var abrir = note.hidden;
        note.hidden = !abrir;
        ref.setAttribute("aria-expanded", String(abrir));
        if (abrir) note.scrollIntoView({ block: "nearest", behavior: "smooth" });
      });
    })(refs[i]);
  }

  function colocar() {
    var margen = ancho.matches;
    for (var k = 0; k < items.length; k++) {
      var it = items[k];
      if (margen && it.margen) {
        if (it.bloque && it.note.previousElementSibling !== it.bloque) {
          it.caja.insertBefore(it.note, it.bloque.nextSibling);
        }
        it.note.classList.add("al-margen");
        it.note.hidden = false;
        it.ref.setAttribute("aria-expanded", "true");
      } else {
        if (it.note.nextSibling !== it.sigue) it.caja.insertBefore(it.note, it.sigue);
        it.note.classList.remove("al-margen");
        it.note.hidden = true;
        it.ref.setAttribute("aria-expanded", "false");
      }
    }
  }
  colocar();
  if (ancho.addEventListener) ancho.addEventListener("change", colocar);
  else if (ancho.addListener) ancho.addListener(colocar);

  /* Revelado al hacer scroll — SOLO imágenes (el texto jamás se anima).
     IntersectionObserver, nunca listener de scroll; reduced-motion lo apaga
     por CSS. Sin IO, las imágenes simplemente quedan visibles.
     rootMargin POSITIVO abajo (2026-08-17): el revelado arranca antes de que
     la imagen entre en pantalla, así deja de aparecer de golpe al hacer
     scroll — el defecto era el momento del disparo, no el peso. */
  if ("IntersectionObserver" in window) {
    var shots = document.querySelectorAll("img.shot");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("en-escena");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px 12% 0px" });
    for (var j = 0; j < shots.length; j++) {
      shots[j].setAttribute("data-reveal", "");
      io.observe(shots[j]);
    }
  }

  /* Film: el póster es un enlace al mp4 (sin JS, el navegador lo abre). Con JS
     se cambia por el reproductor EN SU SITIO: mismo hueco, sin salto de
     maqueta, controles nativos, subtítulos en inglés puestos (la locución es
     en español) y el foco pasa al reproductor. El vídeo no se pide hasta este
     click — preload="none" sería redundante, pero queda dicho. */
  document.querySelectorAll("a.film").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;   /* abrir en pestaña sigue siendo del visitante */
      e.preventDefault();
      var v = document.createElement("video");
      v.className = "film-player";
      v.controls = true; v.playsInline = true; v.preload = "none";
      v.setAttribute("width", "1920"); v.setAttribute("height", "1080");
      v.poster = a.getAttribute("data-poster") || "";
      v.setAttribute("aria-label", (a.getAttribute("aria-label") || "Film").replace(/^Play the film: /, "Film: "));
      var s = document.createElement("source"); s.src = a.getAttribute("href"); s.type = "video/mp4"; v.appendChild(s);
      [["en", "English", true], ["es", "Español", false]].forEach(function (p) {
        var src = a.getAttribute("data-" + p[0]); if (!src) return;
        var tr = document.createElement("track"); tr.kind = "subtitles"; tr.srclang = p[0]; tr.label = p[1]; tr.src = src; tr.default = p[2]; v.appendChild(tr);
      });
      a.parentNode.replaceChild(v, a);
      v.focus();
      var p = v.play(); if (p && p.catch) p.catch(function () {});   /* si el navegador niega el arranque, los controles siguen ahí */
    });
  });

  /* Menú móvil (bajo 62rem): un disclosure, no un cajón. El panel es una
     fila más de la barra — ver site.css —, así que aquí no hay scroll que
     bloquear ni foco que encerrar: solo abrir, cerrar, y no dejar nunca el
     estado colgado. Sin este script el botón no se pinta y las anclas se
     muestran apiladas, así que nadie se queda sin navegación. */
  var toggle = document.querySelector(".nav-toggle");
  var barra = document.querySelector("nav.nav");
  if (toggle && barra) {
    var abrir = function (si) {
      barra.classList.toggle("menu-abierto", si);
      toggle.setAttribute("aria-expanded", si ? "true" : "false");
    };
    toggle.addEventListener("click", function () {
      abrir(toggle.getAttribute("aria-expanded") !== "true");
    });
    /* Un ancla del panel ya lleva a su sección: el panel cumplió y estorba. */
    barra.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () { abrir(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && barra.classList.contains("menu-abierto")) {
        abrir(false);
        toggle.focus();              /* el foco vuelve a quien abrió */
      }
    });
    document.addEventListener("click", function (e) {
      if (barra.classList.contains("menu-abierto") && !barra.contains(e.target)) abrir(false);
    });
    /* Al cruzar a ancho el panel deja de existir. Si el estado quedara
       puesto, volver a angosto lo mostraría abierto sin que nadie lo pidiera. */
    var anchoNav = window.matchMedia("(min-width: 62rem)");
    var resetMenu = function () { if (anchoNav.matches) abrir(false); };
    if (anchoNav.addEventListener) anchoNav.addEventListener("change", resetMenu);
    else if (anchoNav.addListener) anchoNav.addListener(resetMenu);
  }

  /* Anclas internas: el click SIEMPRE aterriza, aunque el hash ya sea el
     mismo (el navegador ignora ese caso y el botón se siente muerto). */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var destino = document.getElementById(a.getAttribute("href").slice(1));
      if (!destino) return;
      e.preventDefault();
      history.pushState(null, "", a.getAttribute("href"));
      destino.scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto" : "smooth"
      });
    });
  });

  /* Formulario: envía por /api/contact (Resend, clave en el servidor).
     Si el endpoint no está o falla, LO DICE y deja el mensaje escrito
     donde está. ⛔ Ya NO abre un compositor de correo (orden de Carlos,
     2026-08-17: nadie manda correos así, y la dirección dejó de ser
     enlace en todo el sitio). El visitante nunca pierde su mensaje ni
     recibe un "enviado" falso: esa parte no se negocia.
     OBLIGATORIOS (2026-08-17): nombre, correo, agencia y mensaje. Rol y
     teléfono pasaron a opcionales — seis campos obligatorios para un primer
     hola cuestan respuestas, y el teléfono se pide solo a quien prefiere
     que lo llamen. El servidor (api/contact.js) exige la MISMA lista. */
  var form = document.getElementById("form-contacto");
  if (form) {
    var v = function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      return el ? el.value.trim() : "";
    };
    /* La caída honesta: dice que falló, NO borra lo escrito y da la
       dirección para copiarla (un toque largo la selecciona entera). */
    var caidaHonesta = function (st) {
      st.textContent = "The direct send didn't go through — nothing you wrote was " +
        "lost, it's still in the form. Try again in a moment, or write to ";
      var dir = document.createElement("span");
      dir.className = "correo";
      dir.textContent = "hello@reasonedweb.com";
      st.appendChild(dir);
      st.appendChild(document.createTextNode("."));
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = form.querySelector(".form-status");
      st.dataset.live = "1";
      var faltan = ["name", "email", "company", "message"].filter(function (n) {
        return !v(n);
      });
      if (faltan.length) {
        st.textContent = "Still needed: " + faltan.join(", ") + ".";
        var primero = form.querySelector('[name="' + faltan[0] + '"]');
        if (primero) primero.focus();
        return;
      }
      st.textContent = "Sending…";
      var boton = form.querySelector("button.enviar");
      boton.disabled = true;
      fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: v("name"), email: v("email"), company: v("company"),
          role: v("role"), phone: v("phone"), ships: v("ships"),
          message: v("message"), website: v("website")
        })
      }).then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      }).then(function () {
        st.textContent = "Sent. I answer within one business day — you'll hear from hello@reasonedweb.com.";
        form.reset();
        boton.disabled = false;
      }).catch(function () {
        boton.disabled = false;
        caidaHonesta(st);
      });
    });
  }
})();
