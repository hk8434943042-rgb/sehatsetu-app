const backendUrl = 'http://127.0.0.1:8000';
let currentLoginMode = 'user';

function switchLoginMode(mode) {
    currentLoginMode = mode;
    const userSection = document.getElementById('userLoginSection');
    const adminSection = document.getElementById('adminLoginSection');
    const userTab = document.getElementById('userLoginTab');
    const adminTab = document.getElementById('adminLoginTab');

    if (mode === 'user') {
        userSection.style.display = 'block';
        adminSection.style.display = 'none';
        userTab.style.borderBottomColor = '#2e7d32';
        userTab.style.color = '#2e7d32';
        adminTab.style.borderBottomColor = 'transparent';
        adminTab.style.color = '#999';
    } else {
        userSection.style.display = 'none';
        adminSection.style.display = 'block';
        userTab.style.borderBottomColor = 'transparent';
        userTab.style.color = '#999';
        adminTab.style.borderBottomColor = '#c62828';
        adminTab.style.color = '#c62828';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Handle regular user login
    const loginForm = document.getElementById('loginForm');
    const loginMessage = document.getElementById('loginMessage');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            if (!email || !password) {
                loginMessage.textContent = 'Please fill in all fields.';
                return;
            }

            try {
                const response = await fetch(`${backendUrl}/api/auth/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    loginMessage.style.color = 'green';
                    loginMessage.textContent = 'Login successful! Redirecting...';

                    // Redirect based on user type
                    setTimeout(() => {
                        if (data.user_type === 'admin') {
                            window.location.href = 'admin-dashboard.html';
                        } else if (data.user_type === 'doctor') {
                            window.location.href = 'doctor-dashboard.html';
                        } else {
                            window.location.href = 'patient-dashboard.html';
                        }
                    }, 1000);
                } else {
                    loginMessage.textContent = data.error || 'Login failed. Please check your credentials.';
                }
            } catch (error) {
                console.error('Login error:', error);
                loginMessage.textContent = 'Network error. Please try again.';
            }
        });
    }

    // Handle admin login
    const adminLoginForm = document.getElementById('adminLoginForm');
    const adminLoginMessage = document.getElementById('adminLoginMessage');

    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('adminEmail').value;
            const password = document.getElementById('adminPassword').value;

            if (!email || !password) {
                adminLoginMessage.textContent = 'Please fill in all fields.';
                return;
            }

            try {
                const response = await fetch(`${backendUrl}/api/auth/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Verify it's an admin account
                    if (data.user_type !== 'admin') {
                        adminLoginMessage.textContent = '❌ Access denied. This account is not an admin account.';
                        return;
                    }

                    adminLoginMessage.style.color = 'green';
                    adminLoginMessage.textContent = '✅ Login successful! Redirecting to admin dashboard...';

                    // Redirect to admin dashboard
                    setTimeout(() => {
                        window.location.href = 'admin-dashboard.html';
                    }, 1000);
                } else {
                    adminLoginMessage.textContent = data.error || 'Login failed. Please check your credentials.';
                }
            } catch (error) {
                console.error('Admin login error:', error);
                adminLoginMessage.textContent = 'Network error. Please try again.';
            }
        });
    }
});