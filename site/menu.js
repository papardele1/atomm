/* Мобильное меню ATOMM: кнопка ☰ в шапке и полноэкранное меню (для экранов до 900px). */
(function () {

  /* Без горизонтальной прокрутки на телефонах (iOS Safari учитывает даже спрятанные панели). */
  (function () {
    var g = document.createElement('style');
    g.textContent = 'html,body{max-width:100%;overflow-x:hidden}@supports(overflow:clip){html,body{overflow-x:clip}}';
    document.head.appendChild(g);
  })();
  var LINKS = [['Главная', 'index.html'], ['Каталог', 'catalog.html'], ['Доставка', 'delivery.html'],
               ['Гарантия', 'warranty.html'], ['Контакты', 'contacts.html']];
  var PHONE = '+79777773727', PHONE_TXT = '+7 977 777-37-27';
  var css = '' +
    '.mburger{display:none;width:44px;height:44px;border-radius:50%;border:1px solid rgba(28,30,33,.16);background:rgba(245,246,247,.6);' +
    'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);align-items:center;justify-content:center;flex-direction:column;gap:5px;cursor:pointer;flex:none;padding:0}' +
    '.mburger span{display:block;width:18px;height:1.5px;background:#1c1e21;border-radius:2px}' +
    '@media(max-width:900px){header nav,header .hnav{display:none!important}.mburger{display:flex}' +
    'header .cart,header .cartbtn{margin-left:auto}header .mburger{margin-left:auto}header .cart~.mburger,header .cartbtn~.mburger{margin-left:10px}}' +
    '.mmenu{position:fixed;inset:0;z-index:100;background:radial-gradient(120% 80% at 50% 0%,#f0f1f3 0%,#dcdee1 60%,#cdd0d4 100%);' +
    'display:flex;flex-direction:column;padding:18px 20px calc(24px + env(safe-area-inset-bottom));transform:translateY(-102%);' +
    'transition:transform .45s cubic-bezier(.2,.8,.2,1);visibility:hidden;font-family:Inter,system-ui,sans-serif;color:#1c1e21}' +
    '.mmenu.show{transform:none;visibility:visible}' +
    '.mmenu .mtop{display:flex;justify-content:space-between;align-items:center}' +
    '.mmenu .mlogo{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:15px;letter-spacing:.34em;color:#1c1e21;text-decoration:none}' +
    '.mmenu .mlogo i{font-style:normal;color:#6b6f75;letter-spacing:.1em;margin-left:6px;font-weight:300}' +
    '.mmenu .mclose{width:44px;height:44px;border-radius:50%;border:1px solid rgba(28,30,33,.16);background:rgba(245,246,247,.6);font-size:24px;line-height:1;cursor:pointer;color:#1c1e21}' +
    '.mmenu nav.mlinks{display:flex!important;flex-direction:column;gap:4px;margin-top:6vh}' +
    '.mmenu nav.mlinks a{font-weight:200;font-size:clamp(34px,10vw,48px);letter-spacing:-.03em;line-height:1.15;color:#1c1e21;text-decoration:none;' +
    'padding:6px 0;border-bottom:1px solid rgba(28,30,33,.1);display:flex;justify-content:space-between;align-items:center}' +
    '.mmenu nav.mlinks a:after{content:"→";font-size:22px;color:#9a9ea4}' +
    '.mmenu nav.mlinks a.on{color:#7b8087}' +
    '.mmenu .mcontacts{margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}' +
    '.mmenu .mcontacts a{display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 6px;border-radius:16px;text-decoration:none;color:#1c1e21;' +
    'background:rgba(245,246,247,.7);border:1px solid rgba(255,255,255,.6);font-size:13px}' +
    '.mmenu .mcontacts i{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#fff}' +
    '.mmenu .mcontacts svg{width:20px;height:20px}' +
    '.mmenu .mphone{font-family:"JetBrains Mono",monospace;font-size:15px;color:#1c1e21;text-decoration:none;margin:18px 0 10px;display:block;text-align:center}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var header = document.querySelector('header');
  if (!header) return;
  var btn = document.createElement('button');
  btn.className = 'mburger'; btn.type = 'button'; btn.setAttribute('aria-label', 'Меню');
  btn.innerHTML = '<span></span><span></span><span></span>';
  header.appendChild(btn);

  var here = (location.pathname.split('/').pop() || 'index.html');
  var ICONS = {
    call: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    tg: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.3 18.8 19c-.2 1-.9 1.3-1.7.8l-4.7-3.5-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.8 8.8-7.9c.4-.3-.1-.5-.6-.2L6.7 13l-4.6-1.4c-1-.3-1-1 .2-1.5l18-6.9c.8-.3 1.6.2 1.6 1.1z"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
  };
  var menu = document.createElement('div');
  menu.className = 'mmenu'; menu.setAttribute('aria-hidden', 'true');
  menu.innerHTML =
    '<div class="mtop"><a class="mlogo" href="index.html">ATOMM<i>/store</i></a><button class="mclose" type="button" aria-label="Закрыть">×</button></div>' +
    '<nav class="mlinks">' + LINKS.map(function (l) {
      return '<a href="' + l[1] + '"' + (l[1] === here ? ' class="on"' : '') + '>' + l[0] + '</a>';
    }).join('') + '</nav>' +
    '<div style="margin-top:14px;font-size:13px"><a href="offer.html" style="color:#55595f;margin-right:18px">Оферта</a><a href="privacy.html" style="color:#55595f">Политика конфиденциальности</a></div>' +
    '<a class="mphone" href="tel:' + PHONE + '">' + PHONE_TXT + '</a>' +
    '<div class="mcontacts">' +
    '<a href="tel:' + PHONE + '"><i style="background:#1c1e21">' + ICONS.call + '</i>Позвонить</a>' +
    '<a href="https://t.me/mskdiler" target="_blank" rel="noopener"><i style="background:#2aabee">' + ICONS.tg + '</i>Telegram</a>' +
    '<a href="https://wa.me/79777773727" target="_blank" rel="noopener"><i style="background:#25d366">' + ICONS.wa + '</i>WhatsApp</a>' +
    '</div>';
  document.body.appendChild(menu);

  function open() { menu.classList.add('show'); menu.setAttribute('aria-hidden', 'false'); document.documentElement.style.overflow = 'hidden'; }
  function close() { menu.classList.remove('show'); menu.setAttribute('aria-hidden', 'true'); document.documentElement.style.overflow = ''; }
  btn.addEventListener('click', open);
  menu.querySelector('.mclose').addEventListener('click', close);
  menu.querySelectorAll('nav.mlinks a').forEach(function (a) { a.addEventListener('click', close); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  /* Подвал с реквизитами продавца — на всех страницах, кроме главной. */
  if (here !== 'index.html' && here !== '') {
    var fs = document.createElement('style');
    fs.textContent = '.sitefoot{border-top:1px solid rgba(28,30,33,.13);margin-top:40px;padding:22px 32px calc(26px + env(safe-area-inset-bottom));' +
      'font:12px/1.6 Inter,system-ui,sans-serif;color:#6b6f75;display:flex;flex-wrap:wrap;gap:6px 22px;justify-content:space-between}' +
      '.sitefoot>div{min-width:0;max-width:100%}.sitefoot a{color:#33363a;text-decoration:none;margin-right:16px;display:inline-block}.sitefoot a:hover{text-decoration:underline}' +
      '@media(max-width:600px){.sitefoot{padding:20px 18px calc(24px + env(safe-area-inset-bottom))}}';
    document.head.appendChild(fs);
    var f = document.createElement('footer');
    f.className = 'sitefoot';
    f.innerHTML = '<div>ИП Головин Руслан Андреевич · ИНН 502716211095 · ОГРНИП 322508100573880</div>' +
      '<div><a href="offer.html">Публичная оферта</a><a href="privacy.html">Политика конфиденциальности</a><a href="tel:' + PHONE + '">' + PHONE_TXT + '</a></div>';
    document.body.appendChild(f);
  }
})();
