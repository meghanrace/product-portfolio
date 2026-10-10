// Contents rail on the long resource pages: marks the section in view.
(function () {
  var links = [].slice.call(document.querySelectorAll('.doc-toc a'));
  if (!links.length) return;
  var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  var ticking = false;
  function spy() {
    ticking = false;
    var line = window.innerHeight * 0.3, current = 0;
    targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top <= line) current = i; });
    links.forEach(function (a, i) { a.classList.toggle('active', i === current); });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(spy); } }, { passive: true });
  window.addEventListener('resize', spy);
  spy();
})();
