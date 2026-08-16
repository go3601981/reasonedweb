/* Ulric de Varens — Catalogue 2026 · deck navigation */
(function () {
  "use strict";

  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var total = slides.length;
  var cur = -1;

  var prevBtn = document.getElementById("prevBtn");
  var nextBtn = document.getElementById("nextBtn");
  var curEl = document.getElementById("curSlide");
  var totEl = document.getElementById("totSlide");
  var fill = document.getElementById("progressFill");

  function pad(n) { return n < 10 ? "0" + n : "" + n; }

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* count-up numbers: <el data-count="7.5" data-dec="1" data-prefix="+"
     data-suffix="M+" data-comma> — re-runs on every slide visit */
  function formatCount(el, value) {
    var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
    var txt;
    if (el.hasAttribute("data-thousands")) {
      txt = Math.round(value).toLocaleString("en-US");
    } else {
      txt = value.toFixed(dec);
      if (el.hasAttribute("data-comma")) txt = txt.replace(".", ",");
    }
    return (el.getAttribute("data-prefix") || "") + txt + (el.getAttribute("data-suffix") || "");
  }
  function runCounters(slide) {
    var els = slide.querySelectorAll("[data-count]");
    Array.prototype.forEach.call(els, function (el) {
      var target = parseFloat(el.getAttribute("data-count"));
      if (el._raf) cancelAnimationFrame(el._raf);
      el.classList.remove("count-done");
      if (reducedMotion) { el.textContent = formatCount(el, target); return; }
      var t0 = null, dur = 1500;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur);
        /* ease-out with a slight overshoot that settles back */
        var s = 1.70158;
        var q = p - 1;
        var eased = q * q * ((s + 1) * q + s) + 1;
        el.textContent = formatCount(el, Math.max(0, target * eased));
        if (p < 1) {
          el._raf = requestAnimationFrame(step);
        } else {
          el.textContent = formatCount(el, target);
          el.classList.add("count-done");
        }
      }
      el._raf = requestAnimationFrame(step);
    });
  }

  /* progressive image loading — slides 3+ ship their <img> as data-src (index.html);
     the slide being shown is hydrated synchronously on arrival, then the rest stream
     in nearest-first order with a forward bias (2 ahead, 1 behind), one slide at a
     time, so bandwidth goes where the presenter is heading instead of 130 images
     racing at once. Deep links (#N) hydrate N first. */
  var hydrated = [];
  var pumping = false;
  function hydrate(i) {
    if (i < 0 || i >= total || hydrated[i]) return [];
    hydrated[i] = true;
    var imgs = Array.prototype.slice.call(slides[i].querySelectorAll("img[data-src]"));
    imgs.forEach(function (img) {
      img.decoding = "async";
      img.src = img.getAttribute("data-src");
      img.removeAttribute("data-src");
    });
    return imgs;
  }
  function nextToHydrate() {
    var f = cur + 1, b = cur - 1, step = 0;
    while (f < total || b >= 0) {
      if (step % 3 === 2) { if (b >= 0 && !hydrated[b]) return b; b--; }
      else { if (f < total && !hydrated[f]) return f; f++; }
      step++;
    }
    return -1;
  }
  function whenLoaded(imgs, cb) {
    var left = imgs.length, done = false;
    function one() { if (!done && --left <= 0) { done = true; cb(); } }
    if (!left) { cb(); return; }
    imgs.forEach(function (img) {
      if (img.complete) { one(); return; }
      img.addEventListener("load", one, { once: true });
      img.addEventListener("error", one, { once: true });
    });
    setTimeout(function () { if (!done) { done = true; cb(); } }, 8000); /* never let a stall block the queue */
  }
  function pump() {
    if (pumping) return;
    var i = nextToHydrate();
    if (i < 0) return;
    pumping = true;
    whenLoaded(hydrate(i), function () { pumping = false; pump(); });
  }

  /* per-slide <video> support: play while active, pause when leaving */
  function manageVideos(oldSlide, newSlide) {
    if (oldSlide) {
      Array.prototype.forEach.call(oldSlide.querySelectorAll("video"), function (v) { v.pause(); });
    }
    if (newSlide) {
      Array.prototype.forEach.call(newSlide.querySelectorAll("video"), function (v) {
        v.muted = true;
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
      });
    }
  }

  function goCore(n) {
    n = Math.max(0, Math.min(total - 1, n));
    if (n === cur) return;
    var prev = cur >= 0 ? slides[cur] : null;
    if (prev) prev.classList.remove("active");
    hydrate(n); /* target slide's images first, before it becomes visible */
    manageVideos(prev, slides[n]);
    cur = n;
    var s = slides[cur];
    s.classList.add("active");
    pump(); /* then keep streaming neighbours from the new position */
    s.scrollTop = 0;

    runCounters(s);

    curEl.textContent = pad(cur + 1);
    fill.style.width = ((cur + 1) / total) * 100 + "%";
    updateChapter(cur);
    prevBtn.disabled = cur === 0;
    nextBtn.disabled = cur === total - 1;
    if (history.replaceState) history.replaceState(null, "", "#" + (cur + 1));
  }

  /* manual navigation stops autoplay; the timer itself uses goAuto */
  function go(n) { stopAutoplay(); goCore(n); }
  function goAuto(n) { goCore(n); }

  function next() { go(cur + 1); }
  function prev() { go(cur - 1); }

  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);

  document.addEventListener("keydown", function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    switch (e.key) {
      case "ArrowRight": case "PageDown": case " ": next(); e.preventDefault(); break;
      case "ArrowLeft": case "PageUp": prev(); e.preventDefault(); break;
      case "Home": go(0); e.preventDefault(); break;
      case "End": go(total - 1); e.preventDefault(); break;
      case "p": case "P": toggleAutoplay(); break;
    }
  });

  /* touch swipe */
  var tx = null, ty = null;
  document.addEventListener("touchstart", function (e) {
    tx = e.changedTouches[0].clientX;
    ty = e.changedTouches[0].clientY;
  }, { passive: true });
  document.addEventListener("touchend", function (e) {
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx;
    var dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      if (dx < 0) next(); else prev();
    }
    tx = ty = null;
  }, { passive: true });

  /* debounced wheel */
  var wheelLock = 0;
  document.addEventListener("wheel", function (e) {
    var now = Date.now();
    if (now - wheelLock < 700) return;
    var active = slides[cur];
    /* don't hijack scrolling when slide content itself scrolls (mobile) */
    if (active && active.scrollHeight > active.clientHeight + 4) return;
    if (Math.abs(e.deltaY) < 12) return;
    wheelLock = now;
    if (e.deltaY > 0) next(); else prev();
  }, { passive: true });

  /* subsidiary chips grow their country on the slide-6 map */
  Array.prototype.forEach.call(document.querySelectorAll(".chip[data-sub]"), function (chip) {
    var country = document.querySelector(".fragw[data-sub='" + chip.getAttribute("data-sub") + "']");
    if (!country) return;
    chip.addEventListener("mouseenter", function () { country.classList.add("grown"); });
    chip.addEventListener("mouseleave", function () { country.classList.remove("grown"); });
  });

  /* fixed-canvas stages: scale 1920x1080 design space to fit the deck area */
  var deck = document.getElementById("deck");
  function fitStages() {
    var s = Math.min(deck.clientWidth / 1920, deck.clientHeight / 1080);
    document.documentElement.style.setProperty("--stage-scale", s);
  }
  window.addEventListener("resize", fitStages);
  fitStages();

  /* chapters: progress ticks + live label */
  var CHAPTERS = [
    { start: 1, name: "La maison" },
    { start: 3, name: "Savoir-faire" },
    { start: 6, name: "Global reach" },
    { start: 11, name: "USA" },
    { start: 15, name: "Marketing" },
    { start: 18, name: "In stores" },
    { start: 21, name: "Catalogue" },
    { start: 33, name: "Contact" }
  ];
  var chapterEl = document.getElementById("chapterLabel");
  var progressEl = document.querySelector(".progress");
  CHAPTERS.forEach(function (c) {
    if (c.start === 1) return;
    var tick = document.createElement("span");
    tick.className = "progress__tick";
    tick.style.left = ((c.start - 1) / total * 100) + "%";
    progressEl.appendChild(tick);
  });
  function updateChapter(n) {
    var name = "";
    CHAPTERS.forEach(function (c) { if (n + 1 >= c.start) name = c.name; });
    if (chapterEl.textContent === name) return;
    chapterEl.classList.add("swap");
    setTimeout(function () {
      chapterEl.textContent = name;
      chapterEl.classList.remove("swap");
    }, 180);
  }

  /* presenter autoplay: P toggles a 12s loop; any manual action stops it */
  var autoTimer = null;
  function stopAutoplay() {
    if (!autoTimer) return;
    clearInterval(autoTimer);
    autoTimer = null;
    document.body.classList.remove("autoplaying");
  }
  function toggleAutoplay() {
    if (autoTimer) { stopAutoplay(); return; }
    document.body.classList.add("autoplaying");
    autoTimer = setInterval(function () {
      goAuto(cur + 1 >= total ? 0 : cur + 1);
    }, 12000);
  }

  /* init — supports #N and ?slide=N deep links */
  totEl.textContent = pad(total);
  var start = 0;
  var q = /[?&]slide=(\d+)/.exec(location.search);
  var h = /^#(\d+)$/.exec(location.hash);
  if (q) start = parseInt(q[1], 10) - 1;
  else if (h) start = parseInt(h[1], 10) - 1;
  go(isNaN(start) ? 0 : start); /* goCore hydrates the start slide and starts the pump */
})();
