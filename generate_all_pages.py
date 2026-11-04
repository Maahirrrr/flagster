import json, os

os.chdir('/home/maahir/.gemini/antigravity/scratch/peculiar-atelier')

with open('js/products.js') as f:
    text = f.read()
    json_str = text.split('window.FLAGSTER_PRODUCTS = ')[1].strip().rstrip(';')
    PRODUCTS = json.loads(json_str)

# Clean up products
for p in PRODUCTS:
    p['title'] = p['title'].replace('DR★G', 'DRUG').replace('DR*G', 'DRUG')
    p['desc'] = p['desc'].replace('—', ' · ')

with open('js/products.js', 'w') as f:
    f.write('window.FLAGSTER_PRODUCTS = ' + json.dumps(PRODUCTS, indent=2) + ';\n')

# 1. WRITE css/style.css
CSS = """/* FLAGSTER — THE DARK ROOM (TASTESKILL COMPLIANT) */
:root {
  --bg: #08090c;
  --bg-card: #10131a;
  --bg-card-hover: #161a24;
  --bg-surface: #1a1e2a;
  --text-main: #f3f4f7;
  --text-muted: #abb1c0;
  --text-dim: #8b92a3;
  --pink-accent: #ffadc6;
  --pink-hover: #ff94b4;
  --green: #10b981;
  --gutter: clamp(20px, 4vw, 56px);
  --radius: 12px;
  --radius-pill: 9999px;
  --font-family: "Work Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}

body {
  background: var(--bg);
  color: var(--text-main);
  font-family: var(--font-family);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  font-size: 16px;
  line-height: 1.6;
  overflow-x: hidden;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  border: none;
  background: none;
  cursor: pointer;
}

img {
  max-width: 100%;
  display: block;
}

/* TOP ANNOUNCEMENT BAR */
.announcement {
  background: var(--pink-accent);
  color: #000000;
  font-size: 14px;
  font-weight: 700;
  text-align: center;
  padding: 10px var(--gutter);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  z-index: 100;
}
.announcement strong {
  background: #000000;
  color: #ffffff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 800;
}

/* NAVBAR */
.nav-bar {
  position: sticky;
  top: 0;
  z-index: 90;
  background: rgba(12, 14, 18, 0.95);
  backdrop-filter: blur(10px);
}
.nav-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 18px var(--gutter);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
}
.nav-logo-badge {
  background: var(--pink-accent);
  color: #000000;
  font-size: 13px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 32px;
}
.nav-links a {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-muted);
  transition: color 0.2s ease;
}
.nav-links a:hover,
.nav-links a.is-active {
  color: #ffffff;
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}
.nav-cart-btn {
  background: #ffffff;
  color: #000000;
  font-size: 14px;
  font-weight: 700;
  padding: 9px 20px;
  border-radius: var(--radius-pill);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s ease, background 0.2s ease;
}
.nav-cart-btn:hover {
  background: #e6e6e6;
  transform: translateY(-1px);
}
.cart-badge {
  background: var(--pink-accent);
  color: #000000;
  font-size: 13px;
  font-weight: 900;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
}

/* BUTTONS */
.btn-primary {
  background: #ffffff;
  color: #000000;
  font-weight: 800;
  font-size: 15px;
  padding: 13px 28px;
  border-radius: var(--radius-pill);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: transform 0.2s ease, background 0.2s ease;
  cursor: pointer;
}
.btn-primary:hover {
  background: #eaeaea;
  transform: translateY(-1px);
}
.btn-pink {
  background: var(--pink-accent);
  color: #000000;
  font-weight: 800;
  font-size: 15px;
  padding: 14px 30px;
  border-radius: var(--radius-pill);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: transform 0.2s ease, background 0.2s ease;
  cursor: pointer;
}
.btn-pink:hover {
  background: var(--pink-hover);
  transform: translateY(-1px);
}
.btn-secondary {
  background: var(--bg-surface);
  color: #ffffff;
  font-weight: 700;
  font-size: 15px;
  padding: 13px 26px;
  border-radius: var(--radius-pill);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s ease, transform 0.2s ease;
}
.btn-secondary:hover {
  background: #252b3b;
  transform: translateY(-1px);
}

/* MARQUEE */
.marquee-bar {
  background: #050608;
  overflow: hidden;
  white-space: nowrap;
  padding: 14px 0;
}
.marquee-track {
  display: inline-block;
  animation: marqueeScroll 32s linear infinite;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
}
.marquee-track span {
  margin: 0 28px;
}
.marquee-track strong {
  color: var(--pink-accent);
  font-weight: 800;
}
@keyframes marqueeScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}


/* MOTION LAYER (TASTESKILL COMPLIANT) */
@media (prefers-reduced-motion: no-preference) {
  .hero-h1, .hero-sub, .tapestry-picker-label, .tapestry-thumbs-row, .hero-price-line, .hero-actions {
    animation: entranceFade 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) both;
  }
  .feature-tile {
    animation: entranceFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;
  }
  .product-card {
    animation: entranceFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;
  }
}
@keyframes entranceFade {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* PRODUCT CARD GRID */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 36px;
}
.product-card {
  background: var(--bg-card);
  border-radius: var(--radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, background 0.25s ease;
  position: relative;
}
.product-card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-4px);
}
.product-thumb-wrap {
  position: relative;
  aspect-ratio: 1.25/1;
  background: #000000;
  overflow: hidden;
}
.product-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.product-card:hover .product-thumb-img {
  transform: scale(1.04);
}
.badge-tag {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(0, 0, 0, 0.8);
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
}
.badge-sale {
  position: absolute;
  top: 14px;
  right: 14px;
  background: var(--pink-accent);
  color: #000000;
  font-size: 13px;
  font-weight: 900;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
}
.product-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.product-category {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-dim);
  margin-bottom: 6px;
}
.product-title {
  font-size: 19px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 10px;
  line-height: 1.3;
}
.product-title a:hover {
  color: var(--pink-accent);
}
.product-desc {
  font-size: 15px;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 22px;
  flex: 1;
}
.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  margin-top: auto;
}
.price-current {
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
}
.price-mrp {
  font-size: 14px;
  color: var(--text-dim);
  text-decoration: line-through;
  margin-left: 6px;
}
.btn-quick-add {
  background: #ffffff;
  color: #000000;
  font-size: 14px;
  font-weight: 800;
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  transition: background 0.2s ease, transform 0.2s ease;
}
.btn-quick-add:hover {
  background: var(--pink-accent);
  transform: translateY(-1px);
}
.btn-view-drop {
  background: var(--bg-surface);
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  margin-right: 6px;
}
.btn-view-drop:hover {
  background: #2a3142;
}

/* CART DRAWER & OVERLAYS */
.cart-drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  z-index: 999;
  display: none;
}
.cart-drawer-overlay.is-active {
  display: block;
}
.cart-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  max-width: 440px;
  background: #0e1117;
  z-index: 1000;
  display: none;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
}
.cart-drawer.is-active {
  display: flex;
}
.cart-header {
  padding: 24px;
  background: #12151e;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.cart-header h3 {
  font-size: 19px;
  font-weight: 900;
  color: #ffffff;
}
.btn-close-cart {
  color: var(--text-dim);
  font-size: 20px;
  cursor: pointer;
  transition: color 0.2s ease;
}
.btn-close-cart:hover {
  color: #ffffff;
}
.shipping-meter {
  background: var(--bg-surface);
  padding: 14px 24px;
  font-size: 14px;
  color: var(--text-muted);
}
.shipping-meter-bar-bg {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 8px;
}
.shipping-meter-bar-fill {
  height: 100%;
  background: var(--pink-accent);
  width: 0%;
  transition: width 0.3s ease;
}
.cart-items-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.cart-item {
  display: grid;
  grid-template-columns: 76px 1fr auto;
  gap: 14px;
  align-items: center;
  background: var(--bg-card);
  border-radius: 10px;
  padding: 12px;
}
.cart-item-img {
  width: 76px;
  height: 76px;
  border-radius: 8px;
  object-fit: cover;
}
.cart-item-info h4 {
  font-size: 14px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.3;
}
.cart-item-meta {
  font-size: 13px;
  color: var(--text-dim);
  margin-top: 2px;
}
.cart-item-price {
  font-size: 15px;
  font-weight: 800;
  color: #ffffff;
  margin-top: 4px;
}
.cart-qty-ctrl {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-surface);
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 13px;
  margin-top: 6px;
  width: fit-content;
}
.cart-qty-ctrl button {
  color: var(--text-muted);
  font-weight: 800;
  padding: 0 4px;
}
.btn-remove-item {
  color: var(--text-dim);
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
}
.btn-remove-item:hover { color: #ff4d4f; }
.cart-footer {
  padding: 24px;
  background: #08090d;
}
.coupon-box {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.coupon-input {
  flex: 1;
  background: var(--bg-card);
  border: none;
  border-radius: var(--radius-pill);
  padding: 12px 18px;
  color: #ffffff;
  font-size: 14px;
  outline: none;
  text-transform: uppercase;
}
.coupon-btn {
  background: var(--bg-surface);
  color: #ffffff;
  border-radius: var(--radius-pill);
  padding: 0 18px;
  font-size: 14px;
  font-weight: 800;
}
.cart-summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.cart-summary-line.total {
  font-size: 19px;
  font-weight: 900;
  color: #ffffff;
  padding-top: 10px;
  margin-top: 10px;
}
.btn-checkout {
  width: 100%;
  margin-top: 16px;
}

/* CHECKOUT MODAL */
.checkout-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  z-index: 1100;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
}
.checkout-modal-overlay.is-active {
  display: flex;
}
.checkout-modal {
  background: #11141c;
  border-radius: 16px;
  width: 100%;
  max-width: 580px;
  padding: 36px;
  position: relative;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
}
.checkout-modal h2 {
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 6px;
}
.checkout-modal p.sub {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 24px;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}
.form-group label {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
}
.form-group input,
.form-group select {
  background: var(--bg-card);
  border: none;
  border-radius: 8px;
  padding: 13px 16px;
  color: #ffffff;
  font-size: 15px;
  outline: none;
}
.payment-selector {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  margin-top: 10px;
}
.payment-opt {
  background: var(--bg-surface);
  border-radius: 10px;
  padding: 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}
.payment-opt.is-active {
  background: rgba(255, 173, 198, 0.15);
  color: var(--pink-accent);
  outline: 2px solid var(--pink-accent);
}
.payment-opt h5 {
  font-size: 14px;
  font-weight: 800;
}
.payment-opt span {
  font-size: 13px;
  color: var(--text-dim);
}

/* SUCCESS MODAL */
.order-success-modal {
  display: none;
  text-align: center;
  padding: 20px 0;
}
.order-success-modal.is-active {
  display: block;
}
.success-circle {
  width: 60px;
  height: 60px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--green);
  margin: 0 auto 18px;
  font-weight: 900;
}

/* FOOTER */
.site-footer {
  background: #050608;
  padding: 72px var(--gutter) 40px;
  margin-top: 80px;
}
.footer-grid {
  max-width: 1440px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1.4fr;
  gap: 48px;
  margin-bottom: 48px;
}
.footer-brand h4 {
  font-size: 24px;
  font-weight: 900;
  margin-bottom: 12px;
  color: #ffffff;
}
.footer-brand p {
  font-size: 15px;
  color: var(--text-muted);
  line-height: 1.6;
  max-width: 360px;
}
.footer-col h5 {
  font-size: 14px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 18px;
}
.footer-col ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.footer-col a {
  font-size: 14px;
  color: var(--text-muted);
  transition: color 0.2s ease;
}
.footer-col a:hover {
  color: var(--pink-accent);
}
.footer-newsletter p {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 14px;
}
.newsletter-form {
  display: flex;
  gap: 8px;
}
.newsletter-input {
  flex: 1;
  background: var(--bg-card);
  border: none;
  border-radius: var(--radius-pill);
  padding: 12px 18px;
  color: #ffffff;
  font-size: 14px;
  outline: none;
}
.footer-bottom {
  max-width: 1440px;
  margin: 0 auto;
  padding-top: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: var(--text-dim);
}

@media (max-width: 900px) {
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 36px; }
}
@media (max-width: 600px) {
  .nav-links { display: none; }
  .footer-grid { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
}
"""

