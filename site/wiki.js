// kdk knowledge 위키 — 목차·사이드바 필터(제목·개념) + 본문 전문 검색(search-index.json) + 현재 문서 표시
(function () {
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); };
  var here = decodeURIComponent(location.pathname.split('/').pop()) || 'index.html';
  document.querySelectorAll('.nav a').forEach(function (a) {
    if (a.getAttribute('href') === here) {
      a.classList.add('on');
      var d = a.closest('details'); if (d) d.open = true;
      var side = a.closest('.side');
      if (side) setTimeout(function () { side.scrollTop = a.offsetTop - side.clientHeight / 2; }, 0);
    }
  });
  var q = document.querySelector('.search');
  var hits = document.getElementById('search-results');
  var root = document.body.getAttribute('data-search-root') || '.';
  var index = null;
  function filter() {
    var t = q ? q.value.trim().toLowerCase() : '';
    document.querySelectorAll('[data-q]').forEach(function (el) {
      el.classList.toggle('hidden', !!t && el.getAttribute('data-q').toLowerCase().indexOf(t) < 0);
    });
    document.querySelectorAll('.nav details, .group').forEach(function (g) {
      g.classList.toggle('hidden', !g.querySelector('[data-q]:not(.hidden)'));
      if (t && g.tagName === 'DETAILS') g.open = true;
    });
    var n = document.querySelector('[data-count]');
    if (n) n.textContent = document.querySelectorAll('.entry:not(.hidden)').length;
  }
  function fullText() {
    if (!hits || !q) return;
    var t = q.value.trim().toLowerCase();
    if (t.length < 2 || !index) { hits.hidden = true; hits.innerHTML = ''; return; }
    var found = index.filter(function (d) { return (d.title + ' ' + d.body).toLowerCase().indexOf(t) >= 0; }).slice(0, 8);
    hits.innerHTML = found.map(function (d) {
      var i = d.body.toLowerCase().indexOf(t);
      var snip = i < 0 ? '' : d.body.slice(Math.max(0, i - 40), i + 70).replace(/\s+/g, ' ');
      return '<li><a href="' + root + '/' + esc(d.url) + '">' + esc(d.title) + '</a><small>' + esc(snip) + '</small></li>';
    }).join('') || '<li><small>본문에 일치하는 문장이 없습니다.</small></li>';
    hits.hidden = false;
  }
  if (q) {
    q.addEventListener('input', function () { filter(); fullText(); });
    fetch(root + '/search-index.json', {cache: 'no-store'}).then(function (r) { return r.json(); })
      .then(function (d) { index = d; fullText(); }).catch(function () {});
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
    });
  }
  filter();
})();
