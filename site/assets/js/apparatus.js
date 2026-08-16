/* Aparato de notas al pie — la interacción-firma del sitio.
   Mejora progresiva: sin JS, todas las notas quedan visibles como notas al
   pie de sección (ninguna afirmación pierde su porqué). Con JS, se pliegan
   y cada marcador [n] abre la suya. */
(function () {
  document.documentElement.classList.add("js");
  var refs = document.querySelectorAll("button.fn-ref");
  for (var i = 0; i < refs.length; i++) {
    (function (ref) {
      var note = document.getElementById(ref.getAttribute("aria-controls"));
      if (!note) return;
      note.hidden = true;
      ref.setAttribute("aria-expanded", "false");
      ref.addEventListener("click", function () {
        var open = note.hidden;
        note.hidden = !open;
        ref.setAttribute("aria-expanded", String(open));
        if (open) note.scrollIntoView({ block: "nearest", behavior: "smooth" });
      });
    })(refs[i]);
  }

  /* Revelado al hacer scroll — SOLO imágenes (el texto jamás se anima).
     IntersectionObserver, nunca listener de scroll; reduced-motion lo apaga
     por CSS. Sin IO, las imágenes simplemente quedan visibles. */
  if ("IntersectionObserver" in window) {
    var shots = document.querySelectorAll("img.shot");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("en-escena");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    for (var j = 0; j < shots.length; j++) {
      shots[j].setAttribute("data-reveal", "");
      io.observe(shots[j]);
    }
  }

  /* Formulario: envía por /api/contact (Resend, clave en el servidor).
     Si el endpoint no está o falla, cae al compositor mailto y LO DICE —
     el visitante nunca pierde su mensaje ni recibe un "enviado" falso. */
  var form = document.getElementById("form-contacto");
  if (form) {
    var v = function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      return el ? el.value.trim() : "";
    };
    var mailtoFallback = function (st) {
      var subject = "Availability inquiry — " + (v("company") || v("name"));
      var body =
        "Name: " + v("name") + "\nEmail: " + v("email") +
        "\nAgency/studio: " + v("company") + "\nRole: " + v("role") +
        "\nPhone: " + v("phone") + "\nThey ship: " + v("ships") +
        "\n\n" + v("message");
      st.textContent =
        "Direct send is unavailable right now — your email app should open with everything filled in for hello@reasonedweb.com.";
      window.location.href =
        "mailto:hello@reasonedweb.com?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = form.querySelector(".form-status");
      st.dataset.live = "1";
      var faltan = ["name", "email", "company", "role", "phone", "message"].filter(function (n) {
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
        mailtoFallback(st);
      });
    });
  }
})();