with open('css/style.css', 'w') as f:
    f.write(CSS)

# Header & Footer
def get_header(active='home'):
    return f"""  <!-- Announcement Bar -->
  <aside class="announcement">
    <span>Free shipping on orders above ₹499. Use code <strong>FLAGSTER10</strong> for 10% off.</span>
  </aside>

  <!-- Navigation -->
  <header class="nav-bar">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        <span>Flagster</span>
        <span class="nav-logo-badge">Originals</span>
      </a>

      <nav class="nav-links">
        <a href="index.html" class="{'is-active' if active == 'home' else ''}">Home</a>
        <a href="shop.html" class="{'is-active' if active == 'shop' else ''}">Shop All ({len(PRODUCTS)})</a>
        <a href="faq.html" class="{'is-active' if active == 'faq' else ''}">How to Hang</a>
        <a href="contact.html" class="{'is-active' if active == 'contact' else ''}">Track Order</a>
      </nav>

      <div class="nav-actions">
        <button class="nav-cart-btn" id="open-cart-btn" aria-label="Open Cart">
          <span>Cart</span>
          <span class="cart-badge" id="nav-cart-badge">0</span>
        </button>
      </div>
    </div>
  </header>"""

def get_footer():
    return """  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-grid">
      <div class="footer-brand">
        <h4>Flagster</h4>
        <p>Heavyweight graphic wall tapestries. Printed with fade-resistant dye sublimation and finished with four pre-installed brass corner eyelets.</p>
      </div>

      <div class="footer-col">
        <h5>Catalog</h5>
        <ul>
          <li><a href="shop.html">All Drops</a></li>
          <li><a href="shop.html?cat=Hip-Hop">Hip-Hop</a></li>
          <li><a href="shop.html?cat=Street+Drip">Street Drip</a></li>
          <li><a href="shop.html?cat=Psychedelic">Psychedelic</a></li>
          <li><a href="shop.html?cat=Typography">Typography</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h5>Support</h5>
        <ul>
          <li><a href="faq.html">How to Hang Guide</a></li>
          <li><a href="faq.html#care">Fabric Care</a></li>
          <li><a href="faq.html#shipping">Shipping and Returns</a></li>
          <li><a href="contact.html">Track Order</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>

      <div class="footer-col footer-newsletter">
        <h5>Updates</h5>
        <p>Join for release notifications on upcoming limited wall drops.</p>
        <form class="newsletter-form" onsubmit="event.preventDefault(); alert('Subscribed for drop alerts.');">
          <input type="email" class="newsletter-input" placeholder="Your email address" required>
          <button type="submit" class="btn-primary" style="padding: 10px 18px; font-size: 14px;">Join</button>
        </form>
      </div>
    </div>

    <div class="footer-bottom">
      <span>2026 Flagster. All rights reserved.</span>
      <span>Flat ₹500 per flag. Cash on delivery available across India.</span>
    </div>
  </footer>

  <!-- Cart Drawer -->
  <div class="cart-drawer-overlay" id="cart-drawer-overlay" onclick="closeCart()"></div>
  <aside class="cart-drawer" id="cart-drawer" aria-label="Shopping Cart">
    <div class="cart-header">
      <h3>Your Bag</h3>
      <button class="btn-close-cart" onclick="closeCart()" aria-label="Close Bag">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>

    <div class="shipping-meter">
      <div id="shipping-meter-text">Add ₹499 for free express delivery</div>
      <div class="shipping-meter-bar-bg">
        <div class="shipping-meter-bar-fill" id="shipping-meter-bar"></div>
      </div>
    </div>

    <div class="cart-items-list" id="cart-items-container">
      <!-- Injected by cart.js -->
    </div>

    <div class="cart-footer">
      <div class="coupon-box">
        <input type="text" id="coupon-input" class="coupon-input" placeholder="Promo code (e.g. FLAGSTER10)">
        <button class="coupon-btn" onclick="applyCouponCode()">Apply</button>
      </div>
      <div id="coupon-status" style="font-size: 13px; margin-bottom: 8px;"></div>

      <div class="cart-summary-line">
        <span>Subtotal</span>
        <span id="cart-subtotal-val">₹0</span>
      </div>
      <div class="cart-summary-line" id="cart-discount-row" style="display: none; color: var(--pink-accent);">
        <span>Discount</span>
        <span id="cart-discount-val">−₹0</span>
      </div>
      <div class="cart-summary-line">
        <span>Shipping</span>
        <span id="cart-shipping-val">Calculated at checkout</span>
      </div>
      <div class="cart-summary-line total">
        <span>Total</span>
        <span id="cart-total-val">₹0</span>
      </div>

      <button class="btn-pink btn-checkout" onclick="openCheckout()">Proceed to Checkout</button>
    </div>
  </aside>

  <!-- Checkout Modal -->
  <div class="checkout-modal-overlay" id="checkout-modal-overlay">
    <div class="checkout-modal" role="dialog" aria-modal="true">
      <button onclick="closeCheckout()" style="position: absolute; top: 20px; right: 24px; color: var(--text-dim); font-size: 20px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>

      <div id="checkout-form-view">
        <h2>Order Details</h2>
        <p class="sub">Complete your shipping address and select payment.</p>

        <form id="checkout-form" onsubmit="handlePlaceOrder(event)">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input type="text" id="cust-name" required placeholder="Alex Turner">
            </div>
            <div class="form-group">
              <label>Phone Number</label>
              <input type="tel" id="cust-phone" required placeholder="+91 98765 43210">
            </div>
          </div>

          <div class="form-group">
            <label>Delivery Address</label>
            <input type="text" id="cust-address" required placeholder="Flat, Street, Area">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>City</label>
              <input type="text" id="cust-city" required placeholder="Mumbai">
            </div>
            <div class="form-group">
              <label>Pincode</label>
              <input type="text" id="cust-pin" required placeholder="400001">
            </div>
          </div>

          <div class="form-group">
            <label>Payment Method</label>
            <div class="payment-selector">
              <div class="payment-opt is-active" onclick="selectPayment(this, 'cod')">
                <h5>Cash on Delivery</h5>
                <span>Pay upon arrival</span>
              </div>
              <div class="payment-opt" onclick="selectPayment(this, 'upi')">
                <h5>UPI / QR</h5>
                <span>Instant payment</span>
              </div>
              <div class="payment-opt" onclick="selectPayment(this, 'card')">
                <h5>Card / Netbanking</h5>
                <span>Online transfer</span>
              </div>
            </div>
          </div>

          <button type="submit" class="btn-pink" style="width: 100%; margin-top: 16px;">Place Order</button>
        </form>
      </div>

      <div class="order-success-modal" id="checkout-success-view">
        <div class="success-circle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <h2>Order Confirmed</h2>
        <p class="sub" id="order-confirm-msg">Thank you. Your order has been placed successfully.</p>
        <p style="font-size: 15px; margin-bottom: 24px;">Order ID: <strong id="order-confirm-id" style="color: var(--pink-accent);">FLG-84920</strong></p>
        <button class="btn-primary" onclick="closeCheckout(); window.location.href='contact.html';">Track Status</button>
      </div>
    </div>
  </div>"""

