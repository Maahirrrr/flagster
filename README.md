# Flagster / Peculiar Atelier

A standalone, single-file interactive full-screen hero section featuring a real-time WebGL 1 cloth simulation with custom holographic foil shading.

Built with **vanilla HTML, CSS, and WebGL** — no frameworks, no build step, no libraries, and zero local asset dependencies.

## Features

- **Real-Time 3D Cloth Physics**:
  - 46 × 42 mass-spring particle lattice (`COLS = 46`, `ROWS = 42`).
  - Distance constraints across orthogonal neighbors, cell diagonals, 2-apart bends, and 5-apart bends.
  - Verlet integration with time-based flutter, gusts, speed capping, and dual-pin tether clamping.
  - 360-step pre-warmup integration so the cloth hangs naturally from the initial frame.
  - Interactive pointer picking with depth-weighted ray projection, $(1 - d^2)^2$ quartic kernel carry weights, and pointer capture with release momentum.

- **Custom Holographic Foil Shader**:
  - High-precision GLSL fragment shader modeling three softbox studio reflections (overhead strip light, side softbox, key light) with `smoothstep(-0.5, 0.5)` borders.
  - Multi-harmonic iridescent thin-film color phase calculation.
  - Print luminance-based metallic gloss modulation and cubic Fresnel rim glow.
  - Back-face foil lighting and soft highlight roll-off curve.

- **Dynamic Studio Shadow**:
  - 1/8 resolution offscreen framebuffer silhouette rendering with 7×7 Gaussian blur composite.

- **Responsive & Accessible**:
  - Desktop wide layout (`width >= 1100`, `aspectRatio >= 1.25`) side-by-side with large display title.
  - Stacked mobile layout responsive down to 375px with zero horizontal scroll.
  - Smooth entrance rise animations, hover transitions, and keyboard focus outlines.
  - Full support for `prefers-reduced-motion: reduce`.
  - Automatic graceful fallback to styled still image if WebGL is unavailable.

## Usage

Simply open `index.html` in any modern web browser or serve with any static web server:

```bash
# Python 3
python3 -m http.server 8000

# or Node.js npx serve
npx serve .
```
