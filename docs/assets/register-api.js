// Registration form handler for Sehat Setu

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.auth-form');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const [nameInput, phoneInput, emailInput, cityInput, passwordInput] = form.querySelectorAll('input[type="text"], input[type="tel"], input[type="email"], input[type="password"]');
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value;

        if (!name || !email || !password) {
            alert('Please fill in all required fields.');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                alert('Registration successful!');
                window.location.href = 'dashboard.html';
            } else {
                alert(data.error || 'Registration failed.');
            }
        } catch (err) {
            alert('Could not connect to server.');
        }
    });
});