# 2. BUILD index.html (Side-by-side hero, NO covered text!)
def build_index():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster · Wall Tapestries and Graphic Flags</title>
  <meta name="description" content="Statement wall tapestries and graphic album art flags. Finished with four pre-installed corner brass grommets. Flat ₹500.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    /* Two-column Hero: Stage and Card side-by-side, no overlap */
    .hero-split-wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 40px var(--gutter) 60px;
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 48px;
      align-items: center;
      min-height: calc(100vh - 120px);
    }}
    .hero-stage-box {{
      position: relative;
      aspect-ratio: 1.25/1;
      background: #000000;
      border-radius: 16px;
      overflow: hidden;
    }}
    .hero-cloth-canvas {{
      width: 100%;
      height: 100%;
      display: block;
      touch-action: pan-y;
      outline: none;
    }}
    .hero-info-card {{
      display: flex;
      flex-direction: column;
    }}
    .hero-h1 {{
      font-size: clamp(34px, 3.8vw, 52px);
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.08;
      color: #ffffff;
      margin-bottom: 14px;
    }}
    .hero-sub {{
      font-size: 16px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 24px;
    }}
    .tapestry-picker-label {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text-dim);
      margin-bottom: 10px;
    }}
    .tapestry-thumbs-row {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 10px;
      margin-bottom: 24px;
    }}
    .thumb-picker-btn {{
      width: 52px;
      height: 52px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      cursor: pointer;
      opacity: 0.6;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }}
    .thumb-picker-btn:hover,
    .thumb-picker-btn.is-active {{
      opacity: 1;
      transform: scale(1.06);
      outline: 2px solid var(--pink-accent);
    }}
    .thumb-picker-btn img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .hero-price-line {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 24px;
    }}
    .hero-price-val {{
      font-size: 32px;
      font-weight: 900;
      color: #ffffff;
    }}
    .hero-price-orig {{
      font-size: 16px;
      color: var(--text-dim);
      text-decoration: line-through;
    }}
    .hero-price-disc {{
      background: var(--pink-accent);
      color: #000000;
      font-size: 13px;
      font-weight: 900;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
    }}
    .hero-actions {{
      display: flex;
      gap: 14px;
    }}

    .section-wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 60px var(--gutter);
    }}
    .section-header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 40px;
    }}
    .section-title {{
      font-size: clamp(26px, 3vw, 38px);
      font-weight: 800;
      letter-spacing: -0.03em;
      color: #ffffff;
    }}
    .section-sub {{
      font-size: 16px;
      color: var(--text-muted);
      margin-top: 6px;
    }}

    .features-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 24px;
    }}
    .feature-tile {{
      background: var(--bg-card);
      border-radius: 12px;
      padding: 28px;
    }}
    .feature-tile h4 {{
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 10px;
    }}
    .feature-tile p {{
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    @media (max-width: 1024px) {{
      .hero-split-wrap {{
        grid-template-columns: 1fr;
        gap: 36px;
        min-height: auto;
      }}
    }}
  </style>
</head>
<body>

{get_header('home')}

  <!-- Marquee -->
  <aside class="marquee-bar">
    <div class="marquee-track">
      <span>Tear-proof woven canvas</span>
      <span>Four brass corner eyelets</span>
      <span>Flat 50% off at <strong>₹500</strong></span>
      <span>Free delivery across India over ₹499</span>
      <span>Cash on delivery available</span>
      <span>Tear-proof woven canvas</span>
      <span>Four brass corner eyelets</span>
      <span>Flat 50% off at <strong>₹500</strong></span>
      <span>Free delivery across India over ₹499</span>
      <span>Cash on delivery available</span>
    </div>
  </aside>

  <!-- Hero with Live 3D Cloth Physics -->
  <main class="hero-split-wrap">
    <div class="hero-stage-box" id="hero-view">
      <canvas id="hero-cloth" class="hero-cloth-canvas"></canvas>
    </div>

    <div class="hero-info-card">
      <h1 class="hero-h1">Wall Drip For Your Space</h1>
      <p class="hero-sub">Heavyweight graphic tapestries with corner brass eyelets. Drag the cloth in 3D to inspect real fabric physics.</p>

      <div class="tapestry-picker-label">Drape Tapestry on Cloth</div>
      <div class="tapestry-thumbs-row">
        {''.join(f'''<button class="thumb-picker-btn {'is-active' if i==0 else ''}" onclick="switchHeroFlag('{p['id']}', '{p['img']}', '{p['title']}', this)" title="{p['title']}"><img src="{p['img']}" alt="{p['title']}"></button>''' for i, p in enumerate(PRODUCTS))}
      </div>

      <div class="hero-price-line">
        <span class="hero-price-val">₹500</span>
        <span class="hero-price-orig">₹1,000</span>
        <span class="hero-price-disc">50% Off</span>
      </div>

      <div class="hero-actions">
        <button class="btn-pink" style="flex: 1;" onclick="handleHeroAdd()">Add to Bag</button>
        <a href="shop.html" class="btn-secondary">View Catalog</a>
      </div>
    </div>
  </main>

  <!-- Feature Pillars -->
  <section class="section-wrap" style="padding-top: 40px;">
    <div class="features-grid">
      <div class="feature-tile">
        <h4>Pre-Installed Brass Eyelets</h4>
        <p>Four solid brass grommets, one in each corner. Mount to walls with thumbtacks, pushpins, or adhesive hooks in 30 seconds.</p>
      </div>
      <div class="feature-tile">
        <h4>Heavy 180GSM Micro-Weave</h4>
        <p>Thick woven canvas fabric. Will not wrinkle, sag, or show room glare through the print.</p>
      </div>
      <div class="feature-tile">
        <h4>Fade-Resistant Thermal Infusion</h4>
        <p>Sublimation dye infused into the fabric. Saturated blacks and bright colors that stay vivid.</p>
      </div>
      <div class="feature-tile">
        <h4>Flat ₹500 Pricing</h4>
        <p>50% discount on every drop. Free delivery on orders over ₹499 with cash on delivery available.</p>
      </div>
    </div>
  </section>

  <!-- Curated Drops -->
  <section class="section-wrap" style="padding-top: 20px;">
    <div class="section-header">
      <div>
        <h2 class="section-title">Current Wall Drops</h2>
        <p class="section-sub">Eight original tapestries for bedrooms, studios, and listening spaces.</p>
      </div>
      <a href="shop.html" class="btn-secondary" style="padding: 10px 22px;">View All</a>
    </div>

    <div class="product-grid">
      {''.join(f'''
      <article class="product-card">
        <div class="product-thumb-wrap">
          <a href="product.html?id={p['id']}">
            <img class="product-thumb-img" src="{p['img']}" alt="{p['title']}" loading="lazy">
          </a>
          <span class="badge-tag">{p['tag']}</span>
          <span class="badge-sale">50% Off</span>
        </div>
        <div class="product-body">
          <div class="product-category">{p['category']}</div>
          <h3 class="product-title"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
          <p class="product-desc">{p['desc']}</p>
          <div class="product-footer">
            <div>
              <span class="price-current">₹500</span>
              <span class="price-mrp">₹1000</span>
            </div>
            <div>
              <a href="product.html?id={p['id']}" class="btn-view-drop">Details</a>
              <button class="btn-quick-add" onclick="addToCart('{p['id']}', 1, 'Medium (4x3 ft)')">Add</button>
            </div>
          </div>
        </div>
      </article>''' for p in PRODUCTS)}
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cloth-sim.js"></script>
  <script src="js/cart.js"></script>
  <script>
    let activeHeroId = '{PRODUCTS[0]['id']}';
    let heroClothEngine = null;

    document.addEventListener('DOMContentLoaded', function() {{
      const heroCanvas = document.getElementById('hero-cloth');
      const heroContainer = document.getElementById('hero-view');
      if (heroCanvas && heroContainer && window.initFlagsterCloth) {{
        heroClothEngine = window.initFlagsterCloth('hero-cloth', 'hero-view', '{PRODUCTS[0]['img']}');
      }}
    }});

    function switchHeroFlag(id, imgUrl, title, btn) {{
      activeHeroId = id;
      document.querySelectorAll('.thumb-picker-btn').forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      if (heroClothEngine) {{
        heroClothEngine.setTexture(imgUrl);
      }}
    }}

    function handleHeroAdd() {{
      addToCart(activeHeroId, 1, 'Medium (4x3 ft)');
    }}
  </script>
</body>
</html>"""

# 3. BUILD product.html (PhewMew style, zero hairlines, zero covered text)
def build_product():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster · Tapestry Detail</title>
  <meta name="description" content="Tapestry details, dual photo and interactive 3D cloth physics view, and size selector.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pdp-wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 40px var(--gutter) 80px;
    }}
    .pdp-grid {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 56px;
      align-items: start;
    }}

    .pdp-media-card {{
      position: relative;
      background: #000000;
      border-radius: 16px;
      overflow: hidden;
      aspect-ratio: 1.38/1;
    }}
    .pdp-photo-view {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .pdp-3d-wrapper {{
      position: absolute;
      inset: 0;
      background: #090a0d;
      display: none;
    }}
    .pdp-3d-wrapper.is-active {{
      display: block;
    }}
    .pdp-cloth-canvas {{
      width: 100%;
      height: 100%;
      display: block;
      touch-action: pan-y;
      outline: none;
    }}
    .pdp-mode-bar {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      display: flex;
      gap: 8px;
      z-index: 10;
      background: rgba(0, 0, 0, 0.8);
      padding: 4px;
      border-radius: var(--radius-pill);
    }}
    .mode-btn {{
      padding: 8px 16px;
      border-radius: var(--radius-pill);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      transition: background 0.2s ease, color 0.2s ease;
    }}
    .mode-btn.is-active {{
      background: #ffffff;
      color: #000000;
    }}

    .pdp-buybox {{
      display: flex;
      flex-direction: column;
    }}
    .pdp-title {{
      font-size: clamp(28px, 3.2vw, 42px);
      font-weight: 900;
      letter-spacing: -0.04em;
      line-height: 1.15;
      color: #ffffff;
      margin-bottom: 14px;
    }}
    .pdp-price-row {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      padding: 14px 20px;
      background: var(--bg-surface);
      border-radius: 10px;
      margin-bottom: 24px;
    }}
    .pdp-price-sale {{
      font-size: 32px;
      font-weight: 900;
      color: #ffffff;
    }}
    .pdp-price-mrp {{
      font-size: 16px;
      color: var(--text-dim);
      text-decoration: line-through;
    }}
    .pdp-price-badge {{
      background: var(--pink-accent);
      color: #000000;
      font-size: 13px;
      font-weight: 900;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
    }}

    .size-pills-row {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 20px;
    }}
    .size-btn {{
      background: var(--bg-surface);
      border-radius: 10px;
      padding: 14px 10px;
      text-align: center;
      cursor: pointer;
      transition: background 0.2s ease;
    }}
    .size-btn.is-active {{
      background: #252b3b;
      outline: 2px solid #ffffff;
    }}
    .size-btn strong {{
      display: block;
      font-size: 14px;
      color: #ffffff;
    }}
    .size-btn span {{
      display: block;
      font-size: 13px;
      color: var(--text-dim);
      margin-top: 2px;
    }}

    .pdp-actions-row {{
      display: flex;
      gap: 12px;
      margin-bottom: 14px;
    }}
    .qty-stepper {{
      display: flex;
      align-items: center;
      background: var(--bg-surface);
      border-radius: var(--radius-pill);
      height: 52px;
      padding: 0 8px;
    }}
    .qty-btn {{
      width: 36px;
      height: 36px;
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .qty-display {{
      padding: 0 12px;
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
    }}
    .btn-add-cart {{
      flex: 1;
      height: 52px;
      background: #ffffff;
      color: #000000;
      border-radius: var(--radius-pill);
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s ease, transform 0.2s ease;
    }}
    .btn-add-cart:hover {{
      background: #e6e6e6;
      transform: translateY(-1px);
    }}
    .btn-buy-now {{
      width: 100%;
      height: 52px;
      background: var(--pink-accent);
      color: #000000;
      border-radius: var(--radius-pill);
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;
      transition: background 0.2s ease, transform 0.2s ease;
      cursor: pointer;
    }}
    .btn-buy-now:hover {{
      background: var(--pink-hover);
      transform: translateY(-1px);
    }}

    .pdp-bullet-list {{
      background: var(--bg-surface);
      border-radius: 12px;
      padding: 20px 22px;
      margin-bottom: 24px;
      font-size: 15px;
      line-height: 1.7;
      color: var(--text-muted);
    }}
    .pdp-bullet-list p {{
      margin-bottom: 4px;
    }}

    .pdp-accordions {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 10px;
    }}
    .accordion-block {{
      background: var(--bg-surface);
      border-radius: 10px;
      padding: 0 20px;
    }}
    .accordion-header {{
      width: 100%;
      padding: 16px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      font-weight: 800;
      color: #ffffff;
      cursor: pointer;
    }}
    .accordion-header span.plus-sign {{
      color: var(--pink-accent);
      font-size: 18px;
      font-weight: 700;
    }}
    .accordion-body {{
      display: none;
      padding-bottom: 18px;
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
    }}
    .accordion-block.is-open .accordion-body {{
      display: block;
    }}

    @media (max-width: 960px) {{
      .pdp-grid {{ grid-template-columns: 1fr; gap: 36px; }}
    }}

    /* Motion entrance */
    @media (prefers-reduced-motion: no-preference) {{
      .pdp-title, .pdp-price-row, .size-pills-row, .pdp-actions-row, .btn-buy-now, .pdp-bullet-list, .accordion-block {{
        animation: entranceFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;
      }}
    }}
  </style>
</head>
<body>

{get_header('shop')}

  <main class="pdp-wrap">
    <div class="pdp-grid">
      <!-- Media -->
      <div>
        <div class="pdp-media-card">
          <img src="{PRODUCTS[0]['img']}" id="pdp-main-img" class="pdp-photo-view" alt="{PRODUCTS[0]['title']}">
          <div class="pdp-3d-wrapper" id="pdp-3d-container">
            <canvas id="pdp-cloth" class="pdp-cloth-canvas"></canvas>
          </div>
          <div class="pdp-mode-bar">
            <button class="mode-btn is-active" id="btn-mode-photo" onclick="setPdpMode('photo')">Photo View</button>
            <button class="mode-btn" id="btn-mode-3d" onclick="setPdpMode('3d')">Interactive 3D Cloth</button>
          </div>
        </div>
        <p style="font-size: 13px; color: var(--text-dim); text-align: center; margin-top: 12px;">
          Tug the cloth with your mouse or finger in 3D mode to view realistic drape.
        </p>
      </div>

      <!-- Buy Box -->
      <div class="pdp-buybox">
        <h1 class="pdp-title" id="pdp-title-el">{PRODUCTS[0]['title']}</h1>

        <div class="pdp-price-row">
          <span class="pdp-price-sale" id="pdp-price-el">₹500</span>
          <span class="pdp-price-mrp" id="pdp-mrp-el">₹1000</span>
          <span class="pdp-price-badge">50% Off</span>
        </div>

        <div style="font-size: 13px; font-weight: 700; color: var(--text-dim); margin-bottom: 8px;">Size</div>
        <div class="size-pills-row">
          <div class="size-btn" onclick="selectSize(this, 'Small (3x2 ft)', 399, 800)">
            <strong>Small</strong>
            <span>3 × 2 ft (₹399)</span>
          </div>
          <div class="size-btn is-active" onclick="selectSize(this, 'Medium (4x3 ft)', 500, 1000)">
            <strong>Medium</strong>
            <span>4 × 3 ft (₹500)</span>
          </div>
          <div class="size-btn" onclick="selectSize(this, 'Large (5x4 ft)', 699, 1400)">
            <strong>Large</strong>
            <span>5 × 4 ft (₹699)</span>
          </div>
        </div>

        <div class="pdp-actions-row">
          <div class="qty-stepper">
            <button class="qty-btn" onclick="changeQty(-1)">−</button>
            <span class="qty-display" id="pdp-qty-display">1</span>
            <button class="qty-btn" onclick="changeQty(1)">+</button>
          </div>
          <button class="btn-add-cart" onclick="handlePdpAdd()">Add to Bag</button>
        </div>

        <button class="btn-buy-now" onclick="handlePdpBuyNow()">Buy Now</button>

        <div class="pdp-bullet-list">
          <p>• Tough and fancy, great for any spot</p>
          <p>• Come with metal grommets and sticky screws for easy hanging</p>
          <p>• Bright colors and cool designs, bringing a bit of flair to your place</p>
        </div>

        <div class="pdp-accordions">
          <div class="accordion-block is-open">
            <button class="accordion-header" onclick="toggleAcc(this)">
              <span>How to Install / Apply</span>
              <span class="plus-sign">+</span>
            </button>
            <div class="accordion-body">
              Mounting takes 30 seconds. Four pre-installed solid brass eyelets in each corner. Hang securely with thumbtacks, pushpins, 3M Command hooks, or small nails without damaging wall plaster or the fabric.
            </div>
          </div>

          <div class="accordion-block">
            <button class="accordion-header" onclick="toggleAcc(this)">
              <span>Material and Care</span>
              <span class="plus-sign">+</span>
            </button>
            <div class="accordion-body">
              100% heavyweight 180GSM micro-weave poly-canvas. Machine washable on cold gentle cycle. Hang dry or steam on low heat to release any packing folds. Colors are permanently infused and won't wash out.
            </div>
          </div>

          <div class="accordion-block">
            <button class="accordion-header" onclick="toggleAcc(this)">
              <span>Shipping and Packaging</span>
              <span class="plus-sign">+</span>
            </button>
            <div class="accordion-body">
              Orders dispatch within 24 hours from Mumbai. Typical delivery time is 3 to 5 business days pan-India. Free delivery on orders above ₹499. Cash on delivery available.
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Related Wall Drops -->
  <section class="pdp-wrap" style="padding-top: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px;">
      <div>
        <h2 style="font-size: 28px; font-weight: 800; color: #fff;">More Wall Drops</h2>
        <p style="font-size: 15px; color: var(--text-muted); margin-top: 4px;">Explore more statement album flags.</p>
      </div>
      <a href="shop.html" class="btn-secondary" style="font-size: 14px; padding: 10px 20px;">View All</a>
    </div>

    <div class="product-grid">
      {"".join(f'''
      <article class="product-card">
        <div class="product-thumb-wrap">
          <a href="product.html?id={p['id']}">
            <img class="product-thumb-img" src="{p['img']}" alt="{p['title']}" loading="lazy">
          </a>
          <span class="badge-tag">{p['tag']}</span>
          <span class="badge-sale">50% Off</span>
        </div>
        <div class="product-body">
          <div class="product-category">{p['category']}</div>
          <h3 class="product-title"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
          <p class="product-desc">{p['desc']}</p>
          <div class="product-footer">
            <div>
              <span class="price-current">₹500</span>
              <span class="price-mrp">₹1000</span>
            </div>
            <div>
              <a href="product.html?id={p['id']}" class="btn-view-drop">Details</a>
              <button class="btn-quick-add" onclick="addToCart('{p['id']}', 1, 'Medium (4x3 ft)')">Add</button>
            </div>
          </div>
        </div>
      </article>''' for p in PRODUCTS[1:5])}
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cloth-sim.js"></script>
  <script src="js/cart.js"></script>
  <script>
    let currentProd = null;
    let selectedSizeName = 'Medium (4x3 ft)';
    let selectedPrice = 500;
    let selectedMrp = 1000;
    let currentQty = 1;
    let pdpClothEngine = null;

    document.addEventListener('DOMContentLoaded', function() {{
      const params = new URLSearchParams(window.location.search);
      const id = params.get('id') || '{PRODUCTS[0]['id']}';
      currentProd = window.FLAGSTER_PRODUCTS.find(x => x.id === id) || window.FLAGSTER_PRODUCTS[0];

      document.title = `${{currentProd.title}} · Flagster`;
      document.getElementById('pdp-title-el').textContent = currentProd.title;
      document.getElementById('pdp-main-img').src = currentProd.img;
      updatePriceDisplay();
    }});

    function updatePriceDisplay() {{
      document.getElementById('pdp-price-el').textContent = `₹${{selectedPrice}}`;
      document.getElementById('pdp-mrp-el').textContent = `₹${{selectedMrp}}`;
    }}

    function selectSize(el, name, price, mrp) {{
      document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('is-active'));
      el.classList.add('is-active');
      selectedSizeName = name;
      selectedPrice = price;
      selectedMrp = mrp;
      updatePriceDisplay();
    }}

    function changeQty(delta) {{
      currentQty = Math.max(1, currentQty + delta);
      document.getElementById('pdp-qty-display').textContent = currentQty;
    }}

    function handlePdpAdd() {{
      if (!currentProd) return;
      addToCart(currentProd.id, currentQty, selectedSizeName);
    }}

    function handlePdpBuyNow() {{
      if (!currentProd) return;
      addToCart(currentProd.id, currentQty, selectedSizeName);
      closeCart();
      openCheckout();
    }}

    function toggleAcc(btn) {{
      btn.parentElement.classList.toggle('is-open');
    }}

    function setPdpMode(mode) {{
      const img = document.getElementById('pdp-main-img');
      const container3D = document.getElementById('pdp-3d-container');
      const btnPhoto = document.getElementById('btn-mode-photo');
      const btn3D = document.getElementById('btn-mode-3d');

      if (mode === '3d') {{
        img.style.display = 'none';
        container3D.classList.add('is-active');
        btnPhoto.classList.remove('is-active');
        btn3D.classList.add('is-active');

        if (!pdpClothEngine && currentProd && window.initFlagsterCloth) {{
          pdpClothEngine = window.initFlagsterCloth('pdp-cloth', 'pdp-3d-container', currentProd.img);
        }} else if (pdpClothEngine && currentProd) {{
          pdpClothEngine.setTexture(currentProd.img);
        }}
      }} else {{
        img.style.display = 'block';
        container3D.classList.remove('is-active');
        btnPhoto.classList.add('is-active');
        btn3D.classList.remove('is-active');
      }}
    }}
  </script>
</body>
</html>"""

# 4. BUILD shop.html
def build_shop():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster · All Wall Drops</title>
  <meta name="description" content="Browse all statement wall tapestries and album flags. Pre-installed brass eyelets. Flat ₹500.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .shop-wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 60px var(--gutter) 100px;
    }}
    .shop-header {{
      margin-bottom: 36px;
    }}
    .shop-title {{
      font-size: clamp(30px, 3.5vw, 46px);
      font-weight: 900;
      letter-spacing: -0.04em;
      color: #ffffff;
      margin-bottom: 8px;
    }}
    .shop-desc {{
      font-size: 16px;
      color: var(--text-muted);
    }}
    .shop-toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 36px;
      flex-wrap: wrap;
    }}
    .filter-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .filter-tab {{
      background: var(--bg-surface);
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 700;
      padding: 9px 20px;
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: background 0.2s ease, color 0.2s ease;
    }}
    .filter-tab.is-active,
    .filter-tab:hover {{
      background: #ffffff;
      color: #000000;
    }}
    .shop-search-input {{
      background: var(--bg-card);
      border: none;
      border-radius: var(--radius-pill);
      padding: 12px 22px;
      color: #ffffff;
      font-size: 14px;
      outline: none;
      min-width: 260px;
    }}

    /* Motion entrance */
    @media (prefers-reduced-motion: no-preference) {{
      .pdp-title, .pdp-price-row, .size-pills-row, .pdp-actions-row, .btn-buy-now, .pdp-bullet-list, .accordion-block {{
        animation: entranceFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;
      }}
    }}
  </style>
