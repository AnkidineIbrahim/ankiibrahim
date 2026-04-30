/* ============================================================
   IBRAHIM ANKIDINE — PORTFOLIO 2026
   main.js — Interactions & Animations Premium (FIXED)
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ════════════════════════════════════════
     1. CUSTOM CURSOR
  ════════════════════════════════════════ */
  const cursor     = document.querySelector('.cursor');
  const cursorRing = document.querySelector('.cursor-ring');

  if (cursor && cursorRing && window.innerWidth > 768) {
    let mx = 0, my = 0, rx = 0, ry = 0;

    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      cursor.style.left = mx + 'px';
      cursor.style.top  = my + 'px';
    });

    const ringLoop = () => {
      rx += (mx - rx) * 0.12;
      ry += (my - ry) * 0.12;
      cursorRing.style.left = rx + 'px';
      cursorRing.style.top  = ry + 'px';
      requestAnimationFrame(ringLoop);
    };
    ringLoop();

    document.querySelectorAll('a, button, .proj-card, .tl-card, .sb').forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.style.transform    = 'translate(-50%,-50%) scale(2.5)';
        cursorRing.style.transform = 'translate(-50%,-50%) scale(1.5)';
        cursorRing.style.opacity  = '0.3';
      });
      el.addEventListener('mouseleave', () => {
        cursor.style.transform    = 'translate(-50%,-50%) scale(1)';
        cursorRing.style.transform = 'translate(-50%,-50%) scale(1)';
        cursorRing.style.opacity  = '0.6';
      });
    });
  }

  /* ════════════════════════════════════════
     2. DARK / LIGHT THEME TOGGLE
     HTML id="themeBtn" (était "themeToggle")
  ════════════════════════════════════════ */
  const themeToggle = document.getElementById('themeBtn'); // ✅ CORRIGÉ
  const savedTheme  = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  themeToggle?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next    = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });

  /* ════════════════════════════════════════
     3. HAMBURGER / MOBILE MENU
     HTML id="navLinks" (était "navCenter")
  ════════════════════════════════════════ */
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks'); // ✅ CORRIGÉ

  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');  // ✅ CORRIGÉ
  });

  navLinks?.querySelectorAll('a').forEach(a => { // ✅ CORRIGÉ
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open'); // ✅ CORRIGÉ
    });
  });

  /* ════════════════════════════════════════
     4. NAV — SCROLL SHADOW + ACTIVE LINK
  ════════════════════════════════════════ */
  const nav      = document.querySelector('nav');
  const sections = document.querySelectorAll('section[id]');
  const navAnchors = document.querySelectorAll('.nav-links a'); // ✅ CORRIGÉ (était .nav-center)

  const navObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navAnchors.forEach(a => {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(s => navObserver.observe(s));

  window.addEventListener('scroll', () => {
    nav?.classList.toggle('scrolled', window.scrollY > 30);
  }, { passive: true });

  /* ════════════════════════════════════════
     5. SCROLL REVEAL
  ════════════════════════════════════════ */
  const revealEls = document.querySelectorAll('.reveal, .stagger');

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => revealObserver.observe(el));

  /* ════════════════════════════════════════
     6. TYPING EFFECT — HERO ROLE
  ════════════════════════════════════════ */
  const roleEl = document.getElementById('heroRole');
  if (roleEl) {
    const phrases = [
      'Développeur Web Full Stack',
      'Spécialiste Laravel & React',
      'Architecte d\'APIs RESTful',
      'Créateur de solutions digitales'
    ];
    let pIdx = 0, cIdx = 0, deleting = false;

    const typeStep = () => {
      const phrase = phrases[pIdx];
      if (!deleting) {
        roleEl.textContent = phrase.slice(0, ++cIdx);
        if (cIdx === phrase.length) {
          deleting = true;
          setTimeout(typeStep, 2200);
          return;
        }
        setTimeout(typeStep, 75);
      } else {
        roleEl.textContent = phrase.slice(0, --cIdx);
        if (cIdx === 0) {
          deleting = false;
          pIdx = (pIdx + 1) % phrases.length;
          setTimeout(typeStep, 300);
          return;
        }
        setTimeout(typeStep, 40);
      }
    };
    setTimeout(typeStep, 1200);
  }

  /* ════════════════════════════════════════
     7. ANIMATED COUNTERS — HERO STATS
     HTML class="stat-n" (était "stat-num")
  ════════════════════════════════════════ */
  const counters = document.querySelectorAll('.stat-n[data-target]'); // ✅ CORRIGÉ

  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.dataset.target);
      const suffix = el.dataset.suffix || '';
      const dur    = 1800;
      const step   = 16;
      const inc    = target / (dur / step);
      let   cur    = 0;

      const tick = () => {
        cur = Math.min(cur + inc, target);
        el.textContent = Math.floor(cur) + suffix;
        if (cur < target) requestAnimationFrame(tick);
      };
      tick();
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => counterObserver.observe(el));

  /* ════════════════════════════════════════
     8. PARALLAX — HERO ORBS
  ════════════════════════════════════════ */
  const orb1 = document.querySelector('.orb1'); // ✅ CORRIGÉ (HTML utilise .orb1/.orb2)
  const orb2 = document.querySelector('.orb2');

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (orb1) orb1.style.transform = `translateY(${y * 0.15}px)`;
    if (orb2) orb2.style.transform = `translateY(${y * -0.1}px)`;
  }, { passive: true });

  /* ════════════════════════════════════════
     9. TILT EFFECT — PROJECT CARDS
     HTML class="proj-card" (était "project-card")
  ════════════════════════════════════════ */
  document.querySelectorAll('.proj-card').forEach(card => { // ✅ CORRIGÉ
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const cx   = rect.left + rect.width  / 2;
      const cy   = rect.top  + rect.height / 2;
      const dx   = (e.clientX - cx) / (rect.width  / 2);
      const dy   = (e.clientY - cy) / (rect.height / 2);
      card.style.transform = `perspective(600px) rotateY(${dx * 5}deg) rotateX(${-dy * 4}deg) translateY(-8px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform  = '';
      card.style.transition = 'transform .6s cubic-bezier(.34,1.56,.64,1), border-color .3s, box-shadow .3s';
    });
    card.addEventListener('mouseenter', () => {
      card.style.transition = 'transform .1s, border-color .3s, box-shadow .3s';
    });
  });

  /* ════════════════════════════════════════
     10. MAGNETIC BUTTONS
  ════════════════════════════════════════ */
  document.querySelectorAll('.btn-primary, .btn-outline, .nav-cv-btn').forEach(btn => { // ✅ CORRIGÉ nav-cta → nav-cv-btn
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const dx   = (e.clientX - (rect.left + rect.width  / 2)) * 0.25;
      const dy   = (e.clientY - (rect.top  + rect.height / 2)) * 0.25;
      btn.style.transform = `translate(${dx}px,${dy}px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform  = '';
      btn.style.transition = 'transform .4s cubic-bezier(.34,1.56,.64,1), background .25s, box-shadow .25s';
    });
    btn.addEventListener('mouseenter', () => {
      btn.style.transition = 'transform .1s, background .25s, box-shadow .25s';
    });
  });

  /* ════════════════════════════════════════
     11. CONTACT FORM
     HTML: id="btnSend", id="formOk" (étaient "btnSubmit", "formSuccess")
  ════════════════════════════════════════ */
  const contactForm = document.getElementById('contactForm');
  const btnForm = document.getElementById('btnSend');
  const formOk = document.getElementById('formOk');

  if (contactForm && btnForm) {
    contactForm.addEventListener('submit', async event => {
      event.preventDefault();

      const name     = document.getElementById('cName')?.value.trim() || '';
      const email    = document.getElementById('cEmail')?.value.trim() || '';
      const msg      = document.getElementById('cMsg')?.value.trim() || '';
      const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      clearErrors();
      let valid = true;
      if (!name)                 { showError('cName',  'Nom requis');     valid = false; }
      if (!emailReg.test(email)) { showError('cEmail', 'Email invalide'); valid = false; }
      if (!msg)                  { showError('cMsg',   'Message requis'); valid = false; }
      if (!valid) return;

      const originalHtml = btnForm.innerHTML;
      btnForm.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
      btnForm.disabled  = true;

      try {
        const response = await fetch(contactForm.action, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            name: name,
            email: email,
            message: msg
          })
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.ok) {
          throw new Error(data.error || 'Impossible d\'envoyer le message.');
        }

        contactForm.reset();
        contactForm.style.display = 'none';
        if (formOk) formOk.style.display = 'block';
      } catch (error) {
        showFormMessage(error.message || 'Une erreur est survenue pendant l\'envoi.');
      } finally {
        btnForm.innerHTML = originalHtml;
        btnForm.disabled = false;
      }
    });
  }

  function showError(id, msg) {
    const input = document.getElementById(id);
    if (!input) return;
    input.style.borderColor = '#e07070';
    const err = document.createElement('span');
    err.className = 'form-err';
    err.style.cssText = 'display:block;color:#e07070;font-size:.72rem;margin-top:.3rem;font-family:JetBrains Mono,monospace;';
    err.textContent = '→ ' + msg;
    input.parentNode.appendChild(err);
  }

  function clearErrors() {
    document.querySelectorAll('.form-err').forEach(e => e.remove());
    ['cName','cEmail','cMsg'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.borderColor = '';
    });
  }

  function showFormMessage(msg) {
    const formWrap = document.getElementById('formWrap');
    if (!formWrap) return;

    let box = formWrap.querySelector('.form-feedback');
    if (!box) {
      box = document.createElement('div');
      box.className = 'form-feedback form-err';
      box.style.cssText = 'margin-top:1rem;color:#e07070;font-size:.82rem;font-family:JetBrains Mono,monospace;';
      formWrap.appendChild(box);
    }
    box.textContent = msg;
  }

  /* ════════════════════════════════════════
     12. PAGE LOADER
  ════════════════════════════════════════ */
  const loader = document.getElementById('pageLoader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        loader.style.opacity      = '0';
        loader.style.pointerEvents = 'none';
        setTimeout(() => loader.remove(), 600);
      }, 400);
    });
  }

  /* ════════════════════════════════════════
     13. FLOATING CV BUTTON
     HTML id="cvFloat" (était "cvFloatBtn")
  ════════════════════════════════════════ */
  const cvFloatBtn  = document.getElementById('cvFloat');   // ✅ CORRIGÉ
  const heroSection = document.getElementById('hero');

  if (cvFloatBtn && heroSection) {
    const floatObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        cvFloatBtn.classList.toggle('visible', !entry.isIntersecting);
      });
    }, { threshold: 0.1 });
    floatObserver.observe(heroSection);
  }

  /* ════════════════════════════════════════
     14. DOWNLOAD BUTTON — animation au clic
  ════════════════════════════════════════ */
  document.querySelectorAll('[download]').forEach(btn => {
    btn.addEventListener('click', function () {
      const orig = this.innerHTML;
      this.innerHTML     = orig.replace(/fa-download|fa-file-arrow-down/, 'fa-check');
      this.style.background   = 'rgba(100,200,120,.15)';
      this.style.borderColor  = '#64c878';
      this.style.color        = '#64c878';
      setTimeout(() => {
        this.innerHTML    = orig;
        this.style.background  = '';
        this.style.borderColor = '';
        this.style.color       = '';
      }, 2500);
    });
  });

});
