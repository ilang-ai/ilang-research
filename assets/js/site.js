// research.ilang.ai: what every page does. The paper/ink switch, the menu on small screens, the hairline under the
// header once the page has moved, the reading line; on a long page the rail that shows where you are; a copy button
// on code blocks. Nothing here is needed to read a page.
(function(){
  'use strict';
  var root = document.documentElement,
      $ = function(s, c){ return (c || document).querySelector(s); },
      $$ = function(s, c){ return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  clearTimeout(window.__ilangSafe);

  // ---- paper or ink
  var themeBtn = $('#theme');
  function current(){ return root.getAttribute('data-theme') || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'ink' : 'paper'); }
  function sync(){
    var ink = current() === 'ink';
    if (themeBtn) themeBtn.setAttribute('aria-checked', ink ? 'true' : 'false');
    if (root.hasAttribute('data-theme')) $$('meta[name="theme-color"]').forEach(function(m){ m.setAttribute('content', ink ? '#12100c' : '#f5f1e8'); });
  }
  sync();
  if (themeBtn) themeBtn.addEventListener('click', function(ev){
    var next = current() === 'ink' ? 'paper' : 'ink';
    var apply = function(){ root.setAttribute('data-theme', next); try { localStorage.setItem('ilang-theme', next); } catch (e) {} sync(); };
    if (!document.startViewTransition || reduce) { apply(); return; }
    var r = themeBtn.getBoundingClientRect(), x = ev.clientX || r.left + r.width / 2, y = ev.clientY || r.top + r.height / 2;
    var far = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var vt = document.startViewTransition(apply);
    vt.ready.then(function(){
      root.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + far + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 750, easing: 'cubic-bezier(.3,.6,.2,1)', pseudoElement: '::view-transition-new(root)' });
    }).catch(function(){});
  });

  // ---- the menu on small screens
  var nav = $('#nav'), toggle = $('#navToggle'), links = $('#navLinks');
  function menu(open){
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    $$('body > *').forEach(function(el){ if (el === nav || el.tagName === 'SCRIPT') return; if (open) el.setAttribute('inert', ''); else el.removeAttribute('inert'); });
  }
  if (toggle && links) {
    toggle.addEventListener('click', function(){ menu(!links.classList.contains('open')); });
    links.addEventListener('click', function(e){ if (e.target.closest('a')) menu(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && links.classList.contains('open')) { menu(false); toggle.focus(); } });
    window.addEventListener('resize', function(){ if (innerWidth > 860 && links.classList.contains('open')) menu(false); });
  }

  // ---- the rail on a long page: one stop per section title
  var content = $('.post-content'), heads = [];
  if (content) {
    heads = $$('.post-content > h2');
    if (!heads.length) heads = $$('.post-content > h5');
    heads = heads.filter(function(h){ return h.id; });
  }
  var rail = null, mark, out, railLinks = [], tops = [], footer = $('.footer');
  if (heads.length >= 3) {
    rail = document.createElement('aside');
    rail.className = 'rail'; rail.setAttribute('aria-hidden', 'true');
    mark = document.createElement('u'); out = document.createElement('output');
    out.textContent = '0.00';
    rail.appendChild(mark); rail.appendChild(out);
    railLinks = heads.map(function(h, i){
      var a = document.createElement('a');
      a.href = '#' + h.id; a.tabIndex = -1;
      a.textContent = (i + 1 < 10 ? '0' : '') + (i + 1);
      a.setAttribute('data-t', h.textContent.replace(/\s+/g, ' ').trim());
      rail.appendChild(a);
      return a;
    });
    document.body.insertBefore(rail, document.body.firstChild);
    root.classList.add('has-rail');
  }
  function place(){
    if (!rail) return;
    var max = document.documentElement.scrollHeight - innerHeight, H = rail.clientHeight - 22, last = -99;
    // a title that is stuck under the header reports where it is stuck, so a section's top is read from what follows it
    tops = heads.map(function(h){ return (h.nextElementSibling || h).getBoundingClientRect().top + window.scrollY; });
    railLinks.forEach(function(a, i){
      var y = Math.min(1, tops[i] / Math.max(1, max)) * H;
      a.style.top = y + 'px';
      a.classList.toggle('dim', y - last < 13);
      if (y - last >= 13) last = y;
    });
  }

  // ---- the hairline under the header, the reading line, the rail's pointer
  var prog = $('#progress'), ticking = false;
  function onScroll(){
    ticking = false;
    var y = window.scrollY || window.pageYOffset, max = document.documentElement.scrollHeight - innerHeight, p = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    if (nav) nav.classList.toggle('scrolled', y > 8);
    if (prog) prog.style.transform = 'scaleX(' + p + ')';
    if (rail) {
      var at = -1;
      mark.style.transform = 'translateY(' + p * (rail.clientHeight - 22) + 'px)';
      out.textContent = p.toFixed(2);
      for (var i = 0; i < tops.length; i++) if (tops[i] <= y + innerHeight * .4) at = i;
      railLinks.forEach(function(a, i){ a.classList.toggle('cur', i === at); });
      if (footer) rail.classList.toggle('away', footer.getBoundingClientRect().top < innerHeight - 40);
    }
  }
  function both(){ place(); onScroll(); }
  window.addEventListener('scroll', function(){ if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', both);
  window.addEventListener('load', both);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(both);
  both();

  // ---- on a small screen a table is read row by row; each cell carries the name of its column
  $$('.post-content table').forEach(function(t){
    var heads = $$('thead th', t).map(function(th){ return th.textContent.replace(/\s+/g, ' ').trim(); });
    if (!heads.length) return;
    $$('tbody tr', t).forEach(function(tr){ $$('td', tr).forEach(function(td, i){ if (heads[i]) td.setAttribute('data-label', heads[i]); }); });
    t.classList.add('stack');
  });

  // ---- a copy button on every code block
  $$('.post-content pre > code').forEach(function(code){
    var box = code.parentNode.parentNode.classList.contains('highlight') ? code.parentNode.parentNode : code.parentNode;
    if (box.tagName === 'PRE') { box.style.position = 'relative'; }
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'copy-code'; b.textContent = 'copy';
    b.addEventListener('click', function(){
      var done = function(){ b.textContent = 'copied!'; b.classList.add('done'); setTimeout(function(){ b.textContent = 'copy'; b.classList.remove('done'); }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(code.textContent).then(done, function(){}); return; }
      var r = document.createRange(); r.selectNodeContents(code);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      try { document.execCommand('copy'); done(); } catch (e) {}
      s.removeAllRanges();
    });
    box.appendChild(b);
  });
})();
