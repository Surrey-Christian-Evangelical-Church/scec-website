/**
 * Surrey Christian Evangelical Church (素里中国福音教会 - SCEC)
 * Main Interactive Script - main.js
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Drawer Toggle
  const mobileToggle = document.querySelector('.mobile-toggle');
  const mainNav = document.querySelector('.main-nav');
  const navItemsWithSubmenu = document.querySelectorAll('.nav-item.has-submenu');

  if (mobileToggle && mainNav) {
    mobileToggle.addEventListener('click', () => {
      const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';
      mobileToggle.setAttribute('aria-expanded', !isExpanded);
      mainNav.classList.toggle('open');
      document.body.style.overflow = mainNav.classList.contains('open') ? 'hidden' : '';
    });
  }

  // Mobile submenu accordion
  navItemsWithSubmenu.forEach(item => {
    const link = item.querySelector('.nav-link');
    if (link) {
      link.addEventListener('click', (e) => {
        if (window.innerWidth <= 840) {
          e.preventDefault();
          item.classList.toggle('open');
        }
      });
    }
  });

  // Close mobile nav when clicking outside
  document.addEventListener('click', (e) => {
    if (mainNav && mainNav.classList.contains('open')) {
      if (!mainNav.contains(e.target) && !mobileToggle.contains(e.target)) {
        mainNav.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    }
  });

  // 2. Back to top button
  const backToTopBtn = document.querySelector('.back-to-top');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 3. Contact Form Submission Handling
  const contactForm = document.getElementById('contactForm');
  const toastMsg = document.getElementById('toastMsg');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = '正在发送...';

      // Simulate sending to Google Form / backend
      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        contactForm.reset();

        if (toastMsg) {
          toastMsg.classList.add('show');
          setTimeout(() => {
            toastMsg.classList.remove('show');
          }, 4500);
        }
      }, 800);
    });
  }

  // 4. Live Search Filter for Worship Songs (worship.html)
  const songSearchInput = document.getElementById('songSearch');
  const songsList = document.getElementById('songsList');

  if (songSearchInput && songsList) {
    const songItems = songsList.querySelectorAll('.song-item-wrapper, .song-item');
    songSearchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim().toLowerCase();
      songItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(query)) {
          item.style.display = 'flex';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }
});
