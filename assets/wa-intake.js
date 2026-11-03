/*
 * Turns every WhatsApp link on the page into a structured inquiry opener.
 *
 * Instead of a vague "Hi, I'm interested in your solar cables", the buyer's
 * first message arrives with the product name, the landing page and blanks for
 * country / spec / quantity. That makes the inbound conversation qualifying
 * from message #1 and keeps the source page traceable without any WhatsApp API.
 */
(function () {
  if (window.__jlccWaIntake) { return; }
  window.__jlccWaIntake = true;

  function productName() {
    var blocks = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < blocks.length; i++) {
      try {
        var data = JSON.parse(blocks[i].textContent);
        if (data && data["@type"] === "Product" && data.name) {
          return String(data.name).split("|")[0].trim();
        }
      } catch (err) {}
    }
    var h1 = document.querySelector("h1");
    if (h1) {
      var heading = h1.textContent.replace(/\s+/g, " ").trim();
      if (heading) { return heading.split("\u2014")[0].split("|")[0].trim(); }
    }
    var title = (document.title || "").split("|")[0].replace(/\s+/g, " ").trim();
    return title || "solar cables";
  }

  function sourceTag() {
    var query = new URLSearchParams(location.search);
    var source = query.get("utm_source");
    var medium = query.get("utm_medium");
    var content = query.get("utm_content");
    var parts = [];
    if (source) { parts.push(source); }
    if (medium) { parts.push(medium); }
    if (content) { parts.push(content); }
    if (parts.length) { return parts.join("/"); }
    return query.get("src") || "";
  }

  function message() {
    var path = location.pathname.replace("/suncable-website", "") || "/";
    var tag = sourceTag();
    return [
      "Hi, I'd like a quote for " + productName() + ".",
      "Page: " + path + (tag ? " (via " + tag + ")" : ""),
      "Country: ",
      "Size / spec: ",
      "Quantity (m): "
    ].join("\n");
  }

  function rewrite(link) {
    if (link.getAttribute("data-wa-intake")) { return; }
    var href = link.getAttribute("href") || "";
    if (href.indexOf("wa.me/") === -1) { return; }
    link.setAttribute("data-wa-intake", "1");
    link.setAttribute("href", href.split("?")[0] + "?text=" + encodeURIComponent(message()));
    link.setAttribute("rel", "noopener");
  }

  var pending = false;

  function scan() {
    pending = false;
    var links = document.querySelectorAll('a[href*="wa.me/"]');
    for (var i = 0; i < links.length; i++) { rewrite(links[i]); }
  }

  function schedule() {
    if (pending) { return; }
    pending = true;
    setTimeout(scan, 60);
  }

  function start() {
    scan();
    if (window.MutationObserver && document.body) {
      new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
