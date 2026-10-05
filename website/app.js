// Fresh visits start at the opening; explicit section links retain their anchors.
window.addEventListener('pageshow', () => {
  if (!window.location.hash) {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
  }
});

const grid = document.querySelector('.glyph-grid');
function bindStyle(buttonSelector, target) {
  const buttons = [...document.querySelectorAll(buttonSelector)];
  for (const button of buttons) button.addEventListener('click', () => {
    const style = button.dataset.glyphStyle || button.dataset.previewStyle;
    target.style.fontStyle = style;
    if (target === grid) requestAnimationFrame(centerGlyphs);
    for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
  });
}
bindStyle('[data-glyph-style]', grid);
const preview = document.querySelector('#type-preview');
bindStyle('[data-preview-style]', preview);
const slider = document.querySelector('#type-size');
const output = document.querySelector('output[for="type-size"]');
const initialSize = window.matchMedia('(max-width: 760px)').matches ? 60 : Math.min(100, Math.round(window.innerWidth * .17));
slider.value = String(initialSize);
function updateSize() {
  preview.style.fontSize = `${slider.value}px`;
  output.value = `${slider.value} px`;
}
updateSize();
slider.addEventListener('input', updateSize);

const comparison = document.querySelector('.process-comparison');
const processButtons = [...document.querySelectorAll('[data-process-style]')];
for (const button of processButtons) button.addEventListener('click', () => {
  comparison.dataset.style = button.dataset.processStyle;
  requestAnimationFrame(centerProcessWords);
  for (const item of processButtons) item.setAttribute('aria-pressed', String(item === button));
});
const menu = document.querySelector('.nav-menu');
for (const link of menu.querySelectorAll('a')) link.addEventListener('click', () => { menu.open = false; });
document.addEventListener('keydown', event => { if (event.key === 'Escape') menu.open = false; });
document.addEventListener('click', event => { if (!menu.contains(event.target)) menu.open = false; });

const copyCss = document.querySelector('#copy-font-css');
const fontCss = document.querySelector('#font-css');
const copyStatus = document.querySelector('#copy-css-status');
let copyReset;
copyCss.addEventListener('click', async () => {
  clearTimeout(copyReset);
  try {
    await navigator.clipboard.writeText(fontCss.textContent);
    copyCss.textContent = 'Copied';
    copyStatus.textContent = 'Font CSS copied to clipboard.';
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(fontCss);
    selection.removeAllRanges();
    selection.addRange(range);
    fontCss.parentElement.focus();
    copyCss.textContent = 'Select CSS';
    copyStatus.textContent = 'CSS selected. Press Command C or Control C to copy.';
  }
  copyReset = setTimeout(() => {
    copyCss.textContent = 'Copy CSS';
    copyStatus.textContent = '';
  }, 3000);
});

