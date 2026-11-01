// Free Cash Prize Competition Ledger - page enhancements
document.addEventListener('DOMContentLoaded', function () {
  // Highlight the current page in nav
  var path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(function (a) {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
});
