/* Inquiry form v4 - relay-free.
   Nothing is posted to a third-party service, so no relay outage can swallow an
   inquiry. On submit the visitor's own details are composed into a ready-to-send
   message and a panel offers WhatsApp, their mail app, Gmail web compose,
   Outlook web compose, and copy. The web-compose routes matter because a large
   share of B2B buyers work in browser mail with no desktop mail client. */
(function () {
  if (window.__jlccInquiryFormLoaded) { return; }
  window.__jlccInquiryFormLoaded = true;

  var EMAIL = 'xxy13992859166@gmail.com';
  var WA = 'https://wa.me/8615339005193';

  function val(f, n) {
    var el = f.querySelector('[name="' + n + '"]');
    return el ? String(el.value || '').trim() : '';
  }

  function compose(f) {
    var name = val(f, 'name'), company = val(f, 'company');
    var email = val(f, 'email'), phone = val(f, 'phone'), msg = val(f, 'message');
    var subject = 'Solar cable inquiry - ' + (company || name || 'website');
    var body = 'Name: ' + name + '\nCompany: ' + company + '\nEmail: ' + email +
      '\nPhone / WhatsApp: ' + phone + '\n\nRequirement:\n' + msg +
      '\n\nPage: ' + location.href;
    // Web compose URLs break past roughly 2000 characters, so the link copy of
    // the body is capped and the untruncated text stays available via Copy.
    var link = body.length > 1500 ? body.slice(0, 1500) + '\n\n[continued - use Copy for the full text]' : body;
    var sub = encodeURIComponent(subject);
    var bod = encodeURIComponent(link);
    return {
      subject: subject,
      body: body,
      wa: WA + '?text=' + encodeURIComponent(subject + '\n\n' + body),
      mail: 'mailto:' + EMAIL + '?subject=' + sub + '&body=' + bod,
      gmail: 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(EMAIL) +
        '&su=' + sub + '&body=' + bod,
      outlook: 'https://outlook.office.com/mail/deeplink/compose?to=' + encodeURIComponent(EMAIL) +
        '&subject=' + sub + '&body=' + bod,
      full: 'To: ' + EMAIL + '\nSubject: ' + subject + '\n\n' + body
    };
  }

  function copyText(text, done) {
    var fallback = function () {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('style', 'position:fixed;left:-9999px;top:0');
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        done();
      } catch (e) { /* leave the message visible for manual copy */ }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
  }

  function panel(f, t) {
    var old = document.getElementById('jlcc-send-panel');
    if (old && old.parentNode) { old.parentNode.removeChild(old); }

    var box = document.createElement('div');
    box.id = 'jlcc-send-panel';
    box.setAttribute('style', 'margin-top:14px;padding:16px 18px;border-radius:8px;background:#eff6ff;border:1px solid #93c5fd;color:#1e3a5f;font-size:14px;line-height:1.6');
    var btnStyle = 'padding:11px 18px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block';
    box.innerHTML =
      '<strong>Your inquiry is written. Pick where to send it - we reply to whichever you use.</strong>' +
      '<div style="margin-top:12px">' +
      '<a href="' + t.wa + '" data-wa-intake="1" target="_blank" rel="noopener" style="' + btnStyle + ';background:#16a34a;color:#fff">WhatsApp (fastest)</a>' +
      '</div>' +
      '<div style="margin-top:8px;font-size:12px;color:#475569">By email - your details are already filled in:</div>' +
      '<div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap">' +
      '<a href="' + t.gmail + '" target="_blank" rel="noopener" style="' + btnStyle + ';background:#2563eb;color:#fff">Open in Gmail</a>' +
      '<a href="' + t.outlook + '" target="_blank" rel="noopener" style="' + btnStyle + ';background:#0f6cbd;color:#fff">Open in Outlook</a>' +
      '<a href="' + t.mail + '" style="' + btnStyle + ';background:#334155;color:#fff">My mail app</a>' +
      '<button type="button" id="jlcc-copy" style="padding:11px 18px;border-radius:6px;border:1px solid #93c5fd;background:#fff;color:#1e3a5f;font-weight:600;cursor:pointer">Copy text</button>' +
      '</div>' +
      '<p style="margin:12px 0 0;font-size:12px;color:#475569">Nothing is sent until you press send in WhatsApp or in your mail window. ' +
      'If no button opens, use Copy text and write to ' + EMAIL + ' or WhatsApp +86 153 3900 5193.</p>';

    var btn = f.querySelector('button[type="submit"]') || f.querySelector('button');
    if (btn && btn.parentNode) { btn.parentNode.insertBefore(box, btn.nextSibling); }
    else { f.appendChild(box); }

    var cp = document.getElementById('jlcc-copy');
    if (cp) {
      cp.addEventListener('click', function () {
        copyText(t.full, function () {
          cp.textContent = 'Copied - now paste it';
        });
      });
    }
    try { box.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
  }

  function onSubmit(e) {
    var f = e.target;
    if (!f || !f.querySelector('[name="message"]')) { return; }
    e.preventDefault();
    var t = compose(f);
    panel(f, t);
  }

  function wire(f) {
    if (!f || f.getAttribute('data-jlcc-wired') === '1') { return; }
    f.setAttribute('data-jlcc-wired', '1');
    f.setAttribute('data-jlcc-form', '1');
    f.addEventListener('submit', onSubmit);
  }

  function existingForm() {
    var f = document.querySelector('form[data-jlcc-form]') ||
      document.querySelector('form[action^="mailto:"]');
    if (f) { return f; }
    var all = document.getElementsByTagName('form');
    for (var i = 0; i < all.length; i++) {
      if (all[i].querySelector('[name="message"]')) { return all[i]; }
    }
    return null;
  }

  function mount() {
    var found = existingForm();
    if (found) { wire(found); return; }
    if (document.getElementById('jlcc-inquiry')) { return; }

    var section = document.createElement('section');
    section.id = 'jlcc-inquiry';
    section.setAttribute('style', 'padding:40px 16px;background:#f1f5f9;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif');
    section.innerHTML = [
      '<div style="max-width:960px;margin:0 auto">',
      '<h2>Request a Quote</h2>',
      '<p style="margin:0 0 18px;color:#475569;font-size:14px">Send your specification and quantity - we reply with price, lead time and packing.</p>',
      '<form data-jlcc-form action="mailto:' + EMAIL + '?subject=Solar%20cable%20inquiry" method="post" enctype="text/plain">',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Your Name *<br><input type="text" name="name" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Company<br><input type="text" name="company" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">Email *<br><input type="email" name="email" required style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '<label style="flex:1 1 220px;font-size:12px;color:#334155">WhatsApp / Phone<br><input type="text" name="phone" style="width:100%;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px"></label>',
      '</div>',
      '<label style="display:block;font-size:12px;color:#334155">Requirement *<br><textarea name="message" required style="width:100%;min-height:110px;padding:10px;margin-top:5px;border:1px solid #cbd5e1;border-radius:6px" placeholder="Cable type and size, quantity in metres, destination port"></textarea></label>',
      '<div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap">',
      '<button type="submit" style="padding:12px 22px;border:0;border-radius:6px;background:#2563eb;color:#fff;font-size:15px;font-weight:600;cursor:pointer">Send Inquiry</button>',
      '<a href="' + WA + '?text=' + encodeURIComponent('Hi, I would like a quote for solar cable.') + '" target="_blank" rel="noopener" style="padding:12px 22px;border-radius:6px;background:#16a34a;color:#fff;font-size:15px;font-weight:600;text-decoration:none">WhatsApp</a>',
      '</div>',
      '<p style="margin:10px 0 0;font-size:12px;color:#64748b">We reply within 2 business hours (Mon-Sat, 08:00-20:00 GMT+8).</p>',
      '</form>',
      '</div>'
    ].join('');

    var footer = document.querySelector('footer');
    if (footer && footer.parentNode) { footer.parentNode.insertBefore(section, footer); }
    else { document.body.appendChild(section); }
    wire(section.querySelector('form'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
