# 🏴 FLAGSTER — Wall Drip For Your Sanctuary

Official e-commerce website for **FLAGSTER**, inspired by streetwear brands like [PhewMew](https://www.phewmew.in/) and [PinkMatter](https://pinkmatter.shop/). Built with modern design engineering playbooks (Impeccable, Apple Design, Taste, UI UX Pro Max).

---

## ⚡ Live Features

- **Real-Time 3D WebGL Cloth Physics Hero**: Drag, tug, and swing the fabric with real-time Verlet physics and neutral studio lighting.
- **Interactive Tapestry Switcher**: Live previews of any tapestry draped on the 3D cloth canvas.
- **PhewMew / PinkMatter Style Product Detail Page (PDP)**:
  - Dual view toggle: High-res print photo vs. interactive 3D cloth simulator.
  - Size selectors: Small (3×2 ft ₹399), Medium (4×3 ft ₹500), Large (5×4 ft ₹699).
  - Add to Cart with slide-in cart drawer + Wishlist button + Instant Buy Now.
  - Authentic accordion information sections (`HOW TO INSTALL / APPLY`, `MATERIAL & CARE`, `SHIPPING & PACKAGING`).
  - Trust badges: 3-5 days Pan-India delivery, 100% secure checkout, fade-proof thermal dye.
- **Persistent Shopping Cart (`localStorage`)**:
  - Slide-in side drawer.
  - Free shipping progress bar (Free delivery over ₹499).
  - Discount coupon input (`FLAGSTER10` for 10% extra off).
  - Complete checkout modal with Cash on Delivery (COD), UPI QR simulation, and Card payments.
- **Multi-Page Experience**:
  - `index.html`: Hero with interactive 3D cloth, feature marquee, trending drops, 30s hang guide, and customer wall showcase.
  - `shop.html`: Catalog with category filtering (Hip-Hop, Street Drip, Psychedelic, Typography), search bar, and sort selector.
  - `product.html`: Dynamic PDP loading each tapestry by URL parameter (`?id=pnd`, `?id=music`, etc.).
  - `faq.html`: How to hang visual guide (pushpins, hooks, grommets) and brand policies.
  - `contact.html`: Live order tracking simulation and direct WhatsApp support.

---

## 🏷️ Products & Pricing

Every statement flag is priced at **₹500** (Flat 50% discount from ₹1,000 MRP):

1. **Dreamin PartyNextDoor Cover Tapestry** (`pnd`) — Hip-Hop
2. **MUSIC IS MY DR★G Tapestry** (`music`) — Typography
3. **Hardstone Psycho Rider Tapestry** (`hardstone`) — Street Drip
4. **Tame Impala — Currents Tapestry** (`currents`) — Psychedelic
5. **Kendrick Lamar — DAMN. Tapestry** (`damn`) — Hip-Hop
6. **Travis Scott — Circus Maximus Tapestry** (`travis-utopia`) — Hip-Hop
7. **Playboi Carti — Whole Lotta Red Tapestry** (`carti`) — Hip-Hop
8. **Strange By Design — Chrome Octopus Tapestry** (`strange`) — Psychedelic

---

## 🚀 Technologies

- Native WebGL 1 shader pipeline with zero external libraries.
- Vanilla JavaScript & CSS custom properties for lightweight, zero-dependency, instant loading.
- Responsive across mobile (375px+), tablet, and ultrawide desktop displays.
