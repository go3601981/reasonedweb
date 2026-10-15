(function () {
  "use strict";

  var filters = Array.prototype.slice.call(document.querySelectorAll("button.work-filter"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".work-card[data-category]"));
  var status = document.getElementById("work-status");
  if (!filters.length || !cards.length || !status) return;

  function labelFor(category) {
    var match = filters.find(function (button) {
      return button.getAttribute("data-filter") === category;
    });
    return match ? match.textContent.trim() : category;
  }

  function apply(category) {
    var visible = 0;
    cards.forEach(function (card) {
      var show = !category || card.getAttribute("data-category") === category;
      card.hidden = !show;
      if (show) visible += 1;
    });
    filters.forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.getAttribute("data-filter") === category));
    });
    status.textContent = category
      ? "Showing " + visible + " of " + cards.length + " projects in " + labelFor(category) + ". Activate the selected filter again to show all work."
      : "Showing all " + cards.length + " projects.";
  }

  filters.forEach(function (button, index) {
    button.addEventListener("click", function () {
      var selected = button.getAttribute("aria-pressed") === "true";
      apply(selected ? "" : button.getAttribute("data-filter"));
    });
    button.addEventListener("keydown", function (event) {
      var next = null;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") next = (index + 1) % filters.length;
      if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = (index - 1 + filters.length) % filters.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = filters.length - 1;
      if (event.key === "Escape") {
        apply("");
        button.focus();
        event.preventDefault();
        return;
      }
      if (next !== null) {
        filters[next].focus();
        event.preventDefault();
      }
    });
  });

  apply("");
})();
