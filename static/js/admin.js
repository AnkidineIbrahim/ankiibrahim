/* ============================================================
   ADMIN PANEL — admin.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── SIDEBAR TOGGLE (mobile) ── */
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar       = document.getElementById('sidebar');

  sidebarToggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
  });

  // Fermer en cliquant à l'extérieur
  document.addEventListener('click', e => {
    if (sidebar?.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        e.target !== sidebarToggle) {
      sidebar.classList.remove('open');
    }
  });

  /* ── AUTO-DISMISS FLASH ── */
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-8px)';
      el.style.transition = 'opacity .4s, transform .4s';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  /* ── CONFIRM DELETE ── */
  document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm(form.dataset.confirm)) e.preventDefault();
    });
  });

  /* ── ACTIVE NAV HIGHLIGHT ── */
  const path = window.location.pathname;
  document.querySelectorAll('.sb-link').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  /* ── ANIMATE KPI NUMBERS ── */
  document.querySelectorAll('.kpi-num').forEach(el => {
    const target = parseInt(el.textContent) || 0;
    if (target === 0) return;
    let cur = 0;
    const step = Math.ceil(target / 30);
    const tick = () => {
      cur = Math.min(cur + step, target);
      el.textContent = cur;
      if (cur < target) requestAnimationFrame(tick);
    };
    tick();
  });

  /* ── BAR CHART ANIMATION ── */
  const barChart = document.getElementById('barChart');
  if (barChart) {
    setTimeout(() => {
      document.querySelectorAll('.bar-fill').forEach((bar, i) => {
        bar.style.transition = `height .6s ease ${i * 0.04}s`;
      });
    }, 100);
  }

  /* ── PAGE BAR ANIMATION ── */
  setTimeout(() => {
    document.querySelectorAll('.page-bar').forEach(bar => {
      const w = bar.style.width;
      bar.style.width = '0';
      setTimeout(() => { bar.style.width = w; }, 100);
    });
  }, 200);

});
