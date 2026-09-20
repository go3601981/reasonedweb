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
     que lo llamen. El servidor (api/contact.js) exige la MISMA lista.
     ⛔ 2026-09-20: un 400 NO es una caída. El servidor rechaza un correo
     mal escrito con 400 y esto lo trataba como fallo de red: el visitante
     leía «try again in a moment», que además de falso es inútil — esperar
     no arregla un correo mal tecleado. Un error del visitante se le dice
     para que lo corrija; la caída honesta queda SOLO para lo que de verdad
     falló del lado del servidor. */
  var form = document.getElementById("form-contacto");
  if (form) {
    /* La MISMA regex que api/contact.js — es la última puerta, la que decide
       si el servidor aceptará. Las reglas de abajo son más finas que ella
       (dicen QUÉ falta), pero ninguna puede dar por bueno lo que esta niega. */
    var CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    /* Los nombres de campo del servidor no son los rótulos que el visitante
       ve: «company» no aparece escrito en ninguna parte de la página. */
    var ROTULO = {
      name: "name", email: "work email",
      company: "agency or studio", phone: "phone", message: "what you need"
    };

    /* Iconografía dibujada — cero emoji (regla del sitio). Un disco sólido
       con la marca calada encima: a 16 px un trazo fino se deshace, un
       disco no. El color lo pone currentColor, así el icono nunca puede
       desafinar del texto al que acompaña. */
    var SVG = "http://www.w3.org/2000/svg";
    function icono(tipo) {
      var s = document.createElementNS(SVG, "svg");
      s.setAttribute("viewBox", "0 0 16 16");
      s.setAttribute("aria-hidden", "true");
      s.setAttribute("focusable", "false");
      var c = document.createElementNS(SVG, "circle");
      c.setAttribute("cx", "8"); c.setAttribute("cy", "8"); c.setAttribute("r", "8");
      c.setAttribute("fill", "currentColor");
      s.appendChild(c);
      if (tipo === "ok") {
        var p = document.createElementNS(SVG, "path");
        p.setAttribute("d", "M4 8.3 6.8 11.1 12 5.4");
        p.setAttribute("fill", "none"); p.setAttribute("stroke", "#F3F4F3");
        p.setAttribute("stroke-width", "2"); p.setAttribute("stroke-linecap", "square");
        s.appendChild(p);
      } else {
        [["7", "3.2", "2", "6.2"], ["7", "10.8", "2", "2"]].forEach(function (r) {
          var b = document.createElementNS(SVG, "rect");
          b.setAttribute("x", r[0]); b.setAttribute("y", r[1]);
          b.setAttribute("width", r[2]); b.setAttribute("height", r[3]);
          b.setAttribute("fill", "#F3F4F3");
          s.appendChild(b);
        });
      }
      return s;
    }

    /* Una regla por campo. Devuelve null si está bien, o EL motivo concreto
       — no «invalid». Un mensaje que no dice qué arreglar obliga a adivinar,
       y quien adivina se va. El correo tiene un motivo por cada forma de
       romperlo porque es el campo que decide si hay respuesta. */
    var REGLAS = {
      name: function (t) {
        if (!t) return "I need a name to put on the reply.";
        if (t.length < 2) return "That's a letter, not a name — give me the one you go by.";
        return null;
      },
      email: function (t) {
        if (!t) return "I need a work email — it's where my answer goes.";
        if (/\s/.test(t)) return "There's a space in that address. Take it out and send again.";
        var partes = t.split("@");
        if (partes.length === 1) return "An email address needs an @ — like you@youragency.com.";
        if (partes.length > 2) return "That address has two @ signs in it.";
        if (!partes[0]) return "There's nothing before the @ — your name goes there.";
        var dominio = partes[1];
        if (!dominio) return "There's nothing after the @ — your agency's domain goes there.";
        if (dominio.indexOf(".") === -1)
          return "The part after the @ needs a domain ending, like youragency.com.";
        if (/\.$/.test(dominio) || /\.[^.]{1}$/.test(dominio))
          return "That domain looks unfinished — check the part after the last dot.";
        if (!CORREO.test(t)) return "That address doesn't look complete — check it and send again.";
        return null;
      },
      company: function (t) {
        if (!t) return "Which agency or studio is this for?";
        return null;
      },
      /* Opcional: en blanco está perfecto. Pero si hay algo escrito, o es un
         número al que se puede llamar o no sirve de nada — y quedarse callado
         ante «sadfsf» es guardar basura y fingir que se recibió un teléfono. */
      phone: function (t) {
        if (!t) return null;
        if ((t.match(/\d/g) || []).length < 7)
          return "That's not a number I could call. Write it in full, or leave it blank and I'll email.";
        return null;
      },
      message: function (t) {
        if (!t) return "Tell me what you need — one line is enough.";
        return null;
      }
    };
    var CAMPOS = Object.keys(REGLAS);

    var campo = function (n) { return form.querySelector('[name="' + n + '"]'); };
    var v = function (n) { var el = campo(n); return el ? el.value.trim() : ""; };
    var enfocar = function (n) { var el = campo(n); if (el) el.focus(); };

    /* Marcar y desmarcar. aria-invalid y el aviso visible se ponen y se
       quitan JUNTOS, en una sola función, para que no exista un estado donde
       el ojo vea un error y el lector de pantalla no (o al revés). */
    var marcar = function (n, motivo) {
      var el = campo(n);
      if (!el) return;
      var aviso = document.getElementById("err-" + n);
      if (motivo) {
        el.setAttribute("aria-invalid", "true");
        if (aviso) {
          aviso.textContent = "";
          aviso.appendChild(icono("error"));
          aviso.appendChild(document.createTextNode(motivo));
          aviso.hidden = false;
        }
      } else {
        el.removeAttribute("aria-invalid");
        if (aviso) { aviso.hidden = true; aviso.textContent = ""; }
      }
    };
    var revisar = function (n) {
      var motivo = REGLAS[n] ? REGLAS[n](v(n)) : null;
      marcar(n, motivo);
      return motivo;
    };
    var limpiarTodo = function () { CAMPOS.forEach(function (n) { marcar(n, null); }); };

    /* El resumen al pie. Junta los rótulos VISIBLES de lo que falla: quien
       llegó abajo del todo tiene que saber a qué subir sin cazar rectángulos
       rojos por la página. */
    var estado = function (st, tipo, texto, correo) {
      st.dataset.live = "1";
      if (tipo) st.dataset.estado = tipo; else delete st.dataset.estado;
      st.textContent = "";
      if (tipo) st.appendChild(icono(tipo));
      var caja = document.createElement("span");
      caja.appendChild(document.createTextNode(texto));
      if (correo) {
        var dir = document.createElement("span");
        dir.className = "correo";
        dir.textContent = "hello@reasonedweb.com";
        caja.appendChild(dir);
        caja.appendChild(document.createTextNode("."));
      }
      st.appendChild(caja);
    };
    var resumen = function (st, fallan) {
      var nombres = fallan.map(function (n) { return ROTULO[n] || n; });
      var lista = nombres.length > 1
        ? nombres.slice(0, -1).join(", ") + " and " + nombres[nombres.length - 1]
        : nombres[0];
      estado(st, "error", "Not sent yet. Check " + lista + ".");
    };
    /* La caída honesta: dice que falló, NO borra lo escrito y da la
       dirección para copiarla (un toque largo la selecciona entera). */
    var caidaHonesta = function (st) {
      estado(st, "error", "The direct send didn't go through — nothing you wrote was " +
        "lost, it's still in the form. Try again in a moment, or write to ", true);
    };

    /* CUÁNDO se revisa, que importa tanto como el qué:
       · al salir de un campo, solo si el visitante escribió algo — pasar de
         largo por un campo vacío no merece un regaño;
       · después del primer intento de envío, al salir de cualquier campo;
       · mientras teclea, SOLO para borrar una marca ya puesta. Nunca se
         estrena un error a mitad de palabra: «carlos@» está mal escrito y
         a la vez va camino de estar bien. */
    var intentado = false;
    CAMPOS.forEach(function (n) {
      var el = campo(n);
      if (!el) return;
      el.addEventListener("blur", function () {
        if (intentado || el.value.trim()) revisar(n);
      });
      el.addEventListener("input", function () {
        if (el.getAttribute("aria-invalid") === "true") revisar(n);
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = form.querySelector(".form-status");
      intentado = true;
      var fallan = CAMPOS.filter(function (n) { return revisar(n) !== null; });
      if (fallan.length) {
        resumen(st, fallan);
        enfocar(fallan[0]);
        return;
      }
      estado(st, null, "Sending…");
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
        /* El cuerpo se lee SIEMPRE: en un 400 es donde el servidor dice
           qué campo hay que corregir. Un cuerpo ilegible no inventa nada
           — cae en {} y acaba en la caída honesta. */
        return r.json().catch(function () { return {}; }).then(function (data) {
          return { status: r.status, ok: r.ok, data: data };
        });
      }).then(function (res) {
        boton.disabled = false;
        if (res.ok && res.data.ok === true) {
          estado(st, "ok", "Sent. I answer within one business day — you'll hear from ", true);
          form.reset();
          limpiarTodo();
          intentado = false;
          return;
        }
        /* 400 = el visitante puede arreglarlo ahora mismo, y el servidor dice
           cuál. Cualquier otra cosa (503 sin clave, 502 de Resend, red caída)
           sí es una caída. Esta rama solo se alcanza si el servidor y las
           reglas de arriba se separan: es la red de seguridad, no el camino. */
        if (res.status === 400 && res.data.error === "email") {
          marcar("email", "That address doesn't look complete — check it and send again.");
          resumen(st, ["email"]);
          enfocar("email");
          return;
        }
        if (res.status === 400 && res.data.error === "missing" &&
            (res.data.fields || []).length) {
          res.data.fields.forEach(function (n) { revisar(n); });
          resumen(st, res.data.fields);
          enfocar(res.data.fields[0]);
          return;
        }
        caidaHonesta(st);
      }).catch(function () {
        boton.disabled = false;
        caidaHonesta(st);
      });
    });
  }
})();
