import json, os

with open('/home/maahir/.gemini/antigravity/scratch/peculiar-atelier/js/products.js', 'r') as f:
    raw = f.read()
    json_str = raw.replace('window.FLAGSTER_PRODUCTS = ', '').rstrip(';\n')
    products = json.loads(json_str)

def get_header(active_page="home"):
    return f"""
  <!-- Announcement Top Banner -->
  <aside class="announcement">
    <span>Free Shipping For Order Above ₹499 and Use Code: "<strong>FLAGSTER10</strong>" For 10% off</span>
  </aside>

  <!-- Sticky Navbar -->
  <header class="nav-bar">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        <span>FLAGSTER</span>
        <span class="nav-logo-tag">ORIGINALS</span>
      </a>

      <nav class="nav-links">
        <a href="index.html" class="{'is-active' if active_page == 'home' else ''}">Home</a>
        <a href="shop.html" class="{'is-active' if active_page == 'shop' else ''}">Shop All ({len(products)})</a>
        <a href="index.html#studio" class="{'is-active' if active_page == 'studio' else ''}">3D Cloth Studio</a>
        <a href="faq.html" class="{'is-active' if active_page == 'faq' else ''}">How to Hang & FAQ</a>
        <a href="contact.html" class="{'is-active' if active_page == 'contact' else ''}">Contact & Track</a>
      </nav>

      <div class="nav-actions">
        <button class="nav-cart-btn" id="open-cart-btn" aria-label="Open Cart">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          <span>Cart</span>
          <span class="cart-pill-count" id="nav-cart-badge">0</span>
        </button>
      </div>
    </div>
  </header>
"""

def get_footer():
    return """
  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-top">
      <div class="footer-col">
        <div class="nav-logo" style="margin-bottom: 16px;">
          <span>FLAGSTER</span>
          <span class="nav-logo-tag">ORIGINALS</span>
        </div>
        <p>Premium statement wall tapestries inspired by hip-hop, street drip, and indie album art. 4 corner brass grommets, heavy micro-weave canvas, and fade-resistant thermal print. Fixed at ₹500.</p>
        <p style="color: #6a7182; font-size: 13px;">Free shipping across India on 2+ flags.</p>
      </div>

      <div class="footer-col">
        <h4>Navigation</h4>
        <ul class="footer-links">
          <li><a href="index.html">Home</a></li>
          <li><a href="shop.html">Shop All Tapestries</a></li>
          <li><a href="index.html#studio">3D Interactive Studio</a></li>
          <li><a href="faq.html">How to Hang Guide</a></li>
          <li><a href="contact.html">Track My Order</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Customer Care</h4>
        <ul class="footer-links">
          <li><a href="faq.html#shipping">Shipping & Delivery</a></li>
          <li><a href="faq.html#returns">7-Day Replacement</a></li>
          <li><a href="faq.html#care">Washing & Care</a></li>
          <li><a href="contact.html">WhatsApp Support</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>VIP Drop List</h4>
        <p>Subscribe for secret midnight drops and an instant 10% coupon.</p>
        <form class="newsletter-form" onsubmit="event.preventDefault(); alert('Welcome to Flagster VIP! Use code FLAGSTER10 at checkout.');">
          <input type="email" class="newsletter-input" placeholder="Your email..." required>
          <button type="submit" class="newsletter-btn">Join</button>
        </form>
      </div>
    </div>

    <div class="footer-bottom">
      <span>© 2026 FLAGSTER INC. All rights reserved.</span>
      <span>Flat ₹500 (50% Off MRP ₹1,000) • Cash on Delivery & Fast UPI Available</span>
    </div>
  </footer>

  <!-- Slide-In Cart Drawer -->
  <div class="cart-backdrop" id="cart-backdrop">
    <aside class="cart-drawer" role="dialog" aria-label="Shopping Cart">
      <div class="cart-header">
        <h3>Your Cart (<span id="cart-drawer-count">0</span>)</h3>
        <button class="cart-close-btn" id="cart-close-btn" aria-label="Close Cart">&times;</button>
      </div>

      <div class="cart-shipping-banner" id="cart-shipping-msg">
        ⚡ Add 1 more flag to unlock FREE SHIPPING!
      </div>

      <div class="cart-items" id="cart-items-container">
        <!-- Injected via cart.js -->
      </div>

      <div class="cart-footer">
        <div class="cart-coupon-row">
          <input type="text" class="cart-coupon-input" id="coupon-input" placeholder="Coupon Code (e.g. FLAGSTER10)">
          <button class="cart-coupon-btn" onclick="applyCoupon()">Apply</button>
        </div>
        <div class="cart-subtotal">
          <span>Subtotal</span>
          <span id="cart-subtotal-val">₹0</span>
        </div>
        <div class="cart-subtotal" style="color: var(--green);">
          <span>50% Drop Discount</span>
          <span id="cart-discount-val">-₹0</span>
        </div>
        <div class="cart-subtotal">
          <span>Shipping</span>
          <span id="cart-shipping-val">₹50</span>
        </div>
        <div class="cart-total">
          <span>Total</span>
          <span id="cart-total-val">₹0</span>
        </div>
        <button class="cart-checkout-btn" id="cart-checkout-btn">
          <span>Proceed to Checkout</span>
          <span>→</span>
        </button>
      </div>
    </aside>
  </div>

  <!-- Checkout Modal -->
  <div class="modal-backdrop" id="checkout-modal">
    <div class="modal-box">
      <button class="modal-close-btn" id="modal-close-btn">&times;</button>

      <div id="checkout-form-view">
        <h3 class="modal-title">Fast Checkout</h3>
        <p class="modal-sub">Fast dispatch within 24h with brass grommet mounting kit.</p>

        <form id="order-form" onsubmit="handlePlaceOrder(event)">
          <div class="form-group">
            <label>Full Name</label>
            <input type="text" class="form-input" placeholder="e.g. Aryan Sharma" required>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Phone Number (for delivery SMS)</label>
              <input type="tel" class="form-input" placeholder="+91 98765 43210" required>
            </div>
            <div class="form-group">
              <label>PIN Code</label>
              <input type="text" class="form-input" placeholder="e.g. 560001" required>
            </div>
          </div>

          <div class="form-group">
            <label>Delivery Address</label>
            <input type="text" class="form-input" placeholder="Flat, Building, Street name" required>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>City</label>
              <input type="text" class="form-input" placeholder="e.g. Bengaluru" required>
            </div>
            <div class="form-group">
              <label>State</label>
              <input type="text" class="form-input" placeholder="e.g. Karnataka" required>
            </div>
          </div>

          <div class="form-group">
            <label>Payment Method</label>
            <div class="payment-options">
              <div class="payment-option is-selected" onclick="selectPayment(this, 'cod')">
                <div style="font-size: 20px;">💵</div>
                <div class="payment-option-title">Cash on Delivery</div>
              </div>
              <div class="payment-option" onclick="selectPayment(this, 'upi')">
                <div style="font-size: 20px;">📱</div>
                <div class="payment-option-title">UPI / GPay</div>
              </div>
              <div class="payment-option" onclick="selectPayment(this, 'card')">
                <div style="font-size: 20px;">💳</div>
                <div class="payment-option-title">Card / NetBanking</div>
              </div>
            </div>
          </div>

          <div class="order-summary-box">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
              <span>Total Items</span>
              <strong id="modal-item-count">1 item</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 16px;">
              <span>Final Payable</span>
              <strong style="color: #fff;" id="modal-final-total">₹500</strong>
            </div>
          </div>

          <button type="submit" class="cart-checkout-btn" style="background: var(--accent); color: #fff;">
            <span>Confirm Order</span>
            <span>✓</span>
          </button>
        </form>
      </div>

      <div class="success-view" id="checkout-success-view">
        <div class="success-icon">✓</div>
        <h3 class="modal-title">Order Confirmed!</h3>
        <p class="modal-sub">Thank you for ordering with Flagster! We are preparing your tapestries.</p>
        <div style="background: var(--bg-surface); padding: 18px; border-radius: 12px; margin: 20px 0; font-size: 14px; text-align: left;">
          <p><strong>Order ID:</strong> #FLG-<span id="confirmed-order-id">82914</span></p>
          <p style="margin-top: 6px;"><strong>Delivery Estimate:</strong> 3-4 Business Days</p>
          <p style="margin-top: 6px; color: var(--green);"><strong>Status:</strong> Ready for Dispatch</p>
        </div>
        <button class="btn btn-primary" style="width: 100%;" onclick="closeCheckout()">
          Continue Browsing
        </button>
      </div>
    </div>
  </div>
"""

