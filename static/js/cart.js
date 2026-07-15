/**
 * SneakerHub — Cart AJAX Operations
 */
function updateCart(cartId, quantity) {
    const form = new FormData();
    form.append('cart_id', cartId);
    form.append('quantity', quantity);
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                      document.querySelector('input[name="csrf_token"]')?.value;
    fetch('/cart/update', { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }, body: form })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                if (quantity < 1) location.reload();
                else {
                    document.getElementById('cart-subtotal') && (document.getElementById('cart-subtotal').textContent = '$' + data.subtotal.toFixed(2));
                    document.getElementById('cart-tax') && (document.getElementById('cart-tax').textContent = '$' + data.tax.toFixed(2));
                    document.getElementById('cart-shipping') && (document.getElementById('cart-shipping').textContent = '$' + data.shipping.toFixed(2));
                    document.getElementById('cart-total') && (document.getElementById('cart-total').textContent = '$' + data.total.toFixed(2));
                    const badge = document.getElementById('cart-badge');
                    if (badge) badge.textContent = data.cart_count;
                }
            }
        }).catch(() => showToast('Error updating cart.', 'danger'));
}

function removeFromCart(cartId) {
    const form = new FormData();
    form.append('cart_id', cartId);
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                      document.querySelector('input[name="csrf_token"]')?.value;
    fetch('/cart/remove', { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }, body: form })
        .then(r => r.json())
        .then(data => { if (data.success) location.reload(); })
        .catch(() => showToast('Error removing item.', 'danger'));
}

function addToCart(productId, size) {
    const form = new FormData();
    form.append('product_id', productId);
    form.append('size', size || '');
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                      document.querySelector('input[name="csrf_token"]')?.value;
    fetch('/cart/add', { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }, body: form })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                showToast(data.message, 'success');
                const badge = document.getElementById('cart-badge');
                if (badge) badge.textContent = data.cart_count;
                else location.reload();
            } else showToast(data.message, 'danger');
        }).catch(() => showToast('Error adding to cart.', 'danger'));
}

function toggleWishlist(productId) {
    const form = new FormData();
    form.append('product_id', productId);
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                      document.querySelector('input[name="csrf_token"]')?.value;
    fetch('/wishlist/add', { method: 'POST', headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }, body: form })
        .then(r => r.json())
        .then(data => { if (data.success) showToast(data.message, 'success'); })
        .catch(() => showToast('Please log in first.', 'warning'));
}
