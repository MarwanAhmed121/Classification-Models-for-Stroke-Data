/**
 * ClassifyAI — Main JavaScript
 * Handles: dark/light mode · navbar · toast auto-dismiss · page loader · animations
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Page Loader ────────────────────────────────────────────────
  const loader = document.getElementById('pageLoader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => loader.classList.add('done'), 200);
    });
  }

  // ── Dark / Light Mode ──────────────────────────────────────────
  const html      = document.documentElement;
  const themeBtn  = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');

  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateThemeIcon(next);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeIcon) return;
    themeIcon.className = theme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
  }

  // ── Navbar Scroll Shadow ───────────────────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.boxShadow = window.scrollY > 10 ? '0 4px 24px rgba(0,0,0,0.25)' : '';
    }, { passive: true });
  }

  // ── Hamburger Menu ─────────────────────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    document.addEventListener('click', e => {
      if (!navbar.contains(e.target)) navLinks.classList.remove('open');
    });
  }

  // ── Toast Auto-dismiss ─────────────────────────────────────────
  document.querySelectorAll('.toast[data-auto-dismiss]').forEach(toast => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(24px)';
      toast.style.transition = 'opacity 0.4s, transform 0.4s';
      setTimeout(() => toast.remove(), 400);
    }, 4500);
  });

  // ── Feature Card Scroll Reveal ────────────────────────────────
  const featureCards = document.querySelectorAll('.feature-card');
  if (featureCards.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const delay = entry.target.dataset.delay || 0;
          setTimeout(() => {
            entry.target.style.opacity    = '1';
            entry.target.style.transform  = 'translateY(0)';
          }, parseInt(delay));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    featureCards.forEach(card => {
      card.style.opacity   = '0';
      card.style.transform = 'translateY(24px)';
      card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(card);
    });
  }

  // ── Mobile sidebar overlay close ──────────────────────────────
  document.addEventListener('click', e => {
    const sidebar = document.getElementById('sidebar');
    const toggle  = document.getElementById('sidebarToggle');
    if (sidebar && toggle && window.innerWidth < 768) {
      if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('mobile-open');
      }
    }
  });

  // On mobile, sidebarToggle adds mobile-open rather than collapsed
  const sidebarToggle = document.getElementById('sidebarToggle');
  if (sidebarToggle && window.innerWidth < 768) {
    sidebarToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const sidebar = document.getElementById('sidebar');
      if (sidebar) sidebar.classList.toggle('mobile-open');
    }, { capture: true });
  }

  // ── Btn loading state helper ──────────────────────────────────
  window.setLoading = (btnId, loading) => {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.querySelector('.btn-label')?.classList.toggle('hidden', loading);
    btn.querySelector('.btn-loader')?.classList.toggle('hidden', !loading);
  };

});
