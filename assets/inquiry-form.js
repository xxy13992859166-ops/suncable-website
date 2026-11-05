/* Inquiry form v2 - resilient submit.
   Posts by fetch; if the relay is unreachable or rejects the submission the
   visitor gets a prefilled email and WhatsApp fallback instead of a fake
   thankyou page. Native POST still works without JS. */
(function () {
  if (window.__jlccInquiryFormLoaded) { return; }
  window.__jlccInquiryFormLoaded = true;

  var EMAIL = 'xxy13992859166@gmail.com';
  var ACTION = 'https://formsubmit.co/' + EMAIL;
  var AJAX = 'https://formsubmit.co/ajax/' + EMAIL;
  var WA = 'https://wa.me/8615339005193';
  var NEXT = 'https://xxy13992859166-ops.github.io/suncable-website/thankyou.html';

  function field(form, n) {
    var el = form.querySelector('[name="' + n + '"]');
    return el ? String(el.value || '') : '';
  }

  function showFallback(form, why) {
    var name = field(form, 'name'), company = field(form, 'company');
    var email = field(form, 'email'), phone = field(form, 'phone');
    var msg = field(form, 'message');
    var subject = 'Solar cable inquiry - ' + (company || name || 'website');
    var body = 'Name: ' + name + '\nCompany: ' + company + '\nEmail: ' + email +
      '\nPhone: ' + phone + '\n\n' + msg + '\n\nSent from: ' + location.href;
    var mail = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);
    var wa = WA + '?text=' + encodeURIComponent('Inquiry from ' + location.pathname + '\n' + body);

    var old = document.getElementById('jlcc-fallback');
    if (old) { old.parentNode.removeChild(old); }
    var box = document.createElement('div');
    box.id = 'jlcc-fallback';
    box.setAttribute('style', 'margin-top:14px;padding:14px 16px;border-radius:8px;background:#fff7ed;border:1px solid #f0b46b;color:#7a4a10;font-size:14px;line-height:1.55');
    box.innerHTML = '<strong>Our form relay did not respond.</strong><br>' +
      'Your details are still in the form. Send them directly and we will reply the same way:' +
      '<div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">' +
      '<a href="' + mail + '" style="padding:9px 14px;border-radius:6px;background:#2563eb;color:#fff;text-decoration:none;font-weight:600">Email us (prefilled)</a>' +
      '<a href="' + wa + '" target="_blank" rel="noopener" style="padding:9px 14px;border-radius:6px;background:#16a34a;color:#fff;text-decoration:none;font-weight:600">WhatsApp</a>' +
      '</div>';
    var btn = form.querySelector('button');
    if (btn && btn.parentNode) { btn.parentNode.insertBefore(box, btn.nextSibling); }
    else { form.appendChild(box); }
  }

  function onSubmit(e) {
    var form = e.target;
    if (!form || form.getAttribute('action') === null) { return; }
    e.preventDefault();
    var btn = form.querySelector('button');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
    var ctrl = (typeof AbortController !== 'undefined') ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) { ctrl.abort(); } }, 12000);
    var opts = { method: 'POST', body: new FormData(form) };
    if (ctrl) { opts.signal = ctrl.signal; }
    fetch(AJAX, opts).then(function (r) {
      clearTimeout(timer);
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      return r.json().catch(function () { return {}; });
    }).then(function (j) {
      if (j && (j.success === false || j.success === 'false')) {
        throw new Error('relay rejected');
      }
      location.href = NEXT;
    }).catch(function () {
      clearTimeout(timer);
      if (btn) { btn.disabled = false; btn.textContent = label || 'Send Inquiry'; }
      showFallback(form, 'relay');
    });
  }

  function mount() {
    if (document.getElementById('jlcc-inquiry')) { return; }
    var section = document.createElement('section');
    section.id = 'jlcc-inquiry';
    section.innerHTML = [
      '<div style="max-width:960px;margin:0 auto">',
      '<h2>Request a Quote</h2>',
      '<p style="margin:0 0 18px;color:#475569;font-size:14px">Send your specification and quantity - we reply with price, lead time and packing.</p>',
      '<form action="' + ACTION + '" method="POST">',
      '<input type="hidden" name="_subject" value="Inquiry from ' + location.pathname + '">',
      '<input type="hidden" name="_captcha" value="false">',
      '<input type="hidden" name="_template" value="table">',
      '<input type="hidden" name="_next" value="' + NEXT + '">',
      '<input type="hidden" name="source_page" value="' + location.href + '">',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Your Name *<br><input type="text" name="name" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Company<br><input type="text" name="company" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Email *<br><input type="email" name="email" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">WhatsApp / Phone<br><input type="text" name="phone" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<label style="display:block;font-size:12px;color:#334155">Requirement *<br><textarea name="message" required style="width:100%;min-height:110px;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></textarea></label>',
      '<button type="submit" style="margin-top:12px;padding:12px 22px;border:0;border-radius:6px;background:#2563eb;color:#fff;font-size:15px;font-weight:600;cursor:pointer">Send Inquiry</button>',
      '<p style="margin:10px 0 0;font-size:12px;color:#64748b">Typical reply within 2 hours on business days. Or WhatsApp +86 153 3900 5193.</p>',
      '</form>',
      '</div>'
    ].join('');
    section.setAttribute('style', 'padding:40px 16px;background:#f1f5f9;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif');
    var footer = document.querySelector('footer');
    if (footer && footer.parentNode) { footer.parentNode.insertBefore(section, footer); }
    else { document.body.appendChild(section); }
    var form = section.querySelector('form');
    if (form) { form.addEventListener('submit', onSubmit); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