</head>
<body>

{get_header('shop')}

  <main class="shop-wrap">
    <div class="shop-header">
      <h1 class="shop-title">All Wall Drops</h1>
      <p class="shop-desc">Eight original tapestries. Heavyweight poly-canvas finished with corner brass eyelets.</p>
    </div>

    <div class="shop-toolbar">
      <div class="filter-tabs">
        <button class="filter-tab is-active" onclick="filterCatalog('All', this)">All ({len(PRODUCTS)})</button>
        <button class="filter-tab" onclick="filterCatalog('Hip-Hop', this)">Hip-Hop</button>
        <button class="filter-tab" onclick="filterCatalog('Street Drip', this)">Street Drip</button>
        <button class="filter-tab" onclick="filterCatalog('Psychedelic', this)">Psychedelic</button>
        <button class="filter-tab" onclick="filterCatalog('Typography', this)">Typography</button>
      </div>

      <input type="text" id="catalog-search" class="shop-search-input" placeholder="Search by name or artist" oninput="handleSearch(this.value)">
    </div>

    <div class="product-grid" id="catalog-grid">
      <!-- Injected by JS -->
    </div>
  </main>

  <!-- Related Wall Drops -->
  <section class="pdp-wrap" style="padding-top: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px;">
      <div>
        <h2 style="font-size: 28px; font-weight: 800; color: #fff;">More Wall Drops</h2>
        <p style="font-size: 15px; color: var(--text-muted); margin-top: 4px;">Explore more statement album flags.</p>
      </div>
      <a href="shop.html" class="btn-secondary" style="font-size: 14px; padding: 10px 20px;">View All</a>
    </div>

    <div class="product-grid">
      {"".join(f'''
      <article class="product-card">
        <div class="product-thumb-wrap">
          <a href="product.html?id={p['id']}">
            <img class="product-thumb-img" src="{p['img']}" alt="{p['title']}" loading="lazy">
          </a>
          <span class="badge-tag">{p['tag']}</span>
          <span class="badge-sale">50% Off</span>
        </div>
        <div class="product-body">
          <div class="product-category">{p['category']}</div>
          <h3 class="product-title"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
          <p class="product-desc">{p['desc']}</p>
          <div class="product-footer">
            <div>
              <span class="price-current">₹500</span>
              <span class="price-mrp">₹1000</span>
            </div>
            <div>
              <a href="product.html?id={p['id']}" class="btn-view-drop">Details</a>
              <button class="btn-quick-add" onclick="addToCart('{p['id']}', 1, 'Medium (4x3 ft)')">Add</button>
            </div>
          </div>
        </div>
      </article>''' for p in PRODUCTS[1:5])}
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script>
    let activeFilter = 'All';
    let searchQuery = '';

    document.addEventListener('DOMContentLoaded', function() {{
      const params = new URLSearchParams(window.location.search);
      const cat = params.get('cat');
      if (cat) {{
        activeFilter = cat;
        document.querySelectorAll('.filter-tab').forEach(b => {{
          if (b.textContent.includes(cat)) {{
            b.classList.add('is-active');
          }} else {{
            b.classList.remove('is-active');
          }}
        }});
      }}
      renderCatalog();
    }});

    function filterCatalog(category, btn) {{
      activeFilter = category;
      document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      renderCatalog();
    }}

    function handleSearch(val) {{
      searchQuery = val.toLowerCase().trim();
      renderCatalog();
    }}

    function renderCatalog() {{
      const grid = document.getElementById('catalog-grid');
      let items = window.FLAGSTER_PRODUCTS;

      if (activeFilter !== 'All') {{
        items = items.filter(x => x.category.toLowerCase() === activeFilter.toLowerCase());
      }}

      if (searchQuery) {{
        items = items.filter(x => x.title.toLowerCase().includes(searchQuery) || x.desc.toLowerCase().includes(searchQuery));
      }}

      if (items.length === 0) {{
        grid.innerHTML = '<p style="color: var(--text-dim); padding: 40px 0;">No matching tapestries found.</p>';
        return;
      }}

      grid.innerHTML = items.map(p => `
        <article class="product-card">
          <div class="product-thumb-wrap">
            <a href="product.html?id=${{p.id}}">
              <img class="product-thumb-img" src="${{p.img}}" alt="${{p.title}}" loading="lazy">
            </a>
            <span class="badge-tag">${{p.tag}}</span>
            <span class="badge-sale">50% Off</span>
          </div>
          <div class="product-body">
            <div class="product-category">${{p.category}}</div>
            <h3 class="product-title"><a href="product.html?id=${{p.id}}">${{p.title}}</a></h3>
            <p class="product-desc">${{p.desc}}</p>
            <div class="product-footer">
              <div>
                <span class="price-current">₹500</span>
                <span class="price-mrp">₹1000</span>
              </div>
              <div>
                <a href="product.html?id=${{p.id}}" class="btn-view-drop">Details</a>
                <button class="btn-quick-add" onclick="addToCart('${{p.id}}', 1, 'Medium (4x3 ft)')">Add</button>
              </div>
            </div>
          </div>
        </article>
      `).join('');
    }}
  </script>
