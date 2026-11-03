(function () {
  if (window.__jlccInquiryFormLoaded) { return; }
  window.__jlccInquiryFormLoaded = true;

  var ACTION = "https://formsubmit.co/xxy13992859166@gmail.com";
  var NEXT = "https://xxy13992859166-ops.github.io/suncable-website/thankyou.html";

  function mount() {
    if (document.querySelector("form[action*='formsubmit.co']")) { return; }
    if (document.getElementById("jlcc-inquiry")) { return; }

    var style = document.createElement("style");
    style.textContent = [
      "#jlcc-inquiry{background:#0f172a;color:#e8eef8;padding:48px 16px;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}",
      "#jlcc-inquiry .jlcc-wrap{max-width:960px;margin:0 auto}",
      "#jlcc-inquiry h2{margin:0 0 8px;font-size:26px;line-height:1.3;color:#fff}",
      "#jlcc-inquiry p.jlcc-sub{margin:0 0 22px;color:#a9b8cc;font-size:14px}",
      "#jlcc-inquiry .jlcc-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px}",
      "#jlcc-inquiry .jlcc-field{flex:1 1 220px;display:flex;flex-direction:column}",
      "#jlcc-inquiry label{font-size:12px;color:#9fb0c7;margin-bottom:6px;letter-spacing:.02em}",
      "#jlcc-inquiry input,#jlcc-inquiry textarea{width:100%;box-sizing:border-box;padding:11px 12px;border-radius:8px;border:1px solid #26354a;background:#152136;color:#eef3fa;font-size:14px}",
      "#jlcc-inquiry input:focus,#jlcc-inquiry textarea:focus{outline:none;border-color:#3b82f6}",
      "#jlcc-inquiry textarea{min-height:110px;resize:vertical}",
      "#jlcc-inquiry button{margin-top:6px;width:100%;padding:13px 18px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-size:15px;font-weight:600;cursor:pointer}",
      "#jlcc-inquiry button:hover{background:#1d4ed8}",
      "#jlcc-inquiry .jlcc-note{margin-top:12px;font-size:12px;color:#8fa2ba}",
      "#jlcc-inquiry .jlcc-honey{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}"
    ].join("");
    document.head.appendChild(style);

    var section = document.createElement("section");
    section.id = "jlcc-inquiry";
    section.innerHTML = [
      '<div class="jlcc-wrap">',
      "<h2>Request a Quote</h2>",
      '<p class="jlcc-sub">Send your specification and quantity — we reply with price, lead time and packing.</p>',
      '<form action="' + ACTION + '" method="POST">',
      '<input type="hidden" name="_subject" value="Inquiry from ' + location.pathname + '">',
      '<input type="hidden" name="_captcha" value="false">',
      '<input type="hidden" name="_template" value="table">',
      '<input type="hidden" name="_autoresponse" value="Thanks for your inquiry - we have received it. Alice, our sales manager, replies within 2 business hours (Mon-Sat, 08:00-20:00 GMT+8).\n\nTo get pricing in the first reply, please send:\n1) cable type and size (e.g. H1Z2Z2-K 1x6mm2)\n2) quantity in metres\n3) destination port or delivery city\n\nNeed it faster? WhatsApp +86 153 3900 5193, or just reply to this email.\n\nJLCC - JunlinChicheng Metal Products Group Co., Ltd.">',
      '<input type="hidden" name="_next" value="' + NEXT + '">',
      '<input type="hidden" name="source_page" value="' + location.href + '">',
      '<div class="jlcc-honey"><label>Do not fill</label><input type="text" name="_honey" tabindex="-1" autocomplete="off"></div>',
      '<div class="jlcc-row">',
      '<div class="jlcc-field"><label>Your Name *</label><input type="text" name="name" required placeholder="John Smith"></div>',
      '<div class="jlcc-field"><label>Company</label><input type="text" name="company" placeholder="Company name"></div>',
      "</div>",
      '<div class="jlcc-row">',
      '<div class="jlcc-field"><label>Email *</label><input type="email" name="email" required placeholder="you@company.com"></div>',
      '<div class="jlcc-field"><label>WhatsApp / Phone</label><input type="text" name="phone" placeholder="+1 234 567 8900"></div>',
      "</div>",
      '<div class="jlcc-row"><div class="jlcc-field"><label>Requirement *</label><textarea name="message" required placeholder="Cable type, size, quantity, destination port, target price..."></textarea></div></div>',
      '<button type="submit">Send Inquiry</button>',
      '<p class="jlcc-note">Typical reply within 2 hours on business days. Or WhatsApp +86 153 3900 5193.</p>',
      "</form>",
      "</div>"
    ].join("");

    var footer = document.querySelector("footer");
    if (footer && footer.parentNode) {
      footer.parentNode.insertBefore(section, footer);
    } else {
      document.body.appendChild(section);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
