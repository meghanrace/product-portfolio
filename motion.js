// motion.js — shared page movement: brush strokes paint in, loose swatches
// drift with the scroll, home-page figures count up. Respects reduced motion.
// Movement. Strokes paint in, swatches drift, figures count up.
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // reveal by position rather than IntersectionObserver, which stays silent
  // in hidden tabs, print and screenshot tools and would leave strokes unpainted
  var pending = [].slice.call(document.querySelectorAll('.paint, .stroke, .rise'));
  function reveal() {
    var line = innerHeight * 0.9;
    pending = pending.filter(function (el) {
      if (still || el.getBoundingClientRect().top < line) { el.classList.add('in'); return false; }
      return true;
    });
  }
  reveal();
  addEventListener('load', reveal);
  if (still) return;

  // drift: each loose swatch moves at its own rate against the scroll
  var drifts = [].slice.call(document.querySelectorAll('.drift'));
  var rates = [0.10, -0.06, 0.16, 0.08, -0.12];
  var base = drifts.map(function (el) { return getComputedStyle(el).transform === 'none' ? '' : getComputedStyle(el).transform; });
  var ticking = false;
  function drift() {
    var y = window.scrollY;
    drifts.forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      var off = (r.top + r.height / 2 - innerHeight / 2) * rates[i % rates.length];
      el.style.transform = base[i] + ' translate3d(' + (off * 0.6).toFixed(1) + 'px,' + off.toFixed(1) + 'px,0)';
    });
    ticking = false;
  }
  addEventListener('scroll', function () { reveal(); if (!ticking) { ticking = true; requestAnimationFrame(drift); } }, { passive: true });
  drift();

  // count up the hero figures once
  document.querySelectorAll('.fact .n').forEach(function (n) {
    var m = n.textContent.match(/^([^0-9]*)([0-9]+)(.*)$/);
    if (!m) return;
    var to = +m[2], t0 = null;
    n.textContent = m[1] + '0' + m[3];
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1100), e = 1 - Math.pow(1 - p, 3);
      n.textContent = m[1] + Math.round(to * e) + m[3];
      if (p < 1) requestAnimationFrame(step);
    }
    setTimeout(function () { requestAnimationFrame(step); }, 250);
  });
})();
