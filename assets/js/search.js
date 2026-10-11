// Site search: loads /search.json (built by Jekyll) and lists the pages and
// posts that contain every word of the query, best matches first.
(function () {
  var script = document.currentScript;
  var input = document.getElementById("search-page-q");
  var status = document.getElementById("search-status");
  var list = document.getElementById("search-results");
  var query = (new URLSearchParams(location.search).get("q") || "").trim();
  input.value = query;
  var headerInput = document.getElementById("site-search-q");
  if (headerInput) headerInput.value = query;
  if (!query) { input.focus(); return; }

  var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  status.textContent = "Searching…";

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  // strip_html leaves entities such as &ndash; in the text; decode them.
  var decoder = document.createElement("textarea");
  function decode(s) { decoder.innerHTML = s; return decoder.value; }
  function escapeRegExp(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  var highlight = new RegExp("(" + terms.map(escapeRegExp).join("|") + ")", "gi");
  function mark(s) { return escapeHtml(s).replace(highlight, "<mark>$1</mark>"); }

  function count(haystack, term) {
    var n = 0, i = haystack.indexOf(term);
    while (i !== -1) { n++; i = haystack.indexOf(term, i + term.length); }
    return n;
  }
  function snippet(text, term) {
    var i = text.toLowerCase().indexOf(term);
    if (i === -1) i = 0;
    var start = Math.max(0, i - 80);
    var s = text.slice(start, start + 220);
    return (start > 0 ? "…" : "") + s + (start + 220 < text.length ? "…" : "");
  }

  fetch(script.dataset.index)
    .then(function (r) { return r.json(); })
    .then(function (docs) {
      docs.forEach(function (doc) { doc.text = decode(doc.text); doc.title = decode(doc.title); });
      var results = [];
      docs.forEach(function (doc) {
        var title = doc.title.toLowerCase(), text = doc.text.toLowerCase(), score = 0;
        for (var i = 0; i < terms.length; i++) {
          var inTitle = count(title, terms[i]), inText = count(text, terms[i]);
          if (!inTitle && !inText) return;
          score += inTitle * 10 + Math.min(inText, 20);
        }
        results.push({ doc: doc, score: score });
      });
      results.sort(function (a, b) { return b.score - a.score; });

      status.textContent = results.length
        ? results.length + (results.length === 1 ? " result" : " results") + " for “" + query + "”"
        : "No results for “" + query + "”. Try fewer or different words.";
      list.innerHTML = results.map(function (r) {
        return '<li class="card"><p class="card__meta">' + (r.doc.date ? escapeHtml(r.doc.date) : "Page") + "</p>" +
          '<h3 class="card__title"><a href="' + escapeHtml(r.doc.url) + '">' + mark(r.doc.title) + "</a></h3>" +
          "<p>" + mark(snippet(r.doc.text, terms[0])) + "</p></li>";
      }).join("");
    })
    .catch(function () { status.textContent = "Sorry, search couldn't load. Please try again."; });
})();