// Center each glyph horizontally while preserving the shared baseline of each row.
const glyphMeasure = document.createElement('canvas').getContext('2d');
function centerGlyphs() {
  if (!grid || !glyphMeasure) return;
  for (const span of grid.querySelectorAll('.glyph-cell > span')) {
    const style = getComputedStyle(span);
    glyphMeasure.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const m = glyphMeasure.measureText(span.textContent);
    if (!Number.isFinite(m.actualBoundingBoxLeft) || !Number.isFinite(m.actualBoundingBoxRight)) continue;
    const x = (m.width + m.actualBoundingBoxLeft - m.actualBoundingBoxRight) / 2;
    span.style.transform = `translate(${x}px, 0px)`;
  }
}
// Process specimens use visible-ink centers; glyph-grid rows retain their baseline.
function centerProcessWords() {
  if (!comparison || !glyphMeasure) return;
  for (const span of comparison.querySelectorAll('.context-word > span')) {
    const style = getComputedStyle(span);
    glyphMeasure.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    if ('letterSpacing' in glyphMeasure) glyphMeasure.letterSpacing = style.letterSpacing === 'normal' ? '0px' : style.letterSpacing;
    const m = glyphMeasure.measureText(span.textContent);
    const metrics = [m.actualBoundingBoxLeft, m.actualBoundingBoxRight, m.actualBoundingBoxAscent, m.actualBoundingBoxDescent, m.fontBoundingBoxAscent, m.fontBoundingBoxDescent];
    if (!metrics.every(Number.isFinite)) continue;
    const x = (m.width + m.actualBoundingBoxLeft - m.actualBoundingBoxRight) / 2;
    const y = (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent - m.fontBoundingBoxAscent + m.fontBoundingBoxDescent) / 2;
    span.style.setProperty('--context-x', `${x}px`);
    span.style.setProperty('--context-y', `${y}px`);
  }
  if ('letterSpacing' in glyphMeasure) glyphMeasure.letterSpacing = '0px';
}
document.fonts.ready.then(() => { centerGlyphs(); centerProcessWords(); });
document.fonts.addEventListener('loadingdone', () => { centerGlyphs(); centerProcessWords(); });
let glyphFrame;
window.addEventListener('resize', () => {
  cancelAnimationFrame(glyphFrame);
  glyphFrame = requestAnimationFrame(() => { centerGlyphs(); centerProcessWords(); });
});

// PhysioPrime's word entrance, scoped to the opening specimen only.
const heroMotionPreference = matchMedia('(prefers-reduced-motion: reduce)');
const heroHeading = document.querySelector('#hero-title');
if (heroHeading && !heroMotionPreference.matches && 'IntersectionObserver' in window) {
  const walker = document.createTreeWalker(heroHeading, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  let index = 0;
  for (const node of nodes) {
    const fragment = document.createDocumentFragment();
    for (const part of node.textContent.split(/(\s+)/)) {
      if (!part) continue;
      if (/^\s+$/.test(part)) { fragment.append(document.createTextNode(part)); continue; }
      const word = document.createElement('span');
      word.className = 'hero-motion-word';
      word.setAttribute('aria-hidden', 'true');
      const inner = document.createElement('span');
      inner.textContent = part;
      inner.style.setProperty('--word-delay', `${Math.min(index++ * 65, 520)}ms`);
      word.append(inner);
      fragment.append(word);
    }
    node.replaceWith(fragment);
  }
  heroHeading.setAttribute('aria-label', 'Кирилица с характер.');
  const headingObserver = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      // If the loading fallback has already revealed the heading, do not hide and replay it.
      if (document.documentElement.classList.contains('hero-motion-pending')) {
        entry.target.classList.add('hero-motion-shown');
        document.documentElement.classList.remove('hero-motion-pending');
      }
      headingObserver.unobserve(entry.target);
    }
  }, { threshold: .2 });
  Promise.all([
    document.fonts.load('400 64px "Lirena"', 'Кирилица'),
    document.fonts.load('italic 400 64px "Lirena"', 'с характер.')
  ]).then(() => headingObserver.observe(heroHeading), () => {
    document.documentElement.classList.remove('hero-motion-pending');
  });
}

// Hover opens the native details navigation, while click and keyboard still work.
const navHover = matchMedia('(hover: hover) and (pointer: fine)');
let menuCloseTimer;
function cancelMenuClose() { clearTimeout(menuCloseTimer); }
menu.addEventListener('pointerenter', () => {
  if (!navHover.matches) return;
  cancelMenuClose();
  menu.open = true;
});
menu.addEventListener('pointerleave', () => {
  if (!navHover.matches || menu.contains(document.activeElement)) return;
  menuCloseTimer = setTimeout(() => { menu.open = false; }, 120);
});
menu.addEventListener('focusin', cancelMenuClose);
menu.addEventListener('focusout', event => {
  if (!menu.contains(event.relatedTarget)) menu.open = false;
});
menu.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    cancelMenuClose();
    menu.open = false;
    menu.querySelector('summary').focus();
  }
});