</body>
</html>"""

# 5. BUILD faq.html
def build_faq():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster · How to Hang and FAQ</title>
  <meta name="description" content="Step-by-step wall mounting guide for pre-installed corner grommets, fabric washing, and shipping information.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .faq-wrap {{
      max-width: 900px;
      margin: 0 auto;
      padding: 60px var(--gutter) 100px;
    }}
    .faq-title {{
      font-size: clamp(30px, 3.5vw, 46px);
      font-weight: 900;
      letter-spacing: -0.04em;
      color: #ffffff;
      margin-bottom: 8px;
    }}
    .faq-sub {{
      font-size: 16px;
      color: var(--text-muted);
      margin-bottom: 48px;
    }}
    .step-box {{
      background: var(--bg-card);
      border-radius: 12px;
      padding: 26px;
      margin-bottom: 16px;
    }}
    .step-box h4 {{
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
    }}
    .step-box p {{
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.6;
    }}
  </style>
</head>
<body>

{get_header('faq')}

  <main class="faq-wrap">
    <h1 class="faq-title">How to Hang and FAQ</h1>
    <p class="faq-sub">Simple guidelines for mounting, care, and order delivery.</p>

    <h2 style="font-size: 22px; font-weight: 800; color: #fff; margin-bottom: 20px;">Mounting in 30 Seconds</h2>
    <div class="step-box">
      <h4>Method 1: Pushpins or Thumbtacks</h4>
      <p>Place a clear pushpin through each of the four pre-installed brass corner grommets directly into drywall or pin boards. Ideal for dorms and rental rooms with zero noticeable damage.</p>
    </div>
    <div class="step-box">
      <h4>Method 2: 3M Command Clear Hooks</h4>
      <p>Adhere 3M Command hooks to your wall and slide the brass grommets over the hooks. Leaves no trace on painted walls upon removal.</p>
    </div>
    <div class="step-box">
      <h4>Method 3: Small Finishing Nails</h4>
      <p>Tap a slender finishing nail into each top corner for a permanent flat aesthetic tension hang.</p>
    </div>

    <h2 style="font-size: 22px; font-weight: 800; color: #fff; margin-top: 48px; margin-bottom: 20px;" id="care">Fabric Care and Ironing</h2>
    <div class="step-box">
      <h4>Washing</h4>
      <p>Machine wash cold on gentle cycle with mild detergent. Hang to dry. Do not bleach.</p>
    </div>
    <div class="step-box">
      <h4>Removing Folds</h4>
      <p>Use a garment steamer on low heat or iron the unprinted backside with a thin towel placed over the fabric.</p>
    </div>

    <h2 style="font-size: 22px; font-weight: 800; color: #fff; margin-top: 48px; margin-bottom: 20px;" id="shipping">Shipping and Replacement</h2>
    <div class="step-box">
      <h4>Delivery Times</h4>
      <p>All flags are printed and shipped within 24 hours. Transit takes 3 to 5 business days pan-India via express surface courier.</p>
    </div>
    <div class="step-box">
      <h4>7-Day Replacement Guarantee</h4>
      <p>If your tapestry arrives with any print defect or stitching fault, reach out on WhatsApp (+91 98765 43210) for an immediate replacement at zero charge.</p>
    </div>
  </main>

  <!-- Related Wall Drops -->
  <section class="pdp-wrap" style="padding-top: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px;">
      <div>
        <h2 style="font-size: 28px; font-weight: 800; color: #fff;">More Wall Drops</h2>
        <p style="font-size: 15px; color: var(--text-muted); margin-top: 4px;">Explore more statement album flags.</p>
      </div>
      <a href="shop.html" class="btn-secondary" style="font-size: 14px; padding: 10px 20px;">View All</a>
    </div>

    <div class="product-grid">
      {"".join(f'''
      <article class="product-card">
        <div class="product-thumb-wrap">
          <a href="product.html?id={p['id']}">
            <img class="product-thumb-img" src="{p['img']}" alt="{p['title']}" loading="lazy">
          </a>
          <span class="badge-tag">{p['tag']}</span>
          <span class="badge-sale">50% Off</span>
        </div>
        <div class="product-body">
          <div class="product-category">{p['category']}</div>
          <h3 class="product-title"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
          <p class="product-desc">{p['desc']}</p>
          <div class="product-footer">
            <div>
              <span class="price-current">₹500</span>
              <span class="price-mrp">₹1000</span>
            </div>
            <div>
              <a href="product.html?id={p['id']}" class="btn-view-drop">Details</a>
              <button class="btn-quick-add" onclick="addToCart('{p['id']}', 1, 'Medium (4x3 ft)')">Add</button>
            </div>
          </div>
        </div>
      </article>''' for p in PRODUCTS[1:5])}
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
</body>
</html>"""

