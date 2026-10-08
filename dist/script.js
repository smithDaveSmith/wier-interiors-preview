'use strict';
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
function closeMenu(restoreFocus = false) {
  nav.removeAttribute('data-open');
  toggle.setAttribute('aria-expanded', 'false');
  if (restoreFocus) toggle.focus();
}
toggle.addEventListener('click', () => {
  const isOpen = toggle.getAttribute('aria-expanded') === 'true';
  if (isOpen) closeMenu();
  else { nav.setAttribute('data-open', ''); toggle.setAttribute('aria-expanded', 'true'); }
});
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const submenu = document.querySelector('.service-menu[open]');
    if (submenu) { submenu.removeAttribute('open'); submenu.querySelector('summary').focus(); }
    else if (toggle.getAttribute('aria-expanded') === 'true') closeMenu(true);
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) {
    if (toggle.getAttribute('aria-expanded') === 'true') closeMenu();
    document.querySelector('.service-menu')?.removeAttribute('open');
  }
});
window.matchMedia('(min-width: 1101px)').addEventListener('change', () => closeMenu());
// Email draft only: no data storage, backend submission or automatic sending.
const form = document.querySelector('#enquiry-form');
if (form) {
  const requested = new URLSearchParams(window.location.search).get('service');
  const select = document.getElementById('service');
  if (requested && [...select.options].some(o => o.value === requested)) select.value = requested;
  form.addEventListener('submit', event => {
    event.preventDefault();
    for (const id of ['name', 'area', 'message']) {
      const input = document.getElementById(id); input.value = input.value.trim();
    }
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const subject = `Website enquiry — ${data.get('service')}`;
    const body = `Hello Weir Interiors,\n\nI would like to discuss a project.\n\nName: ${data.get('name')}\nEmail: ${data.get('email')}\nArea: ${data.get('area')}\nInterested in: ${data.get('service')}\n\n${data.get('message')}\n\nKind regards,\n${data.get('name')}`;
    window.location.href = `mailto:enquiries@weirinteriors.ie?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    document.getElementById('form-status').textContent = 'Your email app should open with a draft. Send it there when you are ready. If it does not open, use the email address above. No message has been sent by this page.';
  });
}
// Native-dialog lightbox, with ordinary image links as the no-JavaScript fallback.
const dialog = document.querySelector('.lightbox');
if (dialog && typeof dialog.showModal === 'function') {
  const photos = [...document.querySelectorAll('.photo-link')];
  let current = 0;
  const img = document.getElementById('lightbox-image');
  function show(index) {
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    img.src = photo.dataset.full; img.alt = photo.dataset.caption;
    document.getElementById('lightbox-caption').textContent = photo.dataset.caption;
    document.getElementById('lightbox-count').textContent = `${current + 1} / ${photos.length}`;
  }
  photos.forEach((photo, index) => photo.addEventListener('click', event => {
    event.preventDefault(); show(index); dialog.showModal();
  }));
  dialog.querySelector('[data-gallery-prev]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-gallery-next]').addEventListener('click', () => show(current + 1));
  dialog.querySelector('[data-gallery-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
  });
  dialog.addEventListener('close', () => photos[current]?.focus());
}
