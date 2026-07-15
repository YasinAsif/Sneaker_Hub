/**
 * SneakerHub — Main JavaScript
 * Toast notifications, delete modal, navbar scroll, animations.
 */

// ── Toast Notification ──
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const icons = { success: 'check-circle-fill', danger: 'exclamation-triangle-fill', warning: 'exclamation-circle-fill', info: 'info-circle-fill' };
    const toast = document.createElement('div');
    toast.className = `toast toast-custom show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `<div class="toast-body d-flex align-items-center gap-2">
        <i class="bi bi-${icons[type] || icons.info} text-${type}"></i>
        <span>${message}</span>
        <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.closest('.toast').remove()"></button>
    </div>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ── Delete Confirmation Modal ──
document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('modal-delete-confirm');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const trigger = event.relatedTarget;
            if (trigger) {
                const action = trigger.getAttribute('data-action');
                const name = trigger.getAttribute('data-name') || 'this item';
                document.getElementById('form-delete-confirm').action = action;
                document.getElementById('modal-delete-body').textContent = `Are you sure you want to delete "${name}"? This action cannot be undone.`;
            }
        });
    }

    // ── Navbar Scroll Effect ──
    const navbar = document.getElementById('navbar-main');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    // ── Fade-in animation on scroll ──
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) { entry.target.classList.add('fade-in-up'); observer.unobserve(entry.target); }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

    // ── Star rating interactive ──
    document.querySelectorAll('.star-rating .star').forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute('data-rating');
            const container = this.closest('.star-rating');
            const input = container.querySelector('input[name="rating"]') || document.getElementById('input-rating');
            if (input) input.value = rating;
            container.querySelectorAll('.star').forEach(s => {
                s.classList.toggle('active', parseInt(s.getAttribute('data-rating')) <= parseInt(rating));
            });
        });
    });

    // ── Size selector ──
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.size-selector').querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const input = document.getElementById('input-size');
            if (input) input.value = this.getAttribute('data-size');
        });
    });

    // ── Auto-dismiss flash alerts ──
    document.querySelectorAll('#flash-messages .alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
});
