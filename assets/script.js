const menuButton = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const yearElement = document.querySelector('#currentYear');
const root = document.documentElement;
const themeStorageKey = 'sehatsetu-theme';

function applyTheme(themeName) {
    if (themeName === 'mono') {
        root.setAttribute('data-theme', 'mono');
        return;
    }

    root.removeAttribute('data-theme');
}

function createThemeToggle() {
    const existingToggle = document.querySelector('.theme-toggle');
    if (existingToggle) {
        return existingToggle;
    }

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'theme-toggle';
    document.body.appendChild(toggle);
    return toggle;
}

function updateToggleLabel(toggleElement) {
    const monoEnabled = root.getAttribute('data-theme') === 'mono';
    toggleElement.textContent = monoEnabled ? 'Color Theme' : 'B/W Theme';
    toggleElement.setAttribute('aria-label', monoEnabled ? 'Switch to color theme' : 'Switch to black and white theme');
}

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

const savedTheme = localStorage.getItem(themeStorageKey);
applyTheme(savedTheme);

const themeToggleButton = createThemeToggle();
updateToggleLabel(themeToggleButton);

themeToggleButton.addEventListener('click', () => {
    const nextTheme = root.getAttribute('data-theme') === 'mono' ? 'color' : 'mono';
    applyTheme(nextTheme);

    if (nextTheme === 'mono') {
        localStorage.setItem(themeStorageKey, 'mono');
    } else {
        localStorage.removeItem(themeStorageKey);
    }

    updateToggleLabel(themeToggleButton);
});

if (menuButton && navLinks) {
    menuButton.addEventListener('click', () => {
        const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
        menuButton.setAttribute('aria-expanded', String(!isExpanded));
        navLinks.classList.toggle('is-open', !isExpanded);
    });
}