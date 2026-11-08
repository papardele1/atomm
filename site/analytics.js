/* Яндекс Метрика для ATOMM: счётчик, цели и электронная коммерция.
   Номер счётчика вписывается в METRIKA_ID; пока он 0, скрипт ничего не отправляет. */
(function () {
  var METRIKA_ID = 0;

  window.dataLayer = window.dataLayer || [];

  /* Цель Метрики: atommGoal('order', {order_price: 123}) */
  window.atommGoal = function (goal, params) {
    try { if (METRIKA_ID && window.ym) window.ym(METRIKA_ID, 'reachGoal', goal, params || {}); } catch (e) {}
  };

  /* Электронная коммерция: atommEcom('add', [{id, name, price, brand, category, quantity}]) */
  window.atommEcom = function (action, products, actionField) {
    try {
      var ec = { currencyCode: 'RUB' };
      ec[action] = { products: products };
      if (actionField) ec[action].actionField = actionField;
      window.dataLayer.push({ ecommerce: ec });
    } catch (e) {}
  };

  if (METRIKA_ID) {
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) return; }
      k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    window.ym(METRIKA_ID, 'init', {
      clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true, ecommerce: 'dataLayer'
    });
  }

  /* Клики по телефону и мессенджерам — на всех страницах. */
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (/^tel:/i.test(h)) window.atommGoal('call');
    else if (/t\.me\//i.test(h)) window.atommGoal('telegram');
    else if (/wa\.me|whatsapp/i.test(h)) window.atommGoal('whatsapp');
  }, true);
})();
