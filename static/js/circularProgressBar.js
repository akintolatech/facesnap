/**
 * Circular Progress component utilities
 * - initProgress(element) : reads data-value or aria-valuenow and paints the conic-gradient.
 * - setProgress(element, value) : sets value (0-100), updates aria, and animates.
 */

function _clamp(n, a=0, b=100){ return Math.min(b, Math.max(a, n)); }

function setProgress(el, value) {
  value = _clamp(Math.round(value));
  // 360 * (value / 100)
  const deg = (360 * value) / 100;
  // set CSS conic gradient stop to deg
  el.querySelector('.cprog-fill').style.background = `conic-gradient(var(--accent) ${deg}deg, transparent ${deg}deg)`;
  // update text + ARIA
  const text = el.querySelector('.cprog-text');
  if (text) text.textContent = `${value}%`;
  el.setAttribute('aria-valuenow', String(value));
  el.dataset.value = String(value);
}

function initProgress(el) {
  // prefer data-value if provided otherwise aria-valuenow
  let initial = parseFloat(el.dataset.value ?? el.getAttribute('aria-valuenow') ?? 0);
  if (isNaN(initial)) initial = 0;
  setProgress(el, initial);
  // keep CSS var for color from style attribute if set inline
  const accent = el.style.getPropertyValue('--accent');
  if (accent) el.querySelector('.cprog-fill').style.setProperty('--accent', accent);
}

// auto-init any .circular-progress on page
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.circular-progress').forEach(initProgress);
});