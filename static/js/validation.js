/**
 * SneakerHub — Client-side Form Validation
 */
document.addEventListener('DOMContentLoaded', function () {
    // ── Registration Form ──
    const regForm = document.getElementById('form-register');
    if (regForm) {
        regForm.addEventListener('submit', function (e) {
            const pw = document.getElementById('input-password')?.value || '';
            const cpw = document.getElementById('input-confirm-password')?.value || '';
            const errors = [];
            if (pw.length < 8) errors.push('Password must be at least 8 characters.');
            if (!/[A-Z]/.test(pw)) errors.push('Password needs an uppercase letter.');
            if (!/[0-9]/.test(pw)) errors.push('Password needs a number.');
            if (pw !== cpw) errors.push('Passwords do not match.');
            if (errors.length) { e.preventDefault(); errors.forEach(err => showToast(err, 'danger')); }
        });
        // Password strength indicator
        const pwInput = document.getElementById('input-password');
        const strengthBar = document.getElementById('password-strength');
        if (pwInput && strengthBar) {
            pwInput.addEventListener('input', function () {
                let score = 0;
                if (this.value.length >= 8) score++;
                if (/[A-Z]/.test(this.value)) score++;
                if (/[0-9]/.test(this.value)) score++;
                if (/[^A-Za-z0-9]/.test(this.value)) score++;
                const colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71'];
                strengthBar.style.width = (score * 25) + '%';
                strengthBar.style.background = colors[score - 1] || '#e74c3c';
            });
        }
    }
});