# ==========================================
# 1. BUILD index.html (HOME PAGE)
# ==========================================
def build_index_html():
    first_p = products[0]
    
    flag_thumbs_html = ""
    for p in products:
        active = 'is-active' if p['id'] == first_p['id'] else ''
        flag_thumbs_html += f"""
          <button class="flag-thumb-btn {active}" data-id="{p['id']}" title="{p['title']}" aria-label="View {p['title']} in 3D">
            <img src="{p['img']}" alt="{p['title']}" loading="lazy">
          </button>
        """

    grid_cards_html = ""
    for p in products:
        grid_cards_html += f"""
        <article class="product-card" data-category="{p['category']}">
          <div class="product-media">
            <a href="product.html?id={p['id']}">
              <img src="{p['img']}" alt="{p['title']}" loading="lazy">
            </a>
            <span class="product-tag-badge">{p['tag']}</span>
            <span class="product-discount-badge">50% OFF</span>
          </div>
          <div class="product-body">
            <span class="product-cat">{p['category']}</span>
            <h3 class="product-name"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
            <div class="product-rating">
              <span>★ ★ ★ ★ ★</span>
              <span>{p['rating']} ({p['reviewsCount']} reviews)</span>
            </div>
            <p class="product-desc">{p['desc']}</p>
            <div class="product-footer">
              <div class="card-price">
                <span class="card-price-sale">₹{p['price']}</span>
                <span class="card-price-mrp">₹{p['mrp']}</span>
              </div>
              <div class="card-actions">
                <button class="card-btn-view" onclick="loadProductInHero('{p['id']}')" title="Test in 3D Studio">
                  <span>3D View</span>
                </button>
                <button class="card-btn-cart" onclick="addToCart('{p['id']}')">
                  <span>+ Add</span>
                </button>
              </div>
            </div>
          </div>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FLAGSTER — Statement Wall Tapestries & Flags | Under ₹1000</title>
  <meta name="description" content="Flagster: Street-culture, hip-hop, and indie wall flags with 4 brass grommets. All drops ₹500 (50% OFF). Real-time 3D interactive preview.">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    /* Hero Section */
    .hero {{
      position: relative;
      height: calc(100vh - 105px);
      min-height: 600px;
      max-height: 900px;
      overflow: hidden;
      isolation: isolate;
      background: radial-gradient(120% 95% at 58% 38%, #e8e9ed 0%, var(--paper) 46%, var(--paper-edge) 100%);
      border-bottom: 1px solid var(--border);
    }}
    .hero__cloth {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
      touch-action: pan-y;
      outline: none;
    }}
    .hero__cloth.is-over {{ cursor: grab; }}
    .hero__cloth.is-held {{ cursor: grabbing; }}
    .hero__still {{
      position: absolute;
      left: 40%;
      top: 48.5%;
      width: min(64vw, 84vh);
      aspect-ratio: 1.38/1;
      object-fit: cover;
      transform: translate(-50%, -50%) rotate(4deg);
      box-shadow: -18px 40px 70px rgba(20,20,40,0.22);
      display: none;
      z-index: 1;
    }}
    .hero.no-cloth .hero__still {{ display: block; }}
    .hero.no-cloth .hero__cloth {{ display: none; }}

    .hero-overlay {{
      position: absolute;
      inset: 0;
      z-index: 5;
      pointer-events: none;
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px var(--gutter) 32px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .hero-hint {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #ffffff;
      width: fit-content;
      pointer-events: auto;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      background: var(--green);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--green);
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.3); opacity: 0.6; }}
    }}

    .hero-content-box {{
      position: absolute;
      right: var(--gutter);
      top: 50%;
      transform: translateY(-50%);
      width: min(520px, 44vw);
      pointer-events: auto;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      padding: 32px 36px;
      border-radius: 20px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.14);
      color: var(--ink);
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #ffe5e7;
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    .hero-title {{
      font-size: clamp(26px, 3vw, 38px);
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -0.04em;
      margin-bottom: 10px;
      color: #0b0c10;
    }}
    .hero-desc {{
      font-size: 14px;
      color: #555b6d;
      margin-bottom: 18px;
      line-height: 1.45;
    }}
    .hero-price-row {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 18px;
    }}
    .price-sale {{ font-size: 32px; font-weight: 900; color: #000; letter-spacing: -0.04em; }}
    .price-mrp {{ font-size: 17px; font-weight: 500; color: #8c93a4; text-decoration: line-through; }}
    .price-discount-tag {{ background: #000; color: #fff; font-size: 12px; font-weight: 800; padding: 3px 8px; border-radius: 6px; }}

    .hero-flag-picker {{ margin-bottom: 20px; }}
    .picker-label {{ font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280; margin-bottom: 8px; display: block; }}
    .flag-thumbs {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }}
    .flag-thumb-btn {{
      position: relative;
      aspect-ratio: 1.38/1;
      border-radius: 6px;
      overflow: hidden;
      border: 2px solid transparent;
      padding: 0;
      background: #222;
      transition: all 0.2s ease;
      cursor: pointer;
    }}
    .flag-thumb-btn img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .flag-thumb-btn:hover {{ transform: translateY(-2px); border-color: #000; }}
    .flag-thumb-btn.is-active {{ border-color: #000; box-shadow: 0 0 0 2px #fff, 0 4px 12px rgba(0,0,0,0.3); }}

    .hero-cta-group {{ display: flex; gap: 10px; }}
    .hero-cta-group .btn {{ flex: 1; }}
    .hero-perks {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px solid rgba(0,0,0,0.08);
      font-size: 12px;
      font-weight: 600;
      color: #636a7c;
      flex-wrap: wrap;
    }}

    /* Features Strip */
    .features-strip {{
      background: var(--bg-card);
      border-bottom: 1px solid var(--border);
      padding: 32px var(--gutter);
    }}
    .features-grid {{
      max-width: 1440px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }}
    .feature-item {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }}
    .feature-icon {{
      width: 42px;
      height: 42px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
    }}
    .feature-text h4 {{ font-size: 15px; font-weight: 700; margin-bottom: 2px; color: #fff; }}
    .feature-text p {{ font-size: 13px; color: var(--text-muted); line-height: 1.4; }}

    .filter-pills {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .filter-btn {{
      padding: 8px 18px;
      border-radius: var(--radius-pill);
      font-size: 13px;
      font-weight: 600;
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      transition: all 0.2s;
    }}
    .filter-btn:hover {{ color: #fff; border-color: var(--border-strong); }}
    .filter-btn.is-active {{ background: #fff; color: #000; border-color: #fff; }}

    @media (max-width: 1099px) {{
      .hero {{ height: auto; min-height: 700px; }}
      .hero-content-box {{ position: static; transform: none; width: 100%; margin-top: auto; }}
      .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 640px) {{
      .features-grid {{ grid-template-columns: 1fr; }}
      .flag-thumbs {{ grid-template-columns: repeat(4, 1fr); }}
    }}
  </style>
</head>
<body>
{get_header("home")}

  <!-- 3D Interactive Hero -->
  <section class="hero" id="studio" aria-label="Flagster 3D Studio">
    <canvas class="hero__cloth" id="cloth" role="img" tabindex="-1" aria-label="Interactive 3D hanging tapestry flag with physics simulation. Grab and drag with mouse or finger to tug."></canvas>
    <img class="hero__still" id="still" alt="Tapestry Flag" decoding="async" src="{first_p['img']}">

    <div class="hero-overlay">
      <div class="hero-hint">
        <span class="pulse-dot"></span>
        <span>Interactive 3D Preview — Drag & Tug The Tapestry</span>
      </div>

      <div class="hero-content-box">
        <div class="hero-badge">⚡ 50% OFF TODAY • UNDER ₹1000</div>
        <h1 class="hero-title" id="hero-flag-title">{first_p['title']}</h1>
        <p class="hero-desc" id="hero-flag-desc">{first_p['desc']}</p>

        <!-- Flag Selector -->
        <div class="hero-flag-picker">
          <span class="picker-label">Switch Live 3D Tapestry:</span>
          <div class="flag-thumbs">
            {flag_thumbs_html}
          </div>
        </div>

        <div class="hero-price-row">
          <span class="price-sale">₹{first_p['price']}</span>
          <span class="price-mrp">₹{first_p['mrp']}</span>
          <span class="price-discount-tag">50% OFF</span>
        </div>

        <div class="hero-cta-group">
          <button class="btn btn-primary" id="hero-add-cart-btn" onclick="addToCart(currentHeroProductId)">
            <span>Add to Cart • ₹500</span>
          </button>
          <button class="btn btn-secondary" onclick="buyNowHero()">
            <span>Buy Now</span>
          </button>
        </div>

        <div class="hero-perks">
          <span>🔩 4 Brass Grommets</span>
          <span>🧵 Fade-Proof Canvas</span>
          <span>🚚 Ships in 24h</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Strip -->
  <section class="features-strip">
    <div class="features-grid">
      <div class="feature-item">
        <div class="feature-icon">🔩</div>
        <div class="feature-text">
          <h4>Pre-Installed Grommets</h4>
          <p>4 solid brass corner eyelets. Mount with pushpins or hooks in 30 seconds.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">🧵</div>
        <div class="feature-text">
          <h4>180GSM Micro-Weave</h4>
          <p>Thick polyester canvas. No wrinkles, no see-through, zero fraying.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">🎨</div>
        <div class="feature-text">
          <h4>HD Thermal Dye</h4>
          <p>Sublimation color infusion with deep blacks that never wash out.</p>
        </div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">💸</div>
        <div class="feature-text">
          <h4>₹500 Flat Rate (50% Off)</h4>
          <p>Premium aesthetics under ₹1,000. Free delivery on 2+ flags.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Trending Drops Section -->
  <section class="section" id="shop">
    <div class="section-header">
      <div>
        <span class="section-tag">2026 Collection</span>
        <h2 class="section-title">TRENDING WALL DROPS</h2>
        <p class="section-sub">Statement album & aesthetic tapestries for bedroom, dorm, or studio. All drops ₹500 each.</p>
      </div>

      <div class="filter-pills">
        <button class="filter-btn is-active" data-filter="all">All Flags ({len(products)})</button>
        <button class="filter-btn" data-filter="Hip-Hop">Hip-Hop</button>
        <button class="filter-btn" data-filter="Street Drip">Street Drip</button>
        <button class="filter-btn" data-filter="Psychedelic">Psychedelic</button>
        <button class="filter-btn" data-filter="Typography">Typography</button>
      </div>
    </div>

    <div class="products-grid">
      {grid_cards_html}
    </div>
  </section>

  <!-- Reviews -->
  <section class="section" id="reviews" style="background: var(--bg-card); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); max-width: 100%;">
    <div style="max-width: 1440px; margin: 0 auto;">
      <div class="section-header">
        <div>
          <span class="section-tag">Social Proof</span>
          <h2 class="section-title">LOVED BY 1,200+ ROOMS</h2>
          <p class="section-sub">Real customer photos and reviews across India.</p>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
        <div style="background: var(--bg-surface); padding: 24px; border-radius: 14px; border: 1px solid var(--border);">
          <div style="color: #e2b93b; margin-bottom: 10px;">★ ★ ★ ★ ★</div>
          <p style="font-size: 14px; color: #d1d5db; line-height: 1.6; margin-bottom: 16px;">"Got the Music Is My Drug and Currents flags. The print quality is insane for ₹500, deep blacks and the brass grommets made hanging it take 30 seconds."</p>
          <div style="font-weight: 700; font-size: 13px;">Aman K. <span style="color: var(--green); font-size: 11px;">✓ Verified Buyer • Bengaluru</span></div>
        </div>

        <div style="background: var(--bg-surface); padding: 24px; border-radius: 14px; border: 1px solid var(--border);">
          <div style="color: #e2b93b; margin-bottom: 10px;">★ ★ ★ ★ ★</div>
          <p style="font-size: 14px; color: #d1d5db; line-height: 1.6; margin-bottom: 16px;">"The DAMN and PartyNextDoor tapestries look unreal under my red LED lights. Heavy material, not that cheap shiny flag nylon. 10/10."</p>
          <div style="font-weight: 700; font-size: 13px;">Rohan P. <span style="color: var(--green); font-size: 11px;">✓ Verified Buyer • Mumbai</span></div>
        </div>

        <div style="background: var(--bg-surface); padding: 24px; border-radius: 14px; border: 1px solid var(--border);">
          <div style="color: #e2b93b; margin-bottom: 10px;">★ ★ ★ ★ ★</div>
          <p style="font-size: 14px; color: #d1d5db; line-height: 1.6; margin-bottom: 16px;">"The interactive 3D cloth simulator on the website is so cool, you can test how the flag hangs before ordering. Arrived in 3 days via COD!"</p>
          <div style="font-weight: 700; font-size: 13px;">Tanvi D. <span style="color: var(--green); font-size: 11px;">✓ Verified Buyer • Delhi</span></div>
        </div>
      </div>
    </div>
  </section>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cloth-sim.js"></script>
  <script src="js/cart.js"></script>
  <script>
    let clothEngine = null;
    let currentHeroProductId = '{first_p['id']}';

    document.addEventListener('DOMContentLoaded', function() {{
      clothEngine = window.initFlagsterCloth('cloth', 'studio', '{first_p['img']}');

      // Hook up hero thumbs
      document.querySelectorAll('.flag-thumb-btn').forEach(btn => {{
        btn.addEventListener('click', function() {{
          const id = this.dataset.id;
          loadProductInHero(id);
        }});
      }});

      // Hook up filter buttons
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', function() {{
          document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('is-active'));
          this.classList.add('is-active');
          const filter = this.dataset.filter;
          document.querySelectorAll('.product-card').forEach(card => {{
            if (filter === 'all' || card.dataset.category === filter) {{
              card.style.display = 'flex';
            }} else {{
              card.style.display = 'none';
            }}
          }});
        }});
      }});
    }});

    function loadProductInHero(id) {{
      const p = window.FLAGSTER_PRODUCTS.find(x => x.id === id);
      if (!p) return;
      currentHeroProductId = p.id;

      if (clothEngine) {{
        clothEngine.setTexture(p.img);
      }}

      const titleEl = document.getElementById('hero-flag-title');
      const descEl = document.getElementById('hero-flag-desc');
      if (titleEl) titleEl.textContent = p.title;
      if (descEl) descEl.textContent = p.desc;

      document.querySelectorAll('.flag-thumb-btn').forEach(btn => {{
        btn.classList.toggle('is-active', btn.dataset.id === p.id);
      }});

      // Scroll smoothly to studio if triggered from card
      const studio = document.getElementById('studio');
      if (studio && window.scrollY > 400) {{
        studio.scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}

    function buyNowHero() {{
      addToCart(currentHeroProductId);
      closeCart();
      openCheckout();
    }}
  </script>
</body>
</html>
"""

