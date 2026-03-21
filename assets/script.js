const menuButton = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const yearElement = document.querySelector('#currentYear');

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

if (menuButton && navLinks) {
    menuButton.addEventListener('click', () => {
        const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
        menuButton.setAttribute('aria-expanded', String(!isExpanded));
        navLinks.classList.toggle('is-open', !isExpanded);
    });
}