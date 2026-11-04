// Flagster Shared Cart & Checkout Engine
(function() {
  'use strict';

  const STORAGE_KEY = 'flagster_cart_v1';
  const COUPON_KEY = 'flagster_coupon_v1';

  let cart = [];
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      cart = JSON.parse(saved);
    }
  } catch (e) {
    cart = [];
  }

  // Default item if cart is empty on first visit
  if (cart.length === 0) {
    cart = [{ id: 'music', qty: 1, size: 'Medium (4x3 ft)' }];
    saveCart();
  }

  let appliedCoupon = null;
  try {
    appliedCoupon = localStorage.getItem(COUPON_KEY);
  } catch (e) {}

  function saveCart() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {}
    updateUI();
  }

  function getProduct(id) {
    if (window.FLAGSTER_PRODUCTS) {
      return window.FLAGSTER_PRODUCTS.find(p => p.id === id) || window.FLAGSTER_PRODUCTS[0];
    }
    return { id, title: 'Tapestry Flag', price: 500, mrp: 1000, img: 'products/music-is-my-drug.jpg' };
  }

  function showToast(msg) {
    let toast = document.getElementById('toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast';
      toast.className = 'toast';
      toast.innerHTML = '<span style="font-size: 16px;">✓</span><span id="toast-msg"></span>';
      document.body.appendChild(toast);
    }
    const msgEl = document.getElementById('toast-msg');
    if (msgEl) msgEl.textContent = msg;
    toast.classList.add('is-shown');
    setTimeout(() => toast.classList.remove('is-shown'), 2500);
  }

  window.addToCart = function(productId, qty = 1, size = 'Medium (4x3 ft)') {
    const existing = cart.find(item => item.id === productId && item.size === size);
    if (existing) {
      existing.qty += qty;
    } else {
      cart.push({ id: productId, qty: qty, size: size });
    }
    saveCart();
    const p = getProduct(productId);
    showToast(`Added "${p.title}" to cart!`);
    openCartDrawer();
  };

  window.updateCartQty = function(productId, delta, size = 'Medium (4x3 ft)') {
    const item = cart.find(x => x.id === productId && x.size === size);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
      cart = cart.filter(x => !(x.id === productId && x.size === size));
    }
    saveCart();
  };

  window.removeFromCart = function(productId, size = 'Medium (4x3 ft)') {
    cart = cart.filter(x => !(x.id === productId && x.size === size));
    saveCart();
    showToast('Item removed from cart');
  };

  window.applyCoupon = function() {
    const input = document.getElementById('coupon-input');
    if (!input) return;
    const code = input.value.trim().toUpperCase();
    if (code === 'FLAGSTER10' || code === 'PHEWMEW10') {
      appliedCoupon = code;
      try { localStorage.setItem(COUPON_KEY, code); } catch (e) {}
      showToast('Coupon applied: Extra 10% OFF!');
      saveCart();
    } else if (code) {
      alert('Invalid coupon code. Try FLAGSTER10 for 10% off!');
    }
  };

  function updateUI() {
    const totalCount = cart.reduce((sum, item) => sum + item.qty, 0);
    const subtotal = totalCount * 500;
    const mrpTotal = totalCount * 1000;
    let couponDiscount = 0;
    if (appliedCoupon) {
      couponDiscount = Math.round(subtotal * 0.10);
    }
    const finalSubtotal = subtotal - couponDiscount;
    const shipping = totalCount >= 2 ? 0 : (totalCount > 0 ? 50 : 0);
    const grandTotal = totalCount > 0 ? (finalSubtotal + shipping) : 0;

    // Badges in navbar
    document.querySelectorAll('.cart-pill-count, #nav-cart-badge').forEach(el => {
      el.textContent = totalCount;
    });

    const drawerCountEl = document.getElementById('cart-drawer-count');
    if (drawerCountEl) drawerCountEl.textContent = totalCount;

    // Shipping threshold
    const shippingMsgEl = document.getElementById('cart-shipping-msg');
    if (shippingMsgEl) {
      if (totalCount >= 2) {
        shippingMsgEl.innerHTML = '🎉 You unlocked <strong>FREE SHIPPING</strong> across India!';
        shippingMsgEl.style.color = '#10b981';
      } else if (totalCount === 1) {
        shippingMsgEl.innerHTML = '⚡ Add 1 more flag (₹500) to get <strong>FREE SHIPPING!</strong>';
        shippingMsgEl.style.color = '#e2e4ea';
      } else {
        shippingMsgEl.innerHTML = '⚡ Add 2 flags to unlock <strong>FREE SHIPPING!</strong>';
        shippingMsgEl.style.color = '#e2e4ea';
      }
    }

    // Render items in drawer
    const container = document.getElementById('cart-items-container');
    if (container) {
      if (cart.length === 0) {
        container.innerHTML = `
          <div class="cart-empty">
            <div style="font-size: 40px; margin-bottom: 12px;">🛒</div>
            <h4>Your cart is empty</h4>
            <p>Explore our trending tapestry drops to start.</p>
            <a href="shop.html" class="btn btn-secondary btn-sm" style="margin-top: 16px; display: inline-flex;">Shop Tapestries</a>
          </div>
        `;
      } else {
        container.innerHTML = cart.map(item => {
          const p = getProduct(item.id);
          return `
            <div class="cart-item">
              <div class="cart-item-img">
                <img src="${p.img}" alt="${p.title}">
              </div>
              <div class="cart-item-info">
                <div class="cart-item-title">${p.title}</div>
                <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 4px;">${item.size || 'Medium (4x3 ft)'}</div>
                <div class="cart-item-price">₹${p.price * item.qty} <span style="font-size: 11px; color: var(--text-dim); text-decoration: line-through;">₹${p.mrp * item.qty}</span></div>
                <div class="cart-item-controls">
                  <button class="qty-btn" onclick="updateCartQty('${p.id}', -1, '${item.size}')">-</button>
                  <span class="qty-num">${item.qty}</span>
                  <button class="qty-btn" onclick="updateCartQty('${p.id}', 1, '${item.size}')">+</button>
                  <button class="cart-item-remove" onclick="removeFromCart('${p.id}', '${item.size}')" title="Remove">&times;</button>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    // Subtotals
    const subtotalEl = document.getElementById('cart-subtotal-val');
    if (subtotalEl) subtotalEl.textContent = `₹${subtotal}`;

    const discountEl = document.getElementById('cart-discount-val');
    if (discountEl) {
      const totalDisc = (mrpTotal - subtotal) + couponDiscount;
      discountEl.textContent = `-₹${totalDisc}`;
    }

    const shippingEl = document.getElementById('cart-shipping-val');
    if (shippingEl) shippingEl.textContent = shipping === 0 ? 'FREE' : `₹${shipping}`;

    const totalEl = document.getElementById('cart-total-val');
    if (totalEl) totalEl.textContent = `₹${grandTotal}`;

    // Modal
    const modalCountEl = document.getElementById('modal-item-count');
    if (modalCountEl) modalCountEl.textContent = `${totalCount} item${totalCount === 1 ? '' : 's'}`;

    const modalTotalEl = document.getElementById('modal-final-total');
    if (modalTotalEl) modalTotalEl.textContent = `₹${grandTotal}`;
  }

  function openCartDrawer() {
    const drawer = document.getElementById('cart-backdrop');
    if (drawer) drawer.classList.add('is-open');
  }
  function closeCartDrawer() {
    const drawer = document.getElementById('cart-backdrop');
    if (drawer) drawer.classList.remove('is-open');
  }

  window.openCart = openCartDrawer;
  window.closeCart = closeCartDrawer;

  window.openCheckout = function() {
    if (cart.length === 0) {
      showToast('Your cart is empty! Add a flag first.');
      return;
    }
    closeCartDrawer();
    const modal = document.getElementById('checkout-modal');
    if (modal) {
      modal.classList.add('is-open');
      document.getElementById('checkout-form-view').style.display = 'block';
      document.getElementById('checkout-success-view').style.display = 'none';
    }
  };

  window.closeCheckout = function() {
    const modal = document.getElementById('checkout-modal');
    if (modal) modal.classList.remove('is-open');
  };

  window.selectPayment = function(el, method) {
    document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('is-selected'));
    el.classList.add('is-selected');
  };

  window.handlePlaceOrder = function(e) {
    e.preventDefault();
    const orderId = Math.floor(10000 + Math.random() * 90000);
    const confirmedEl = document.getElementById('confirmed-order-id');
    if (confirmedEl) confirmedEl.textContent = orderId;
    document.getElementById('checkout-form-view').style.display = 'none';
    document.getElementById('checkout-success-view').style.display = 'block';
    cart = [];
    saveCart();
  };

  // Wire up listeners when DOM is loaded
  document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('open-cart-btn');
    if (openBtn) openBtn.addEventListener('click', openCartDrawer);

    const closeBtn = document.getElementById('cart-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', closeCartDrawer);

    const backdrop = document.getElementById('cart-backdrop');
    if (backdrop) backdrop.addEventListener('click', function(e) {
      if (e.target === this) closeCartDrawer();
    });

    const checkoutBtn = document.getElementById('cart-checkout-btn');
    if (checkoutBtn) checkoutBtn.addEventListener('click', window.openCheckout);

    const modalCloseBtn = document.getElementById('modal-close-btn');
    if (modalCloseBtn) modalCloseBtn.addEventListener('click', window.closeCheckout);

    const modalBackdrop = document.getElementById('checkout-modal');
    if (modalBackdrop) modalBackdrop.addEventListener('click', function(e) {
      if (e.target === this) window.closeCheckout();
    });

    updateUI();
  });

  window.flagsterCart = {
    add: window.addToCart,
    open: openCartDrawer,
    close: closeCartDrawer
  };
})();