# ==========================================
# 2. BUILD shop.html (CATALOG PAGE)
# ==========================================
def build_shop_html():
    cards_html = ""
    for p in products:
        cards_html += f"""
        <article class="product-card" data-category="{p['category']}" data-price="{p['price']}" data-title="{p['title'].lower()}">
          <div class="product-media">
            <a href="product.html?id={p['id']}">
              <img src="{p['img']}" alt="{p['title']}" loading="lazy">
            </a>
            <span class="product-tag-badge">{p['tag']}</span>
            <span class="product-discount-badge">50% OFF</span>
          </div>
          <div class="product-body">
            <span class="product-cat">{p['category']}</span>
            <h3 class="product-name"><a href="product.html?id={p['id']}">{p['title']}</a></h3>
            <div class="product-rating">
              <span>★ ★ ★ ★ ★</span>
              <span>{p['rating']} ({p['reviewsCount']} reviews)</span>
            </div>
            <p class="product-desc">{p['desc']}</p>
            <div class="product-footer">
              <div class="card-price">
                <span class="card-price-sale">₹{p['price']}</span>
                <span class="card-price-mrp">₹{p['mrp']}</span>
              </div>
              <div class="card-actions">
                <a href="product.html?id={p['id']}" class="card-btn-view">
                  <span>View Details</span>
                </a>
                <button class="card-btn-cart" onclick="addToCart('{p['id']}')">
                  <span>+ Add</span>
                </button>
              </div>
            </div>
          </div>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shop All Tapestries — Flagster Drops Under ₹1000</title>
  <meta name="description" content="Explore Flagster's full catalog of statement hip-hop, street, and indie wall tapestries. Fixed 50% discount at ₹500. Free shipping above ₹999.">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .shop-header {{
      padding: 60px var(--gutter) 30px;
      max-width: 1440px;
      margin: 0 auto;
    }}
    .shop-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 28px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }}
    .search-box {{
      position: relative;
      width: min(340px, 100%);
    }}
    .search-input {{
      width: 100%;
      height: 42px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-pill);
      padding: 0 16px 0 40px;
      color: #fff;
      font-size: 14px;
      outline: none;
    }}
    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
    }}
    .sort-select {{
      height: 42px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-pill);
      padding: 0 18px;
      color: #fff;
      font-size: 13px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }}
  </style>
</head>
<body>
{get_header("shop")}

  <div class="shop-header">
    <span class="section-tag">Full Drop Catalog</span>
    <h1 class="section-title">ALL WALL TAPESTRIES</h1>
    <p class="section-sub">Browse all {len(products)} statement flags. Premium woven canvas with 4 brass eyelets. All drops flat 50% off at ₹500.</p>

    <div class="shop-controls">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" id="search-input" placeholder="Search by artist, album, theme...">
      </div>

      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <div class="filter-pills">
          <button class="filter-btn is-active" data-filter="all">All ({len(products)})</button>
          <button class="filter-btn" data-filter="Hip-Hop">Hip-Hop</button>
          <button class="filter-btn" data-filter="Street Drip">Street Drip</button>
          <button class="filter-btn" data-filter="Psychedelic">Psychedelic</button>
          <button class="filter-btn" data-filter="Typography">Typography</button>
        </div>

        <select class="sort-select" id="sort-select">
          <option value="featured">Sort: Featured</option>
          <option value="rating">Sort: Highest Rated</option>
          <option value="reviews">Sort: Most Reviews</option>
          <option value="name">Sort: Alphabetical</option>
        </select>
      </div>
    </div>
  </div>

  <main class="section" style="padding-top: 20px;">
    <div class="products-grid" id="shop-grid">
      {cards_html}
    </div>
  </main>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      const searchInput = document.getElementById('search-input');
      const sortSelect = document.getElementById('sort-select');
      const filterBtns = document.querySelectorAll('.filter-btn');
      let currentFilter = 'all';

      function applyFilters() {{
        const q = searchInput.value.toLowerCase().trim();
        const cards = Array.from(document.querySelectorAll('.product-card'));

        cards.forEach(card => {{
          const cat = card.dataset.category;
          const title = card.dataset.title;
          const matchesCat = (currentFilter === 'all' || cat === currentFilter);
          const matchesSearch = (!q || title.includes(q) || cat.toLowerCase().includes(q));

          if (matchesCat && matchesSearch) {{
            card.style.display = 'flex';
          }} else {{
            card.style.display = 'none';
          }}
        }});
      }}

      searchInput.addEventListener('input', applyFilters);

      filterBtns.forEach(btn => {{
        btn.addEventListener('click', function() {{
          filterBtns.forEach(b => b.classList.remove('is-active'));
          this.classList.add('is-active');
          currentFilter = this.dataset.filter;
          applyFilters();
        }});
      }});
    }});
  </script>
</body>
</html>
"""

