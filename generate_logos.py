import os

os.chdir('/home/maahir/.gemini/antigravity/scratch/peculiar-atelier/assets/logo')

# 1. STANDALONE LOGOMARK: The Flagster Banner-Star Emblem
# Combining a hanging flag silhouette, 4 corner brass grommets, and a razor-sharp cultural 4-point star.
MARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Subtle brutalist geometry and gradients if needed -->
    <clipPath id="flag-clip">
      <rect x="56" y="76" width="400" height="360" rx="20" />
    </clipPath>
  </defs>

  <!-- Dark Background Plate for standalone preview -->
  <rect width="512" height="512" rx="32" fill="#090a0d" />

  <!-- Outer Flag Silhouette -->
  <rect x="56" y="76" width="400" height="360" rx="16" fill="#141722" stroke="#ffffff" stroke-width="8" />

  <!-- 4 Corner Brass Grommets (Eyelets) -->
  <!-- Top Left -->
  <circle cx="96" cy="116" r="18" fill="#ffadc6" />
  <circle cx="96" cy="116" r="8" fill="#090a0d" />
  <!-- Top Right -->
  <circle cx="416" cy="116" r="18" fill="#ffadc6" />
  <circle cx="416" cy="116" r="8" fill="#090a0d" />
  <!-- Bottom Left -->
  <circle cx="96" cy="396" r="18" fill="#ffadc6" />
  <circle cx="96" cy="396" r="8" fill="#090a0d" />
  <!-- Bottom Right -->
  <circle cx="416" cy="396" r="18" fill="#ffadc6" />
  <circle cx="416" cy="396" r="8" fill="#090a0d" />

  <!-- Center Brutalist Flagster Star -->
  <!-- 4-point Diamond Star with razor cuts -->
  <path d="M 256 120 
           C 256 195, 275 225, 390 256 
           C 275 287, 256 317, 256 392 
           C 256 317, 237 287, 122 256 
           C 237 225, 256 195, 256 120 Z" 
        fill="#ffffff" />

  <!-- Center Grommet Cutout -->
  <circle cx="256" cy="256" r="16" fill="#090a0d" />
  <circle cx="256" cy="256" r="10" fill="#ffadc6" />
</svg>
"""

with open('logo-mark.svg', 'w') as f:
    f.write(MARK_SVG)

# 2. FULL HORIZONTAL LOCKUP: Mark + Custom Wordmark + Tagline
FULL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" width="1000" height="240">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@900&amp;display=swap');
      .brand-title {
        font-family: 'Work Sans', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 900;
        font-size: 88px;
        letter-spacing: -0.05em;
        fill: #ffffff;
      }
      .brand-sub {
        font-family: 'Work Sans', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.18em;
        fill: #8e95a5;
        text-transform: uppercase;
      }
      .badge-text {
        font-family: 'Work Sans', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800;
        font-size: 13px;
        letter-spacing: 0.08em;
        fill: #000000;
      }
    </style>
  </defs>

  <!-- Left: Logomark (Flag with grommets & star) -->
  <g transform="translate(20, 20) scale(0.39)">
    <!-- Outer Flag Canvas -->
    <rect x="56" y="76" width="400" height="360" rx="20" fill="#141722" stroke="#ffffff" stroke-width="12" />

    <!-- 4 Grommets -->
    <circle cx="106" cy="126" r="22" fill="#ffadc6" />
    <circle cx="106" cy="126" r="10" fill="#090a0d" />
    <circle cx="406" cy="126" r="22" fill="#ffadc6" />
    <circle cx="406" cy="126" r="10" fill="#090a0d" />
    <circle cx="106" cy="386" r="22" fill="#ffadc6" />
    <circle cx="106" cy="386" r="10" fill="#090a0d" />
    <circle cx="406" cy="386" r="22" fill="#ffadc6" />
    <circle cx="406" cy="386" r="10" fill="#090a0d" />

    <!-- Center 4-Point Star -->
    <path d="M 256 120 
             C 256 195, 275 225, 390 256 
             C 275 287, 256 317, 256 392 
             C 256 317, 237 287, 122 256 
             C 237 225, 256 195, 256 120 Z" 
          fill="#ffffff" />
    <circle cx="256" cy="256" r="16" fill="#ffadc6" />
  </g>

  <!-- Right: Wordmark -->
  <text x="240" y="132" class="brand-title">FLAGSTER</text>

  <!-- Badge: ORIGINALS -->
  <rect x="730" y="76" width="104" height="28" rx="14" fill="#ffadc6" />
  <text x="746" y="95" class="badge-text">ORIGINALS</text>

  <!-- Subtitle: WALL DRIP · EST. 2026 -->
  <text x="244" y="176" class="brand-sub">WALL DRIP · UNUSUAL BY INTENT · EST. 2026</text>
</svg>
"""

with open('logo-full.svg', 'w') as f:
    f.write(FULL_SVG)

# 3. FAVICON & COMPACT APP ICON (64x64 and 32x32 scalable)
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#090a0d" />
  <rect x="8" y="10" width="48" height="44" rx="4" fill="#141722" stroke="#ffffff" stroke-width="2.5" />
  
  <!-- Grommets -->
  <circle cx="15" cy="17" r="3" fill="#ffadc6" />
  <circle cx="49" cy="17" r="3" fill="#ffadc6" />
  <circle cx="15" cy="47" r="3" fill="#ffadc6" />
  <circle cx="49" cy="47" r="3" fill="#ffadc6" />

  <!-- Center Star -->
  <path d="M 32 16 
           C 32 25, 34 29, 48 32 
           C 34 35, 32 39, 32 48 
           C 32 39, 30 35, 16 32 
           C 30 29, 32 25, 32 16 Z" 
        fill="#ffffff" />
  <circle cx="32" cy="32" r="2.5" fill="#ffadc6" />
</svg>
"""

with open('favicon.svg', 'w') as f:
    f.write(FAVICON_SVG)

# 4. MONOCHROME INVERTED VARIANT (All White for dark screens)
MONO_WHITE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 160" width="760" height="160">
  <defs>
    <style>
      .mono-title {
        font-family: 'Work Sans', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 900;
        font-size: 80px;
        letter-spacing: -0.05em;
        fill: #ffffff;
      }
    </style>
  </defs>
  <g transform="translate(10, 15) scale(0.28)">
    <rect x="56" y="76" width="400" height="360" rx="20" fill="none" stroke="#ffffff" stroke-width="16" />
    <circle cx="106" cy="126" r="20" fill="#ffffff" />
    <circle cx="406" cy="126" r="20" fill="#ffffff" />
    <circle cx="106" cy="386" r="20" fill="#ffffff" />
    <circle cx="406" cy="386" r="20" fill="#ffffff" />
    <path d="M 256 120 C 256 195, 275 225, 390 256 C 275 287, 256 317, 256 392 C 256 317, 237 287, 122 256 C 237 225, 256 195, 256 120 Z" fill="#ffffff" />
    <circle cx="256" cy="256" r="14" fill="#090a0d" />
  </g>
  <text x="180" y="110" class="mono-title">FLAGSTER</text>
</svg>
"""

with open('logo-mono-white.svg', 'w') as f:
    f.write(MONO_WHITE)

print("Generated vector logo suite in assets/logo/ successfully!")