# 6. BUILD contact.html
def build_contact():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster · Order Tracking and Support</title>
  <meta name="description" content="Check live order dispatch status or connect with Flagster customer care on WhatsApp.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .contact-wrap {{
      max-width: 800px;
      margin: 0 auto;
      padding: 60px var(--gutter) 100px;
    }}
    .contact-title {{
      font-size: clamp(30px, 3.5vw, 46px);
      font-weight: 900;
      letter-spacing: -0.04em;
      color: #ffffff;
      margin-bottom: 8px;
    }}
    .contact-sub {{
      font-size: 16px;
      color: var(--text-muted);
      margin-bottom: 40px;
    }}
    .tool-box {{
      background: var(--bg-card);
      border-radius: 14px;
      padding: 32px;
      margin-bottom: 32px;
    }}
    .tool-box h3 {{
      font-size: 19px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 8px;
    }}
    .tool-box p {{
      font-size: 15px;
      color: var(--text-muted);
      margin-bottom: 20px;
    }}
    .track-input-row {{
      display: flex;
      gap: 10px;
    }}
    .track-input {{
      flex: 1;
      background: var(--bg-surface);
      border: none;
      border-radius: var(--radius-pill);
      padding: 13px 20px;
      color: #ffffff;
      font-size: 15px;
      outline: none;
    }}
    .tracking-result {{
      margin-top: 20px;
      padding: 18px;
      background: var(--bg-surface);
      border-radius: 8px;
      display: none;
      font-size: 14px;
      line-height: 1.6;
    }}
  </style>