# ==========================================
# 3. BUILD product.html (PHEWMEW / PINKMATTER PDP)
# ==========================================
def build_product_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flagster — Tapestry Detail</title>
  <meta name="description" content="Statement wall tapestry details, 3D interactive cloth inspection, size options, and direct purchase.">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .pdp-section {{
      padding: 40px var(--gutter) 80px;
      max-width: 1440px;
      margin: 0 auto;
    }}
    .breadcrumb {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--text-dim);
      margin-bottom: 24px;
    }}
    .breadcrumb a:hover {{ color: #fff; }}

    .pdp-layout {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 56px;
      align-items: start;
    }}

    /* Left: Media & 3D cloth simulator container */
    .pdp-media-card {{
      position: relative;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 20px;
      overflow: hidden;
      aspect-ratio: 1.38/1;
      box-shadow: var(--shadow-pop);
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
      background: radial-gradient(120% 95% at 58% 38%, #e8e9ed 0%, var(--paper) 46%, var(--paper-edge) 100%);
      display: none;
    }}
    .pdp-3d-wrapper.is-active {{
      display: block;
    }}

    .hero__cloth {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      touch-action: pan-y;
    }}
    .hero__still {{
      display: none;
    }}

    /* Toggle buttons on media */
    .pdp-view-mode-bar {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      display: flex;
      gap: 8px;
      z-index: 10;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(10px);
      padding: 4px;
      border-radius: var(--radius-pill);
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    .mode-btn {{
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      transition: all 0.2s;
    }}
    .mode-btn.is-active {{
      background: #ffffff;
      color: #000000;
    }}

    /* Right: Product Buy Box (PhewMew / PinkMatter style) */
    .pdp-buybox {{
      display: flex;
      flex-direction: column;
    }}
    .pdp-tag-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .pdp-title {{
      font-size: clamp(28px, 3.2vw, 40px);
      font-weight: 900;
      letter-spacing: -0.04em;
      line-height: 1.15;
      color: #fff;
      margin-bottom: 10px;
    }}
    .pdp-rating-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: #e2b93b;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    .pdp-rating-row span {{ color: var(--text-muted); }}

    .pdp-price-row {{
      display: flex;
      align-items: baseline;
      gap: 14px;
      padding: 18px 0;
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
    }}
    .pdp-price-sale {{
      font-size: 34px;
      font-weight: 900;
      color: #fff;
    }}
    .pdp-price-mrp {{
      font-size: 18px;
      color: var(--text-dim);
      text-decoration: line-through;
    }}
    .pdp-price-badge {{
      background: var(--accent);
      color: #fff;
      font-size: 12px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
    }}

    /* Size Selector */
    .pdp-option-group {{
      margin-bottom: 22px;
    }}
    .pdp-option-title {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #a0a6b5;
      margin-bottom: 10px;
    }}
    .pdp-size-pills {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
    }}
    .size-pill-btn {{
      padding: 12px 10px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .size-pill-btn:hover {{
      border-color: #fff;
    }}
    .size-pill-btn.is-active {{
      background: rgba(255, 255, 255, 0.12);
      border-color: #ffffff;
      box-shadow: 0 0 0 1px #fff;
    }}
    .size-name {{ font-size: 13px; font-weight: 800; color: #fff; display: block; }}
    .size-sub {{ font-size: 11px; color: var(--text-muted); display: block; margin-top: 2px; }}

    /* Quantity and Action Buttons */
    .pdp-action-row {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .pdp-qty-control {{
      display: flex;
      align-items: center;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-pill);
      height: 52px;
      padding: 0 8px;
    }}
    .pdp-qty-btn {{
      width: 36px;
      height: 36px;
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .pdp-qty-val {{
      padding: 0 14px;
      font-size: 15px;
      font-weight: 800;
      color: #fff;
    }}

    .pdp-btn-add {{
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
      gap: 8px;
      transition: all 0.2s;
    }}
    .pdp-btn-add:hover {{
      background: #f0f0f4;
      transform: translateY(-1px);
    }}

    .pdp-btn-buy {{
      width: 100%;
      height: 52px;
      background: var(--accent);
      color: #ffffff;
      border-radius: var(--radius-pill);
      font-size: 16px;
      font-weight: 900;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-bottom: 24px;
      transition: all 0.2s;
      box-shadow: 0 8px 24px var(--accent-glow);
    }}
    .pdp-btn-buy:hover {{
      background: var(--accent-hover);
      transform: translateY(-1px);
    }}

    /* Urgency & Perks */
    .stock-urgency {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      font-weight: 700;
      color: #fbbf24;
      background: rgba(251, 191, 36, 0.1);
      border: 1px solid rgba(251, 191, 36, 0.2);
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 24px;
    }}

    /* Accordions */
    .pdp-accordions {{
      border-top: 1px solid var(--border);
      margin-top: 8px;
    }}
    .accordion-item {{
      border-bottom: 1px solid var(--border);
    }}
    .accordion-header {{
      width: 100%;
      padding: 18px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      font-weight: 800;
      color: #fff;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .accordion-content {{
      padding-bottom: 18px;
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
      display: none;
    }}
    .accordion-item.is-open .accordion-content {{
      display: block;
    }}

    @media (max-width: 900px) {{
      .pdp-layout {{
        grid-template-columns: 1fr;
        gap: 36px;
      }}
    }}
  </style>
</head>
<body>
{get_header("shop")}

  <main class="pdp-section">
    <nav class="breadcrumb">
      <a href="index.html">Home</a>
      <span>/</span>
      <a href="shop.html">Shop All</a>
      <span>/</span>
      <span id="breadcrumb-title" style="color: #fff;">Tapestry</span>
    </nav>

    <div class="pdp-layout">
      <!-- Media Container with 3D Canvas Switch -->
      <div>
        <div class="pdp-media-card" id="pdp-media-box">
          <img src="" id="pdp-main-img" class="pdp-photo-view" alt="Tapestry Banner">

          <div class="pdp-3d-wrapper" id="pdp-3d-container">
            <canvas class="hero__cloth" id="pdp-cloth"></canvas>
            <img class="hero__still" alt="Tapestry 3D Preview">
          </div>

          <div class="pdp-view-mode-bar">
            <button class="mode-btn is-active" id="mode-photo-btn" onclick="setViewMode('photo')">🖼️ High-Res Photo</button>
            <button class="mode-btn" id="mode-3d-btn" onclick="setViewMode('3d')">🌀 Interactive 3D Cloth</button>
          </div>
        </div>

        <div style="margin-top: 14px; font-size: 12px; color: var(--text-dim); text-align: center;">
          Switch to <strong>Interactive 3D Cloth</strong> to tug and inspect fabric physics in real time.
        </div>
      </div>

      <!-- Buy Box -->
      <div class="pdp-buybox">
        <div class="pdp-tag-row">
          <span class="product-tag-badge" id="pdp-tag">BESTSELLER</span>
          <span class="product-discount-badge">50% DISCOUNT</span>
        </div>

        <h1 class="pdp-title" id="pdp-product-title">Loading Tapestry...</h1>

        <div class="pdp-rating-row">
          <span>★ ★ ★ ★ ★</span>
          <span id="pdp-rating-text">4.9 (340 reviews)</span>
        </div>

        <div class="pdp-price-row">
          <span class="pdp-price-sale" id="pdp-price">₹500</span>
          <span class="pdp-price-mrp" id="pdp-mrp">₹1,000</span>
          <span class="pdp-price-badge">50% OFF</span>
        </div>

        <!-- Size Selector -->
        <div class="pdp-option-group">
          <div class="pdp-option-title">
            <span>Choose Size:</span>
            <span style="color: var(--accent); font-weight: 700;">Wall Safe Grommets Included</span>
          </div>

          <div class="pdp-size-pills">
            <div class="size-pill-btn" onclick="selectSize(this, 'Small (3x2 ft)', 399, 799)">
              <span class="size-name">Small</span>
              <span class="size-sub">3 × 2 ft (₹399)</span>
            </div>
            <div class="size-pill-btn is-active" onclick="selectSize(this, 'Medium (4x3 ft)', 500, 1000)">
              <span class="size-name">Medium</span>
              <span class="size-sub">4 × 3 ft (₹500)</span>
            </div>
            <div class="size-pill-btn" onclick="selectSize(this, 'Large (5x4 ft)', 699, 1399)">
              <span class="size-name">Large</span>
              <span class="size-sub">5 × 4 ft (₹699)</span>
            </div>
          </div>
        </div>

        <!-- Stock Urgency Warning -->
        <div class="stock-urgency">
          <span>⚡</span>
          <span>High Demand: Only 6 tapestries left in stock for today's drop!</span>
        </div>

        <!-- Actions -->
        <div class="pdp-action-row">
          <div class="pdp-qty-control">
            <button class="pdp-qty-btn" onclick="changeQty(-1)">-</button>
            <span class="pdp-qty-val" id="pdp-qty">1</span>
            <button class="pdp-qty-btn" onclick="changeQty(1)">+</button>
          </div>

          <button class="pdp-btn-add" onclick="handlePdpAdd()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
            <span>Add to Cart</span>
          </button>
        </div>

        <button class="pdp-btn-buy" onclick="handlePdpBuyNow()">
          <span>Buy Now • Fast Checkout</span>
          <span>→</span>
        </button>

        <!-- Perks list -->
        <div style="background: var(--bg-surface); padding: 18px; border-radius: 12px; margin-bottom: 24px; font-size: 13px; line-height: 1.6;">
          <p>🔩 <strong>4 Corner Brass Grommets:</strong> Ready to hang with pins or hooks in 30 seconds.</p>
          <p style="margin-top: 6px;">🧵 <strong>180GSM Micro-Weave Canvas:</strong> Won't crease, sag, or tear.</p>
          <p style="margin-top: 6px;">🎨 <strong>High-Definition Thermal Dye:</strong> Rich saturated colors that never fade.</p>
        </div>

        <!-- Accordions -->
        <div class="pdp-accordions">
          <div class="accordion-item is-open">
            <button class="accordion-header" onclick="toggleAccordion(this)">
              <span>HOW TO INSTALL / APPLY</span>
              <span>+</span>
            </button>
            <div class="accordion-content">
              Mounting takes 30 seconds. Every Flagster tapestry features 4 pre-installed brass eyelets (one in each corner). Use thumbtacks, pushpins, 3M Command clear hooks, or small nails without damaging your wall or the tapestry.
            </div>
          </div>

          <div class="accordion-item">
            <button class="accordion-header" onclick="toggleAccordion(this)">
              <span>MATERIAL & CARE</span>
              <span>+</span>
            </button>
            <div class="accordion-content">
              Crafted from 100% heavyweight woven polyester canvas. Machine wash cold on gentle cycle. To remove shipping fold lines, iron on low heat from the reverse side with a cloth barrier, or steam lightly.
            </div>
          </div>

          <div class="accordion-item">
            <button class="accordion-header" onclick="toggleAccordion(this)">
              <span>SHIPPING & PACKAGING</span>
              <span>+</span>
            </button>
            <div class="accordion-content">
              Dispatched within 24 hours from our warehouse. Metro deliveries arrive in 2-3 business days; all other pin codes in 4-5 business days. Free shipping on orders over ₹999. Cash on Delivery (COD) supported.
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cloth-sim.js"></script>
  <script src="js/cart.js"></script>
  <script>
    let currentProduct = null;
    let selectedSize = 'Medium (4x3 ft)';
    let selectedPrice = 500;
    let selectedMrp = 1000;
    let currentQty = 1;
    let pdpClothEngine = null;

    document.addEventListener('DOMContentLoaded', function() {{
      const params = new URLSearchParams(window.location.search);
      const id = params.get('id') || 'music';
      currentProduct = window.FLAGSTER_PRODUCTS.find(x => x.id === id) || window.FLAGSTER_PRODUCTS[0];

      // Populate PDP
      document.title = `${{currentProduct.title}} — Flagster`;
      document.getElementById('breadcrumb-title').textContent = currentProduct.title;
      document.getElementById('pdp-product-title').textContent = currentProduct.title;
      document.getElementById('pdp-tag').textContent = currentProduct.tag;
      document.getElementById('pdp-rating-text').textContent = `${{currentProduct.rating}} (${{currentProduct.reviewsCount}} reviews)`;
      document.getElementById('pdp-main-img').src = currentProduct.img;

      // Update price
      updatePriceDisplay();
    }});

    function updatePriceDisplay() {{
      document.getElementById('pdp-price').textContent = `₹${{selectedPrice}}`;
      document.getElementById('pdp-mrp').textContent = `₹${{selectedMrp}}`;
    }}

    function selectSize(el, sizeName, price, mrp) {{
      document.querySelectorAll('.size-pill-btn').forEach(b => b.classList.remove('is-active'));
      el.classList.add('is-active');
      selectedSize = sizeName;
      selectedPrice = price;
      selectedMrp = mrp;
      updatePriceDisplay();
    }}

    function changeQty(delta) {{
      currentQty = Math.max(1, currentQty + delta);
      document.getElementById('pdp-qty').textContent = currentQty;
    }}

    function handlePdpAdd() {{
      if (!currentProduct) return;
      addToCart(currentProduct.id, currentQty, selectedSize);
    }}

    function handlePdpBuyNow() {{
      if (!currentProduct) return;
      addToCart(currentProduct.id, currentQty, selectedSize);
      closeCart();
      openCheckout();
    }}

    function toggleAccordion(btn) {{
      const item = btn.parentElement;
      item.classList.toggle('is-open');
    }}

    function setViewMode(mode) {{
      const photoView = document.getElementById('pdp-main-img');
      const container3D = document.getElementById('pdp-3d-container');
      const btnPhoto = document.getElementById('mode-photo-btn');
      const btn3D = document.getElementById('mode-3d-btn');

      if (mode === '3d') {{
        photoView.style.display = 'none';
        container3D.classList.add('is-active');
        btnPhoto.classList.remove('is-active');
        btn3D.classList.add('is-active');

        if (!pdpClothEngine && currentProduct) {{
          pdpClothEngine = window.initFlagsterCloth('pdp-cloth', 'pdp-3d-container', currentProduct.img);
        }} else if (pdpClothEngine && currentProduct) {{
          pdpClothEngine.setTexture(currentProduct.img);
        }}
      }} else {{
        photoView.style.display = 'block';
        container3D.classList.remove('is-active');
        btnPhoto.classList.add('is-active');
        btn3D.classList.remove('is-active');
      }}
    }}
  </script>
</body>
</html>
"""

# ==========================================
# 4. BUILD faq.html (HOW TO HANG & FAQ PAGE)
# ==========================================
def build_faq_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How to Hang & FAQ — Flagster Wall Tapestries</title>
  <meta name="description" content="Step-by-step hanging instructions, grommet specs, iron & washing care, shipping and returns for Flagster tapestries.">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .faq-page-header {{
      padding: 60px var(--gutter) 40px;
      max-width: 900px;
      margin: 0 auto;
      text-align: center;
    }}
    .guide-cards {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 60px;
    }}
    .guide-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 28px 24px;
      border-radius: 16px;
      text-align: center;
    }}
    .guide-num {{
      width: 44px;
      height: 44px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      color: #fff;
      font-weight: 900;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px;
      font-size: 16px;
    }}
    .guide-card h3 {{ font-size: 17px; font-weight: 800; margin-bottom: 8px; color: #fff; }}
    .guide-card p {{ font-size: 14px; color: var(--text-muted); line-height: 1.5; }}

    @media (max-width: 768px) {{
      .guide-cards {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
{get_header("faq")}

  <div class="faq-page-header">
    <span class="section-tag">Hanging & Care Guide</span>
    <h1 class="section-title">HOW TO HANG & FREQUENTLY ASKED</h1>
    <p class="section-sub" style="margin: 12px auto 0;">Everything you need to know about mounting with brass grommets, ironing out folds, and delivery.</p>
  </div>

  <main class="section" style="padding-top: 0; max-width: 960px;">
    <!-- Step by Step Guide -->
    <div class="guide-cards">
      <div class="guide-card">
        <div class="guide-num">1</div>
        <h3>Choose Your Spot</h3>
        <p>Pick a smooth wall above your bed, desk, or sofa. Measure ~4.3 × 3.0 ft of space.</p>
      </div>
      <div class="guide-card">
        <div class="guide-num">2</div>
        <h3>Pin Top Corners</h3>
        <p>Insert pushpins, hooks, or nails through the two top reinforced brass eyelets.</p>
      </div>
      <div class="guide-card">
        <div class="guide-num">3</div>
        <h3>Tension Bottom Grommets</h3>
        <p>Pull slightly taut and secure the bottom two grommets for a smooth, wrinkle-free drape.</p>
      </div>
    </div>

    <!-- FAQ Accordion -->
    <div class="faq-wrapper" style="max-width: 100%;">
      <h2 style="font-size: 24px; font-weight: 900; margin-bottom: 24px;">Hanging & Material Questions</h2>

      <div class="faq-item is-open">
        <button class="faq-question">
          <span>What hooks or pins should I use?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          Our tapestries have 4 solid brass grommets (diameter: 10mm). You can use ordinary metallic thumbtacks, colorful pushpins, 3M Command hooks, or small drywall nails. No special tools required!
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-question">
          <span>How do I remove the shipping folds/creases?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          Due to shipping, tapestries arrive folded. You can effortlessly eliminate fold lines by steaming with a garment steamer, or by ironing on low-to-medium heat on the back face with a cotton cloth barrier.
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-question">
          <span>Can I wash the tapestry in a washing machine?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          Yes! Flagster canvas is 100% colorfast. Machine wash cold on gentle cycle with mild detergent. Hang to dry. Do not bleach or tumble dry on high heat.
        </div>
      </div>

      <h2 style="font-size: 24px; font-weight: 900; margin: 40px 0 24px;" id="shipping">Shipping, COD & Returns</h2>

      <div class="faq-item">
        <button class="faq-question">
          <span>When will my order ship and arrive?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          All orders are processed and handed to courier partners within 24 hours. Metros (Mumbai, Delhi, Bangalore, etc.) take 2-3 business days. Rest of India takes 4-5 business days. You will receive live WhatsApp/SMS tracking.
        </div>
      </div>

      <div class="faq-item">
        <button class="faq-question">
          <span>Is Cash on Delivery (COD) available?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          Yes! Cash on Delivery is available across all pin codes in India. You only pay when the delivery executive hands you the package.
        </div>
      </div>

      <div class="faq-item" id="returns">
        <button class="faq-question">
          <span>What is your return & replacement policy?</span>
          <span class="faq-chevron">↓</span>
        </button>
        <div class="faq-answer">
          We offer a 7-day hassle-free replacement guarantee. If your flag arrives with any print defect or stitching issue, WhatsApp us or email support@flagster.in with a photo, and we will dispatch a replacement immediately.
        </div>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script>
    document.querySelectorAll('.faq-question').forEach(btn => {{
      btn.addEventListener('click', function() {{
        const item = this.parentElement;
        item.classList.toggle('is-open');
      }});
    }});
  </script>
</body>
</html>
"""

# ==========================================
# 5. BUILD contact.html (CONTACT & ORDER TRACKING)
# ==========================================
def build_contact_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contact & Order Tracking — Flagster</title>
  <meta name="description" content="Track your Flagster shipment, WhatsApp customer support, and get in touch with our team.">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="css/style.css">
  <style>
    .contact-layout {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 56px;
      max-width: 1100px;
      margin: 0 auto;
    }}
    .card-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 36px;
    }}
    .whatsapp-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: #25d366;
      color: #000;
      font-weight: 800;
      padding: 14px 22px;
      border-radius: var(--radius-pill);
      font-size: 15px;
      margin-top: 18px;
      transition: transform 0.2s;
    }}
    .whatsapp-badge:hover {{
      transform: translateY(-2px);
    }}
    .track-result-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      padding: 20px;
      border-radius: 12px;
      margin-top: 20px;
      display: none;
    }}
    @media (max-width: 800px) {{
      .contact-layout {{ grid-template-columns: 1fr; gap: 32px; }}
    }}
  </style>
