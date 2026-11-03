(function () {
  if (window.__jlccStickyCta) { return; }
  window.__jlccStickyCta = true;

  var WA = "https://wa.me/8615339005193?text=Hi%2C%20I%20need%20a%20quote%20for%20solar%20cables.";
  var MAIL = "mailto:xxy13992859166@gmail.com?subject=Solar%20Cable%20Quote";

  function build() {
    if (document.getElementById("jlcc-cta-bar")) { return; }

    var style = document.createElement("style");
    style.textContent = [
      "#jlcc-cta-bar{position:fixed;left:0;right:0;bottom:0;z-index:9998;display:none;gap:8px;padding:10px 12px;background:rgba(9,17,29,.97);border-top:1px solid #1e2d42;box-shadow:0 -6px 24px rgba(0,0,0,.35);font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}",
      "#jlcc-cta-bar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;padding:12px 8px;border-radius:10px;font-size:15px;font-weight:700;text-decoration:none;line-height:1}",
      "#jlcc-cta-bar a.jlcc-wa{background:#25d366;color:#06240f}",
      "#jlcc-cta-bar a.jlcc-q{background:#2563eb;color:#fff}",
      "#jlcc-cta-bar a:active{transform:scale(.99)}",
      "body{padding-bottom:76px}",
      "@media(min-width:821px){#jlcc-cta-bar{display:none!important}body{padding-bottom:0!important}}"
    ].join("");
    document.head.appendChild(style);

    var bar = document.createElement("div");
    bar.id = "jlcc-cta-bar";
    bar.style.display = "flex";
    bar.innerHTML =
      '<a class="jlcc-wa" href="' + WA + '" target="_blank" rel="noopener">WhatsApp</a>' +
      '<a class="jlcc-q" href="#jlcc-inquiry">Get Quote</a>';
    document.body.appendChild(bar);

    var q = bar.querySelector(".jlcc-q");
    q.addEventListener("click", function (e) {
      var target = document.getElementById("jlcc-inquiry") || document.querySelector("form[action*='formsubmit.co']");
      if (!target) { return; }
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      var first = target.querySelector("input[type=text],input[type=email],textarea");
      if (first) { setTimeout(function () { try { first.focus({ preventScroll: true }); } catch (err) {} }, 600); }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