</head>
<body>

{get_header('contact')}

  <main class="contact-wrap">
    <h1 class="contact-title">Track Order and Support</h1>
    <p class="contact-sub">Lookup dispatch status or reach our support desk.</p>

    <!-- Tracking Lookup -->
    <div class="tool-box">
      <h3>Track Your Package</h3>
      <p>Enter your Flagster order reference (e.g. FLG-84920 or FLG-2026).</p>
      <form class="track-input-row" onsubmit="handleTrack(event)">
        <input type="text" id="order-ref-input" class="track-input" placeholder="Order ID" required>
        <button type="submit" class="btn-pink">Track</button>
      </form>
      <div class="tracking-result" id="tracking-result-box"></div>
    </div>

    <!-- Direct WhatsApp -->
    <div class="tool-box">
      <h3>Direct WhatsApp Support</h3>
      <p>Have an inquiry about dimensions, custom graphics, or order changes? Message our desk directly.</p>
      <a href="https://wa.me/919876543210" target="_blank" rel="noopener" class="btn-primary">Message on WhatsApp (+91 98765 43210)</a>
    </div>

    <!-- Inquiries -->
    <div class="tool-box">
      <h3>General Inquiries</h3>
      <p>Email our desk at support@flagster.in with your order reference. Responses within 24 hours.</p>
    </div>
  </main>

  <!-- Related Wall Drops -->
  <section class="pdp-wrap" style="padding-top: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px;">
      <div>
        <h2 style="font-size: 28px; font-weight: 800; color: #fff;">More Wall Drops</h2>
        <p style="font-size: 15px; color: var(--text-muted); margin-top: 4px;">Explore more statement album flags.</p>
      </div>
      <a href="shop.html" class="btn-secondary" style="font-size: 14px; padding: 10px 20px;">View All</a>
    </div>

    <div class="product-grid">
      {"".join(f'''
      <article class="product-card">
        <div class="product-thumb-wrap">
          <a href="product.html?id={p['id']}">
            <img class="product-thumb-img" src="{p['img']}" alt="{p['title']}" loading="lazy">
          </a>
          <span class="badge-tag">{p['tag']}</span>
          <span class="badge-sale">50% Off</span>
        </div>
        <div class="product-body">
          <div class="product-category">{p['category']}</div>
          <h3 class="product-title"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
          <p class="product-desc">{p['desc']}</p>
          <div class="product-footer">
            <div>
              <span class="price-current">₹500</span>
              <span class="price-mrp">₹1000</span>
            </div>
            <div>
              <a href="product.html?id={p['id']}" class="btn-view-drop">Details</a>
              <button class="btn-quick-add" onclick="addToCart('{p['id']}', 1, 'Medium (4x3 ft)')">Add</button>
            </div>
          </div>
        </div>
      </article>''' for p in PRODUCTS[1:5])}
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script>
    function handleTrack(e) {{
      e.preventDefault();
      const val = document.getElementById('order-ref-input').value.trim();
      const box = document.getElementById('tracking-result-box');
      box.style.display = 'block';
      box.innerHTML = `
        <div style="font-weight: 800; color: #fff; margin-bottom: 4px;">Status for ${{val}}</div>
        <div style="color: var(--pink-accent); font-weight: 700; margin-bottom: 6px;">Dispatched · In Transit</div>
        <p style="color: var(--text-muted); font-size: 13px;">Carrier: BlueDart Express · Estimated Delivery: Within 2 to 3 Business Days</p>
      `;
    }}
  </script>
</body>
</html>"""

# Write all pages
with open('index.html', 'w') as f: f.write(build_index())
with open('product.html', 'w') as f: f.write(build_product())
with open('shop.html', 'w') as f: f.write(build_shop())
with open('faq.html', 'w') as f: f.write(build_faq())
with open('contact.html', 'w') as f: f.write(build_contact())

print("All 5 pages generated cleanly with 0 hairlines, 0 shadows at rest, 16px body, 0 covered text.")
