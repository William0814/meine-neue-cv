const { Tolgee, InContextTools, FormatSimple, BackendFetch } = window['@tolgee/web'];

// Detectar idioma desde URL o localStorage
const url = new URL(window.location.href);
let currentLang = url.searchParams.get('lang') || localStorage.getItem('preferredLang') || 'en-US';
console.log('[Tolgee] Detected language:', currentLang);

// Guardar idioma en localStorage
localStorage.setItem('preferredLang', currentLang);

// Preseleccionar el idioma en el <select> si existe
document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('demo-category');
  if (selector) selector.value = currentLang;
});

// Inicializar Tolgee
const tolgee = Tolgee()
  .use(InContextTools())
  .use(FormatSimple())
  .use(BackendFetch())
  .init({
    apiKey: window.tolgeeConfig.apiKey,
    apiUrl: window.tolgeeConfig.apiUrl,
    language: currentLang,
    observerType: 'text',
    observerOptions: { inputPrefix: '{{', inputSuffix: '}}' },
  });

console.log('[Tolgee] Config:', window.tolgeeConfig);
console.log('[Tolgee] SDK instance:', tolgee);

tolgee.run().then(() => {
    const t = tolgee.t;

    document.querySelectorAll('[data-i18n]').forEach((el) => {
        const key = el.getAttribute('data-i18n');
        const attr = el.getAttribute('data-i18n-attr');
        console.log('[Tolgee] Translating:', key);

        if (attr) {
        el.setAttribute(attr, t(key));
        } else {
        el.innerText = t(key);
        }
    });
    });

// Cambiar idioma desde el selector
document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('demo-category');
  if (selector) {
    selector.addEventListener('change', function () {
      const lang = this.value;
      localStorage.setItem('preferredLang', lang);
      const url = new URL(window.location.href);
      url.searchParams.set('lang', lang);
      window.location.href = url.toString();
    });
  }
});
