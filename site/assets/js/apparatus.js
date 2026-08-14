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
