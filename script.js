document.querySelectorAll('[data-year]').forEach((element) => {
  element.textContent = new Date().getFullYear();
});

const root = document.documentElement;
const header = document.querySelector('.site-header');
const themeMeta = document.querySelector('meta[name="theme-color"]');

function savedTheme() {
  try {
    return localStorage.getItem('portfolio-theme');
  } catch {
    return null;
  }
}

if (header) {
  const nav = header.querySelector('.nav');
  const themeButton = document.createElement('button');
  themeButton.type = 'button';
  themeButton.className = 'theme-toggle';
  nav.append(themeButton);

  function applyTheme(theme) {
    const dark = theme === 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    const icon = dark
      ? '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4m0-14.2-1.4 1.4M6.3 17.7l-1.4 1.4"/>'
      : '<path d="M20 15.3A8.4 8.4 0 0 1 8.7 4 8.5 8.5 0 1 0 20 15.3Z"/>';
    themeButton.innerHTML = `<svg aria-hidden="true" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${icon}</svg>`;
    themeButton.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    themeButton.title = themeButton.getAttribute('aria-label');
    themeMeta?.setAttribute('content', dark ? '#191b1b' : '#f6f3ea');
  }

  applyTheme(savedTheme() || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  themeButton.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem('portfolio-theme', next);
    } catch {
      // Theme selection still works when browser storage is disabled.
    }
    applyTheme(next);
  });

  const measureHeader = () => root.style.setProperty('--header-height', `${header.offsetHeight}px`);
  measureHeader();
  if ('ResizeObserver' in window) new ResizeObserver(measureHeader).observe(header);

  if (document.querySelector('.home-intro')) {
    const links = nav.querySelectorAll('a[href^="/#"]');
    const syncSection = () => links.forEach((link) => {
      if (link.hash === location.hash) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    syncSection();
    window.addEventListener('hashchange', syncSection);
  }
}

const scrollRegions = [...document.querySelectorAll('.table-scroll, pre.code')];
if (scrollRegions.length) {
  const setScrollFocus = (region) => {
    const scrollable = region.scrollWidth > region.clientWidth + 1 || region.scrollHeight > region.clientHeight + 1;
    if (scrollable) region.tabIndex = 0;
    else region.removeAttribute('tabindex');
  };
  const observer = 'ResizeObserver' in window
    ? new ResizeObserver((entries) => entries.forEach(({ target }) => setScrollFocus(target)))
    : null;
  scrollRegions.forEach((region) => {
    setScrollFocus(region);
    observer?.observe(region);
    if (region.matches('pre')) {
      new MutationObserver(() => setScrollFocus(region)).observe(region, {
        childList: true, characterData: true, subtree: true,
      });
    }
  });
}

document.querySelectorAll('.copy-template').forEach((button) => {
  const status = document.createElement('p');
  status.className = 'copy-status';
  status.setAttribute('role', 'status');
  button.closest('.artifact-actions').after(status);
  button.hidden = false;
  let reset;

  button.addEventListener('click', async () => {
    window.clearTimeout(reset);
    button.disabled = true;
    status.textContent = 'Copying template…';

    try {
      const response = await fetch(button.dataset.copyPath);
      if (!response.ok) throw new Error('Template unavailable');
      await navigator.clipboard.writeText(await response.text());
      status.textContent = 'Template copied to the clipboard.';
    } catch {
      status.textContent = 'Copy was unavailable. Open the Markdown download to copy it.';
    } finally {
      button.disabled = false;
      reset = window.setTimeout(() => { status.textContent = ''; }, 5000);
    }
  });
});