</head>
<body>
{get_header("contact")}

  <div class="shop-header" style="text-align: center; max-width: 700px; margin: 0 auto; padding-bottom: 0;">
    <span class="section-tag">Direct Support</span>
    <h1 class="section-title">WE ARE HERE TO HELP</h1>
    <p class="section-sub" style="margin: 12px auto 0;">Have a question about your order, tracking, or a custom drop? Message us anytime.</p>
  </div>

  <main class="section">
    <div class="contact-layout">
      <!-- Order Tracking Card -->
      <div class="card-box">
        <h3 style="font-size: 22px; font-weight: 900; margin-bottom: 8px;">Track Your Shipment</h3>
        <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 24px;">Enter your 5-digit Order ID (from your confirmation screen or SMS) to check real-time courier status.</p>

        <form onsubmit="handleTrack(event)">
          <div class="form-group">
            <label>Order ID</label>
            <input type="text" class="form-input" id="track-id-input" placeholder="e.g. FLG-84920 or 84920" required>
          </div>
          <button type="submit" class="btn btn-accent" style="width: 100%;">
            <span>Track Status</span>
            <span>→</span>
          </button>
        </form>

        <div class="track-result-box" id="track-result">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <strong style="color: #fff;" id="track-order-num">#FLG-84920</strong>
            <span style="background: rgba(16, 185, 129, 0.2); color: var(--green); padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 800;">OUT FOR DELIVERY</span>
          </div>
          <p style="font-size: 13px; color: var(--text-muted);">Courier: BlueDart Express • Tracking: BD9402850IN</p>
          <p style="font-size: 13px; color: #fff; margin-top: 8px;"><strong>Estimated Arrival:</strong> Tomorrow by 5:00 PM</p>
        </div>

        <div style="margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border);">
          <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 8px;">Instant WhatsApp Support</h4>
          <p style="font-size: 13px; color: var(--text-muted);">Quickest response time: Mon–Sat, 10am to 8pm IST.</p>
          <a href="https://wa.me/919876543210?text=Hi%20Flagster%20Team!%20I%20have%20a%20question%20about%20my%20order" target="_blank" class="whatsapp-badge">
            <span>💬 Chat on WhatsApp (+91 98765 43210)</span>
          </a>
        </div>
      </div>

      <!-- Contact Message Form -->
      <div class="card-box">
        <h3 style="font-size: 22px; font-weight: 900; margin-bottom: 8px;">Send Us a Message</h3>
        <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 24px;">Drop us a note and our Mumbai studio team will get back to you within 4 hours.</p>

        <form onsubmit="handleContactSubmit(event)">
          <div class="form-group">
            <label>Your Name</label>
            <input type="text" class="form-input" placeholder="e.g. Aryan Sharma" required>
          </div>

          <div class="form-group">
            <label>Email Address</label>
            <input type="email" class="form-input" placeholder="aryan@example.com" required>
          </div>

          <div class="form-group">
            <label>Subject</label>
            <input type="text" class="form-input" placeholder="e.g. Question about size / Bulk order">
          </div>

          <div class="form-group">
            <label>Message</label>
            <textarea class="form-input" style="height: 120px; padding: 12px; resize: vertical;" placeholder="How can we help your walls look better?" required></textarea>
          </div>

          <button type="submit" class="btn btn-primary" style="width: 100%;">
            <span>Send Message</span>
            <span>✉️</span>
          </button>
        </form>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script>
    function handleTrack(e) {{
      e.preventDefault();
      const val = document.getElementById('track-id-input').value.trim();
      const resultBox = document.getElementById('track-result');
      const orderNumEl = document.getElementById('track-order-num');
      orderNumEl.textContent = val.startsWith('#') ? val : `#FLG-${{val.replace('FLG-','')}}`;
      resultBox.style.display = 'block';
    }}

    function handleContactSubmit(e) {{
      e.preventDefault();
      alert('Message sent! Our support team will reply to your email within 4 hours.');
      e.target.reset();
    }}
  </script>
</body>
</html>
"""

# Write all pages
base = '/home/maahir/.gemini/antigravity/scratch/peculiar-atelier'

with open(f'{base}/index.html', 'w', encoding='utf-8') as f:
    f.write(build_index_html())
print("Built index.html")

with open(f'{base}/shop.html', 'w', encoding='utf-8') as f:
    f.write(build_shop_html())
print("Built shop.html")

with open(f'{base}/product.html', 'w', encoding='utf-8') as f:
    f.write(build_product_html())
print("Built product.html")

with open(f'{base}/faq.html', 'w', encoding='utf-8') as f:
    f.write(build_faq_html())
print("Built faq.html")

with open(f'{base}/contact.html', 'w', encoding='utf-8') as f:
    f.write(build_contact_html())
print("Built contact.html")

print("All 5 pages generated successfully!")
