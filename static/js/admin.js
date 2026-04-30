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

  /* —— MESSAGE MODAL —— */
  const messageModal = document.getElementById('messageModal');
  const modalName = document.getElementById('modalMessageName');
  const modalEmail = document.getElementById('modalMessageEmail');
  const modalDate = document.getElementById('modalMessageDate');
  const modalContent = document.getElementById('modalMessageContent');

  const closeMessageModal = () => {
    if (!messageModal) return;
    messageModal.classList.remove('open');
    messageModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  const openMessageModal = trigger => {
    if (!messageModal || !trigger) return;
    if (modalName) modalName.textContent = trigger.dataset.messageName || '-';
    if (modalEmail) modalEmail.textContent = trigger.dataset.messageEmail || '-';
    if (modalDate) modalDate.textContent = trigger.dataset.messageDate || '-';
    if (modalContent) modalContent.textContent = trigger.dataset.messageContent || '';
    messageModal.classList.add('open');
    messageModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  document.querySelectorAll('.js-open-message').forEach(btn => {
    btn.addEventListener('click', () => openMessageModal(btn));
  });

  messageModal?.querySelectorAll('[data-close-message-modal]').forEach(btn => {
    btn.addEventListener('click', closeMessageModal);
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && messageModal?.classList.contains('open')) {
      closeMessageModal();
    }
  });

  /* —— EXPERIENCE BULLETS MODAL —— */
  const bulletsModal = document.getElementById('experienceBulletsModal');
  const bulletsCompany = document.getElementById('experienceBulletsCompany');
  const bulletsRole = document.getElementById('experienceBulletsRole');
  const bulletsPeriod = document.getElementById('experienceBulletsPeriod');
  const bulletsList = document.getElementById('experienceBulletsList');

  const closeBulletsModal = () => {
    if (!bulletsModal) return;
    bulletsModal.classList.remove('open');
    bulletsModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  const renderBullets = bullets => {
    if (!bulletsList) return;
    bulletsList.innerHTML = '';

    if (!Array.isArray(bullets) || bullets.length === 0) {
      const empty = document.createElement('li');
      empty.className = 'modal-bullets-empty';
      empty.textContent = 'Aucun bullet renseigné pour cette expérience.';
      bulletsList.appendChild(empty);
      return;
    }

    bullets.forEach(text => {
      const item = document.createElement('li');
      item.textContent = text;
      bulletsList.appendChild(item);
    });
  };

  const openBulletsModal = trigger => {
    if (!bulletsModal || !trigger) return;

    let bullets = [];
    try {
      bullets = JSON.parse(trigger.dataset.experienceBullets || '[]');
    } catch (error) {
      bullets = [];
    }

    if (bulletsCompany) bulletsCompany.textContent = trigger.dataset.experienceCompany || '-';
    if (bulletsRole) bulletsRole.textContent = trigger.dataset.experienceRole || '-';
    if (bulletsPeriod) bulletsPeriod.textContent = trigger.dataset.experiencePeriod || '-';
    renderBullets(bullets);

    bulletsModal.classList.add('open');
    bulletsModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  document.querySelectorAll('.js-open-bullets').forEach(btn => {
    btn.addEventListener('click', () => openBulletsModal(btn));
  });

  bulletsModal?.querySelectorAll('[data-close-bullets-modal]').forEach(btn => {
    btn.addEventListener('click', closeBulletsModal);
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && bulletsModal?.classList.contains('open')) {
      closeBulletsModal();
    }
  });

});
