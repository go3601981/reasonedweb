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

  /* Formulario: estado honesto mientras el buzón del estudio se aprovisiona.
     Nada se envía y se dice que nada se envió. */
  var form = document.querySelector("form[data-interim]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = form.querySelector(".form-status");
      st.dataset.live = "1";
      st.textContent =
        "The studio inbox is being provisioned — this form activates when it goes live. Nothing was sent.";
    });
  }
})();
