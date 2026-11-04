// Flagster Real-time WebGL Cloth Simulation Engine
window.initFlagsterCloth = function(canvasId, heroId, initialSrc) {
  const canvas = document.getElementById(canvasId);
  const hero = document.getElementById(heroId);
  if (!canvas || !hero) return null;

  function failover() {
    hero.classList.add('no-cloth');
  }

  let gl = null;
  try {
    gl = canvas.getContext('webgl', {
      alpha: true,
      antialias: true,
      premultipliedAlpha: true,
      powerPreference: 'high-performance'
    });
  } catch (e) {
    failover();
    return null;
  }

  if (!gl) {
    failover();
    return null;
  }

  canvas.addEventListener('webglcontextlost', function(e) {
    e.preventDefault();
    failover();
  });

  const size = 0.90;
  const aspect = 1.38;
  const spread = 0.98;
  const pinRoll = 5.5 * Math.PI / 180;
  const flutter = 0.35;
  let damping = 0.30;
  const stiffness = 0.60;
  const crumple = 0.55;
  const grabRadius = 0.12;
  const carryRadius = 0.20;
  const gravity = 2.6;
  const tilt = -10 * Math.PI / 180;
  const turn = -12 * Math.PI / 180;
  const perspective = 0.45;
  const maxSpeed = 12;
  const steps = 8;

  const COLS = 46;
  const ROWS = 42;
  const NUM_POINTS = COLS * ROWS;
  const CH = size;
  const CW = size * aspect;

  const t = tilt;
  const r = turn;
  const cosR = Math.cos(r), sinR = Math.sin(r);
  const cosT = Math.cos(t), sinT = Math.sin(t);

  const R0 = [cosR, 0, sinR];
  const R1 = [sinT * sinR, cosT, -sinT * cosR];
  const R2 = [-cosT * sinR, sinT, cosT * cosR];

  const invR0 = [R0[0], R1[0], R2[0]];
  const invR1 = [R0[1], R1[1], R2[1]];
  const invR2 = [R0[2], R1[2], R2[2]];

  const CAM = Math.exp(Math.log(18) * (1 - perspective) + Math.log(1.7) * perspective);

  let heroWidth = 1;
  let heroHeight = 1;
  let aspectRatio = 1;
  let cx = 0.38;
  let cy = 0.485;
  let zoom = 1.0;

  function ridge(x) {
    return Math.sqrt(Math.sin(x) * Math.sin(x) + 0.03) - 0.64;
  }

  function crease(u, v) {
    return crumple * 0.045 * CH * (
      ridge(2.7 * u + 2.9 * v + 0.7) +
      0.8 * ridge(-2.6 * u + 3.3 * v + 2.1) +
      0.5 * Math.sin(4.9 * u - 1.4 * v + 2.2) +
      0.55 * ridge(1.1 * u + 6.4 * v + 1.3) +
      0.4 * ridge(8.3 * u + 3.9 * v + 0.2) +
      0.3 * ridge(-5.7 * u + 9.1 * v + 1.6)
    );
  }

  const flatX = new Float32Array(NUM_POINTS);
  const flatY = new Float32Array(NUM_POINTS);
  const pRest = new Float32Array(NUM_POINTS * 3);

  for (let row = 0; row < ROWS; row++) {
    const v = row / (ROWS - 1);
    for (let col = 0; col < COLS; col++) {
      const u = col / (COLS - 1);
      const i = row * COLS + col;
      const fx = (u - 0.5) * CW;
      const fy = (v - 0.5) * CH;
      flatX[i] = fx;
      flatY[i] = fy;
      pRest[3 * i] = fx;
      pRest[3 * i + 1] = fy;
      pRest[3 * i + 2] = crease(u, v);
    }
  }

  const leftPinIdx = (ROWS - 1) * COLS + 0;
  const rightPinIdx = (ROWS - 1) * COLS + (COLS - 1);

  const half = 0.5 * CW * spread;
  const topEdge = 0.5 * CH;
  const roll = pinRoll;
  const pinL = new Float32Array([-half * Math.cos(roll), topEdge + half * Math.sin(roll), 0]);
  const pinR = new Float32Array([half * Math.cos(roll), topEdge - half * Math.sin(roll), 0]);

  const maxDistLeft = new Float32Array(NUM_POINTS);
  const maxDistRight = new Float32Array(NUM_POINTS);
  for (let i = 0; i < NUM_POINTS; i++) {
    const flatDistL = Math.hypot(flatX[i] - (-0.5 * CW), flatY[i] - (0.5 * CH));
    const flatDistR = Math.hypot(flatX[i] - (0.5 * CW), flatY[i] - (0.5 * CH));
    maxDistLeft[i] = 1.02 * flatDistL;
    maxDistRight[i] = 1.02 * flatDistR;
  }

  const linksA = [];
  const linksB = [];
  const linkRestDist = [];
  const linkStiff = [];

  function addLink(i, j, s) {
    linksA.push(i);
    linksB.push(j);
    const dx = pRest[3 * j] - pRest[3 * i];
    const dy = pRest[3 * j + 1] - pRest[3 * i + 1];
    const dz = pRest[3 * j + 2] - pRest[3 * i + 2];
    linkRestDist.push(Math.hypot(dx, dy, dz));
    linkStiff.push(s);
  }

  const bend = 0.02 + (0.60 - 0.02) * stiffness;

  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const i = row * COLS + col;
      if (col + 1 < COLS) addLink(i, row * COLS + (col + 1), 1.0);
      if (row + 1 < ROWS) addLink(i, (row + 1) * COLS + col, 1.0);
      if (col + 1 < COLS && row + 1 < ROWS) {
        addLink(i, (row + 1) * COLS + (col + 1), 0.5);
        addLink(row * COLS + (col + 1), (row + 1) * COLS + col, 0.5);
      }
      if (col + 2 < COLS) addLink(i, row * COLS + (col + 2), bend);
      if (row + 2 < ROWS) addLink(i, (row + 2) * COLS + col, bend);
      if (col + 5 < COLS) addLink(i, row * COLS + (col + 5), bend * 0.5);
      if (row + 5 < ROWS) addLink(i, (row + 5) * COLS + col, bend * 0.5);
    }
  }

  const linkCount = linksA.length;
  const linksAArray = new Int32Array(linksA);
  const linksBArray = new Int32Array(linksB);
  const linkRestDistArray = new Float32Array(linkRestDist);
  const linkStiffArray = new Float32Array(linkStiff);

  const pos = new Float32Array(NUM_POINTS * 3);
  const prev = new Float32Array(NUM_POINTS * 3);
  const normals = new Float32Array(NUM_POINTS * 3);

  for (let row = 0; row < ROWS; row++) {
    const v = row / (ROWS - 1);
    for (let col = 0; col < COLS; col++) {
      const u = col / (COLS - 1);
      const i = row * COLS + col;
      const fx = flatX[i];
      const fy = flatY[i];

      const scaleX = spread + (1 - spread) * Math.pow(1 - v, 2);
      const xScaled = fx * scaleX;
      const dx = xScaled;
      const dy = fy - topEdge;

      const px = dx * Math.cos(roll) + dy * Math.sin(roll);
      const py = topEdge - dx * Math.sin(roll) + dy * Math.cos(roll);
      const pz = crease(u, v);

      pos[3 * i] = px;
      pos[3 * i + 1] = py;
      pos[3 * i + 2] = pz;

      prev[3 * i] = px;
      prev[3 * i + 1] = py;
      prev[3 * i + 2] = pz;
    }
  }

  pos[3 * leftPinIdx] = pinL[0];
  pos[3 * leftPinIdx + 1] = pinL[1];
  pos[3 * leftPinIdx + 2] = pinL[2];
  prev[3 * leftPinIdx] = pinL[0];
  prev[3 * leftPinIdx + 1] = pinL[1];
  prev[3 * leftPinIdx + 2] = pinL[2];

  pos[3 * rightPinIdx] = pinR[0];
  pos[3 * rightPinIdx + 1] = pinR[1];
  pos[3 * rightPinIdx + 2] = pinR[2];
  prev[3 * rightPinIdx] = pinR[0];
  prev[3 * rightPinIdx + 1] = pinR[1];
  prev[3 * rightPinIdx + 2] = pinR[2];

  let isHeld = false;
  let activePointerId = null;
  let grabbedIdx = -1;
  let grabRemDepth = 0;
  let grabOffsetX = 0;
  let grabOffsetY = 0;
  const currentPointer = { clientX: 0, clientY: 0 };
  const carryWeights = new Float32Array(NUM_POINTS);

  const numQuads = (COLS - 1) * (ROWS - 1);
  const indices = new Uint16Array(numQuads * 6);
  let iOffset = 0;
  for (let row = 0; row < ROWS - 1; row++) {
    for (let col = 0; col < COLS - 1; col++) {
      const p00 = row * COLS + col;
      const p10 = row * COLS + (col + 1);
      const p01 = (row + 1) * COLS + col;
      const p11 = (row + 1) * COLS + (col + 1);

      indices[iOffset++] = p00;
      indices[iOffset++] = p10;
      indices[iOffset++] = p11;

      indices[iOffset++] = p00;
      indices[iOffset++] = p11;
      indices[iOffset++] = p01;
    }
  }

  const texCoords = new Float32Array(NUM_POINTS * 2);
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const i = row * COLS + col;
      // Inset UV coordinates by 0.8% to avoid edge bleeding and white boundary sampling
      const u = 0.008 + (col / 45.0) * 0.984;
      const v = 0.008 + (1.0 - row / 41.0) * 0.984;
      texCoords[2 * i] = u;
      texCoords[2 * i + 1] = v;
    }
  }

  function compileShader(type, src) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  function createProgram(vsSrc, fsSrc) {
    const vs = compileShader(gl.VERTEX_SHADER, vsSrc);
    const fs = compileShader(gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      gl.deleteProgram(prog);
      return null;
    }
    return prog;
  }

  const clothVsSource = `
    attribute vec3 a_position;
    attribute vec3 a_normal;
    attribute vec2 a_texCoord;

    uniform mat3 u_R;
    uniform float u_cam;
    uniform float u_zoom;
    uniform float u_aspectRatio;
    uniform vec2 u_c;

    varying vec3 v_viewPos;
    varying vec3 v_viewNormal;
    varying vec2 v_uv;

    void main() {
      vec3 q = u_R * a_position;
      vec3 vn = u_R * a_normal;
      float scale = u_cam / max(u_cam - q.z, 0.001);
      vec2 screen = q.xy * scale * u_zoom;

      float clipX = 2.0 * (u_c.x + screen.x / u_aspectRatio) - 1.0;
      float clipY = 1.0 - 2.0 * (u_c.y - screen.y);
      float clipZ = -q.z * 0.5;

      gl_Position = vec4(clipX, clipY, clipZ, 1.0);
      v_viewPos = q;
      v_viewNormal = vn;
      v_uv = a_texCoord;
    }
  `;

  const clothFsSource = `
    precision highp float;

    varying vec3 v_viewPos;
    varying vec3 v_viewNormal;
    varying vec2 v_uv;

    uniform sampler2D u_texture;
    uniform float u_hasTexture;
    uniform float u_cam;

    float boxLight(vec3 dir, vec3 centre, vec2 halfSize, float soft) {
      vec3 up = abs(centre.y) < 0.99 ? vec3(0.0, 1.0, 0.0) : vec3(1.0, 0.0, 0.0);
      vec3 right = normalize(cross(up, centre));
      vec3 top = cross(centre, right);
      vec3 d = dir - centre;
      float dx = dot(d, right);
      float dy = dot(d, top);
      float ex = smoothstep(-0.5, 0.5, (halfSize.x - abs(dx)) / soft);
      float ey = smoothstep(-0.5, 0.5, (halfSize.y - abs(dy)) / soft);
      return ex * ey;
    }

    void main() {
      vec3 n = normalize(v_viewNormal);
      bool back = n.z < 0.0;
      if (back) n = -n;

      vec3 V = normalize(vec3(0.0, 0.0, u_cam) - v_viewPos);
      vec3 Rf = reflect(-V, n);
      vec3 KEY = normalize(vec3(-0.42, 0.45, 0.79));
      float nv = clamp(dot(n, V), 0.0, 1.0);
      float nl = max(dot(n, KEY), 0.0);

      vec3 printCol;
      if (u_hasTexture > 0.5) {
        printCol = pow(texture2D(u_texture, v_uv).rgb, vec3(2.2));
      } else {
        printCol = vec3(0.05, 0.05, 0.05);
      }

      float shade = 0.46 + 0.68 * nl + 0.08 * n.y;
      float key = pow(max(dot(Rf, KEY), 0.0), 26.0);

      float strip = boxLight(Rf, normalize(vec3(0.08, 0.93, 0.36)), vec2(1.1, 0.07), 0.22);
      float side = boxLight(Rf, normalize(vec3(0.86, 0.12, 0.50)), vec2(0.06, 0.85), 0.20);
      float fill = boxLight(Rf, KEY, vec2(0.42, 0.30), 0.35);

      vec3 holo = vec3(1.0);

      float lum = dot(printCol, vec3(0.2126, 0.7152, 0.0722));
      float gloss = mix(1.0, 0.45, smoothstep(0.55, 0.9, lum));
      vec3 spec = holo * gloss * mix(vec3(1.0), printCol * 2.4 + 0.08, 0.65) * (0.34 * key + 0.11 * strip + 0.07 * side + 0.02 * fill);

      vec3 colour = printCol * shade + spec + holo * printCol * 0.4 * pow(1.0 - nv, 3.0);

      if (back) {
        vec3 backFabric = vec3(0.12, 0.12, 0.13) * (0.35 + 0.9 * nl) + spec * 0.7;
        colour = mix(backFabric, printCol * shade, 0.42);
      }

      colour = min(colour, vec3(0.8)) + vec3(0.2) * (vec3(1.0) - exp(-max(colour - vec3(0.8), vec3(0.0)) / 0.2));

      gl_FragColor = vec4(pow(colour, vec3(1.0 / 2.2)), 1.0);
    }
  `;

  const shadowSilVsSource = `
    attribute vec3 a_position;
    uniform mat3 u_R;
    uniform float u_cam;
    uniform float u_zoom;
    uniform float u_aspectRatio;
    uniform vec2 u_c;

    void main() {
      vec3 q = u_R * a_position;
      float scale = u_cam / max(u_cam - q.z, 0.001);
      vec2 screen = q.xy * scale * u_zoom;
      float clipX = 2.0 * (u_c.x + screen.x / u_aspectRatio) - 1.0;
      float clipY = 1.0 - 2.0 * (u_c.y - screen.y);
      float clipZ = -q.z * 0.5;
      gl_Position = vec4(clipX, clipY, clipZ, 1.0);
    }
  `;

  const shadowSilFsSource = `
    precision mediump float;
    void main() {
      gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
  `;

  const shadowBlurVsSource = `
    attribute vec2 a_pos;
    varying vec2 v_uv;
    void main() {
      v_uv = a_pos * 0.5 + 0.5;
      gl_Position = vec4(a_pos, 0.0, 1.0);
    }
  `;

  const shadowBlurFsSource = `
    precision highp float;
    varying vec2 v_uv;
    uniform sampler2D u_shadowTex;
    uniform vec2 u_spacing;
    uniform vec2 u_shift;

    void main() {
      vec2 baseUV = v_uv - u_shift;
      float sum = 0.0;
      float totalWeight = 0.0;
      for (int i = -3; i <= 3; i++) {
        for (int j = -3; j <= 3; j++) {
          float d2 = float(i * i + j * j);
          float w = exp(-d2 / 6.0);
          vec2 offset = vec2(float(i), float(j)) * u_spacing;
          sum += texture2D(u_shadowTex, baseUV + offset).r * w;
          totalWeight += w;
        }
      }
      float alpha = (sum / totalWeight) * 0.30;
      vec3 col = vec3(0.07, 0.07, 0.16) * alpha;
      gl_FragColor = vec4(col, alpha);
    }
  `;

  const clothProgram = createProgram(clothVsSource, clothFsSource);
  const shadowSilProgram = createProgram(shadowSilVsSource, shadowSilFsSource);
  const shadowBlurProgram = createProgram(shadowBlurVsSource, shadowBlurFsSource);

  if (!clothProgram || !shadowSilProgram || !shadowBlurProgram) {
    failover();
    return null;
  }

  const posVbo = gl.createBuffer();
  const normalVbo = gl.createBuffer();
  const texVbo = gl.createBuffer();
  const ibo = gl.createBuffer();

  gl.bindBuffer(gl.ARRAY_BUFFER, texVbo);
  gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);

  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);

  const quadVbo = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, quadVbo);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,
     3, -1,
    -1,  3
  ]), gl.STATIC_DRAW);

  let fbo = null, fboTex = null, fboW = 1, fboH = 1;

  function setupFBO() {
    if (!fbo) {
      fbo = gl.createFramebuffer();
      fboTex = gl.createTexture();
    }
    fboW = Math.max(1, Math.floor(canvas.width / 8));
    fboH = Math.max(1, Math.floor(canvas.height / 8));

    gl.bindTexture(gl.TEXTURE_2D, fboTex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, fboW, fboH, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, fboTex, 0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }

  let hasTexture = 0.0;
  const clothTexture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, clothTexture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([15, 15, 15, 255]));

  function loadTexture(src) {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = function() {
      gl.bindTexture(gl.TEXTURE_2D, clothTexture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);

      function isPow2(v) { return (v & (v - 1)) === 0; }
      let uploadSource = img;
      if (!isPow2(img.width) || !isPow2(img.height)) {
        const offCanvas = document.createElement('canvas');
        offCanvas.width = 1024;
        offCanvas.height = 1024;
        const ctx = offCanvas.getContext('2d');
        ctx.fillStyle = '#090a0d';
        ctx.fillRect(0, 0, 1024, 1024);
        ctx.drawImage(img, 0, 0, 1024, 1024);
        uploadSource = offCanvas;
      }

      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, uploadSource);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.generateMipmap(gl.TEXTURE_2D);

      const ext = gl.getExtension('EXT_texture_filter_anisotropic') ||
                  gl.getExtension('WEBKIT_EXT_texture_filter_anisotropic') ||
                  gl.getExtension('MOZ_EXT_texture_filter_anisotropic');
      if (ext) {
        const maxAniso = gl.getParameter(ext.MAX_TEXTURE_MAX_ANISOTROPY_EXT);
        gl.texParameterf(gl.TEXTURE_2D, ext.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(8, maxAniso));
      }

      hasTexture = 1.0;
      const stillImg = hero.querySelector('.hero__still');
      if (stillImg) stillImg.src = src;
      renderFrame();
    };
    img.src = src;
  }

  if (initialSrc) {
    loadTexture(initialSrc);
  }

  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  function updateView() {
    const rect = hero.getBoundingClientRect();
    heroWidth = rect.width;
    heroHeight = rect.height;
    if (heroHeight === 0 || heroWidth === 0) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const pixelW = Math.round(heroWidth * dpr);
    const pixelH = Math.round(heroHeight * dpr);

    if (canvas.width !== pixelW || canvas.height !== pixelH) {
      canvas.width = pixelW;
      canvas.height = pixelH;
      setupFBO();
    }

    aspectRatio = heroWidth / heroHeight;
    const isWide = heroWidth >= 1100 && aspectRatio >= 1.25;

    cx = 0.5;
    cy = (aspectRatio < 0.85) ? 0.44 : 0.47;
    zoom = Math.min(1.0, 0.82 * aspectRatio / (CW * 1.08), 0.78 / CH);
  }

  window.addEventListener('resize', updateView);
  if (typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(updateView).observe(hero);
  }
  updateView();

  function computeNormals() {
    for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
        const i = row * COLS + col;
        let dx_x, dx_y, dx_z;
        let dy_x, dy_y, dy_z;

        if (col === 0) {
          const iRight = row * COLS + 1;
          dx_x = pos[3 * iRight] - pos[3 * i];
          dx_y = pos[3 * iRight + 1] - pos[3 * i + 1];
          dx_z = pos[3 * iRight + 2] - pos[3 * i + 2];
        } else if (col === COLS - 1) {
          const iLeft = row * COLS + (COLS - 2);
          dx_x = pos[3 * i] - pos[3 * iLeft];
          dx_y = pos[3 * i + 1] - pos[3 * iLeft + 1];
          dx_z = pos[3 * i + 2] - pos[3 * iLeft + 2];
        } else {
          const iRight = row * COLS + (col + 1);
          const iLeft = row * COLS + (col - 1);
          dx_x = 0.5 * (pos[3 * iRight] - pos[3 * iLeft]);
          dx_y = 0.5 * (pos[3 * iRight + 1] - pos[3 * iLeft + 1]);
          dx_z = 0.5 * (pos[3 * iRight + 2] - pos[3 * iLeft + 2]);
        }

        if (row === 0) {
          const iUp = 1 * COLS + col;
          dy_x = pos[3 * iUp] - pos[3 * i];
          dy_y = pos[3 * iUp + 1] - pos[3 * i + 1];
          dy_z = pos[3 * iUp + 2] - pos[3 * i + 2];
        } else if (row === ROWS - 1) {
          const iDown = (ROWS - 2) * COLS + col;
          dy_x = pos[3 * i] - pos[3 * iDown];
          dy_y = pos[3 * i + 1] - pos[3 * iDown + 1];
          dy_z = pos[3 * i + 2] - pos[3 * iDown + 2];
        } else {
          const iUp = (row + 1) * COLS + col;
          const iDown = (row - 1) * COLS + col;
          dy_x = 0.5 * (pos[3 * iUp] - pos[3 * iDown]);
          dy_y = 0.5 * (pos[3 * iUp + 1] - pos[3 * iDown + 1]);
          dy_z = 0.5 * (pos[3 * iUp + 2] - pos[3 * iDown + 2]);
        }

        let nx = dx_y * dy_z - dx_z * dy_y;
        let ny = dx_z * dy_x - dx_x * dy_z;
        let nz = dx_x * dy_y - dx_y * dy_x;
        const len = Math.hypot(nx, ny, nz);
        if (len > 1e-6) {
          nx /= len; ny /= len; nz /= len;
        }
        normals[3 * i] = nx;
        normals[3 * i + 1] = ny;
        normals[3 * i + 2] = nz;
      }
    }
  }

  function projectPoint(i) {
    const px = pos[3 * i], py = pos[3 * i + 1], pz = pos[3 * i + 2];
    const qx = R0[0] * px + R0[1] * py + R0[2] * pz;
    const qy = R1[0] * px + R1[1] * py + R1[2] * pz;
    const qz = R2[0] * px + R2[1] * py + R2[2] * pz;
    const scale = CAM / Math.max(CAM - qz, 0.001);
    return { qx, qy, qz, projX: qx * scale, projY: qy * scale };
  }

  function findBestPoint(ptrX, ptrY) {
    let bestIdx = -1;
    let bestScore = Infinity;
    let bestProj = null;
    const threshold = grabRadius / zoom;
    for (let i = 0; i < NUM_POINTS; i++) {
      const p = projectPoint(i);
      const dist = Math.hypot(p.projX - ptrX, p.projY - ptrY);
      if (dist <= threshold) {
        const score = dist - 0.08 * p.qz;
        if (score < bestScore) {
          bestScore = score;
          bestIdx = i;
          bestProj = p;
        }
      }
    }
    return { idx: bestIdx, proj: bestProj };
  }

  canvas.addEventListener('pointerdown', function(e) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    const rect = canvas.getBoundingClientRect();
    const ptrX = ((e.clientX - rect.left) / rect.width - cx) * aspectRatio / zoom;
    const ptrY = (cy - (e.clientY - rect.top) / rect.height) / zoom;
    const found = findBestPoint(ptrX, ptrY);
    if (found.idx !== -1) {
      activePointerId = e.pointerId;
      isHeld = true;
      grabbedIdx = found.idx;
      grabRemDepth = found.proj.qz;
      grabOffsetX = found.proj.projX - ptrX;
      grabOffsetY = found.proj.projY - ptrY;
      currentPointer.clientX = e.clientX;
      currentPointer.clientY = e.clientY;

      for (let i = 0; i < NUM_POINTS; i++) {
        if (i === leftPinIdx || i === rightPinIdx) {
          carryWeights[i] = 0;
        } else if (i === grabbedIdx) {
          carryWeights[i] = 1;
        } else {
          const d = Math.hypot(flatX[i] - flatX[grabbedIdx], flatY[i] - flatY[grabbedIdx]) / (carryRadius * CH);
          carryWeights[i] = d < 1.0 ? Math.pow(1.0 - d * d, 2) : 0.0;
        }
      }

      canvas.classList.add('is-held');
      try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
    }
  });

  canvas.addEventListener('pointermove', function(e) {
    const rect = canvas.getBoundingClientRect();
    if (isHeld && e.pointerId === activePointerId) {
      currentPointer.clientX = e.clientX;
      currentPointer.clientY = e.clientY;
    } else if (!isHeld) {
      const ptrX = ((e.clientX - rect.left) / rect.width - cx) * aspectRatio / zoom;
      const ptrY = (cy - (e.clientY - rect.top) / rect.height) / zoom;
      const found = findBestPoint(ptrX, ptrY);
      if (found.idx !== -1) {
        canvas.classList.add('is-over');
      } else {
        canvas.classList.remove('is-over');
      }
    }
  });

  function releasePointer(e) {
    if (isHeld && (e.pointerId === activePointerId || e.type === 'lostpointercapture')) {
      isHeld = false;
      activePointerId = null;
      canvas.classList.remove('is-held');
      carryWeights.fill(0);
    }
  }

  canvas.addEventListener('pointerup', releasePointer);
  canvas.addEventListener('pointercancel', releasePointer);
  canvas.addEventListener('lostpointercapture', releasePointer);

  canvas.addEventListener('touchstart', function(e) {
    if (e.touches.length > 0) {
      const tTouch = e.touches[0];
      const rect = canvas.getBoundingClientRect();
      const ptrX = ((tTouch.clientX - rect.left) / rect.width - cx) * aspectRatio / zoom;
      const ptrY = (cy - (tTouch.clientY - rect.top) / rect.height) / zoom;
      const found = findBestPoint(ptrX, ptrY);
      if (found.idx !== -1) e.preventDefault();
    }
  }, { passive: false });

  window.addEventListener('touchmove', function(e) {
    if (isHeld) e.preventDefault();
  }, { passive: false });

  let timeT = 0;
  let sweepDirection = 1;

  function subStep(h) {
    timeT += h;
    const damp = Math.exp(-(0.15 + 5.85 * damping) * h);
    const gust = 0.6 + 0.4 * Math.sin(0.37 * timeT) * Math.sin(0.23 * timeT + 1.0);
    const wind = reducedMotionQuery.matches ? 0 : flutter * 2.4 * gust * (gravity / 2.6);

    if (isHeld && grabbedIdx !== -1) {
      const rect = canvas.getBoundingClientRect();
      const currPtrX = ((currentPointer.clientX - rect.left) / rect.width - cx) * aspectRatio / zoom;
      const currPtrY = (cy - (currentPointer.clientY - rect.top) / rect.height) / zoom;

      const targetScreenX = currPtrX + grabOffsetX;
      const targetScreenY = currPtrY + grabOffsetY;
      const targetQz = grabRemDepth;
      const scale = CAM / Math.max(CAM - targetQz, 0.001);
      const targetQx = targetScreenX / scale;
      const targetQy = targetScreenY / scale;

      let targetX = invR0[0] * targetQx + invR1[0] * targetQy + invR2[0] * targetQz;
      let targetY = invR0[1] * targetQx + invR1[1] * targetQy + invR2[1] * targetQz;
      let targetZ = invR0[2] * targetQx + invR1[2] * targetQy + invR2[2] * targetQz;

      const dL = Math.hypot(targetX - pinL[0], targetY - pinL[1], targetZ - pinL[2]);
      if (dL > maxDistLeft[grabbedIdx]) {
        const sL = maxDistLeft[grabbedIdx] / dL;
        targetX = pinL[0] + (targetX - pinL[0]) * sL;
        targetY = pinL[1] + (targetY - pinL[1]) * sL;
        targetZ = pinL[2] + (targetZ - pinL[2]) * sL;
      }
      const dR = Math.hypot(targetX - pinR[0], targetY - pinR[1], targetZ - pinR[2]);
      if (dR > maxDistRight[grabbedIdx]) {
        const sR = maxDistRight[grabbedIdx] / dR;
        targetX = pinR[0] + (targetX - pinR[0]) * sR;
        targetY = pinR[1] + (targetY - pinR[1]) * sR;
        targetZ = pinR[2] + (targetZ - pinR[2]) * sR;
      }

      const deltaX = targetX - pos[3 * grabbedIdx];
      const deltaY = targetY - pos[3 * grabbedIdx + 1];
      const deltaZ = targetZ - pos[3 * grabbedIdx + 2];

      for (let i = 0; i < NUM_POINTS; i++) {
        if (i === leftPinIdx || i === rightPinIdx) continue;
        const w = carryWeights[i];
        if (w >= 0.98) {
          pos[3 * i] += deltaX; pos[3 * i + 1] += deltaY; pos[3 * i + 2] += deltaZ;
          prev[3 * i] += deltaX; prev[3 * i + 1] += deltaY; prev[3 * i + 2] += deltaZ;
        } else if (w > 0.0) {
          pos[3 * i] += w * deltaX; pos[3 * i + 1] += w * deltaY; pos[3 * i + 2] += w * deltaZ;
          prev[3 * i] += w * deltaX; prev[3 * i + 1] += w * deltaY; prev[3 * i + 2] += w * deltaZ;
        }
      }
    }

    const maxSpdH = maxSpeed * h;
    for (let row = 0; row < ROWS; row++) {
      const v = row / (ROWS - 1);
      for (let col = 0; col < COLS; col++) {
        const i = row * COLS + col;
        if (i === leftPinIdx || i === rightPinIdx) continue;
        if (isHeld && carryWeights[i] >= 0.98) continue;

        const u = col / (COLS - 1);
        const s1 = Math.sin(9.1 * u - 3.7 * v + 3.1 * timeT);
        const s2 = Math.sin(6.3 * u + 7.9 * v - 2.3 * timeT + 1.3);
        const s3 = Math.sin(2.9 * u + 1.7 * timeT + 0.8 * Math.sin(0.5 * timeT)) * Math.cos(2.3 * v - 0.9 * timeT);

        const accelX = wind * 0.25 * Math.sin(3.3 * v + 1.1 * timeT + u);
        const accelY = wind * 0.1 * s2 - gravity;
        const accelZ = wind * (0.45 * s1 + 0.35 * s2 + 0.3 * s3);

        let vx = (pos[3 * i] - prev[3 * i]) * damp + accelX * h * h;
        let vy = (pos[3 * i + 1] - prev[3 * i + 1]) * damp + accelY * h * h;
        let vz = (pos[3 * i + 2] - prev[3 * i + 2]) * damp + accelZ * h * h;

        const spd = Math.hypot(vx, vy, vz);
        if (spd > maxSpdH) {
          const f = maxSpdH / spd;
          vx *= f; vy *= f; vz *= f;
        }

        prev[3 * i] = pos[3 * i]; prev[3 * i + 1] = pos[3 * i + 1]; prev[3 * i + 2] = pos[3 * i + 2];
        pos[3 * i] += vx; pos[3 * i + 1] += vy; pos[3 * i + 2] += vz;
      }
    }

    pos[3 * leftPinIdx] = pinL[0]; pos[3 * leftPinIdx + 1] = pinL[1]; pos[3 * leftPinIdx + 2] = pinL[2];
    pos[3 * rightPinIdx] = pinR[0]; pos[3 * rightPinIdx + 1] = pinR[1]; pos[3 * rightPinIdx + 2] = pinR[2];

    if (sweepDirection === 1) {
      for (let k = 0; k < linkCount; k++) relaxLink(k);
    } else {
      for (let k = linkCount - 1; k >= 0; k--) relaxLink(k);
    }
    sweepDirection = -sweepDirection;

    for (let i = 0; i < NUM_POINTS; i++) {
      if (i === leftPinIdx || i === rightPinIdx) continue;

      let dxL = pos[3 * i] - pinL[0], dyL = pos[3 * i + 1] - pinL[1], dzL = pos[3 * i + 2] - pinL[2];
      let dL = Math.hypot(dxL, dyL, dzL);
      if (dL > maxDistLeft[i]) {
        const sL = maxDistLeft[i] / dL;
        pos[3 * i] = pinL[0] + dxL * sL; pos[3 * i + 1] = pinL[1] + dyL * sL; pos[3 * i + 2] = pinL[2] + dzL * sL;
      }

      let dxR = pos[3 * i] - pinR[0], dyR = pos[3 * i + 1] - pinR[1], dzR = pos[3 * i + 2] - pinR[2];
      let dR = Math.hypot(dxR, dyR, dzR);
      if (dR > maxDistRight[i]) {
        const sR = maxDistRight[i] / dR;
        pos[3 * i] = pinR[0] + dxR * sR; pos[3 * i + 1] = pinR[1] + dyR * sR; pos[3 * i + 2] = pinR[2] + dzR * sR;
      }
    }
  }

  function relaxLink(k) {
    const i = linksAArray[k];
    const j = linksBArray[k];

    const wA = (i === leftPinIdx || i === rightPinIdx || (isHeld && carryWeights[i] >= 0.98)) ? 0 : 1;
    const wB = (j === leftPinIdx || j === rightPinIdx || (isHeld && carryWeights[j] >= 0.98)) ? 0 : 1;
    const wTotal = wA + wB;
    if (wTotal === 0) return;

    const dx = pos[3 * j] - pos[3 * i];
    const dy = pos[3 * j + 1] - pos[3 * i + 1];
    const dz = pos[3 * j + 2] - pos[3 * i + 2];
    const dist = Math.hypot(dx, dy, dz);
    if (dist < 1e-6) return;

    const factor = (dist - linkRestDistArray[k]) / dist * linkStiffArray[k] / wTotal;
    const corrX = dx * factor, corrY = dy * factor, corrZ = dz * factor;

    if (wA > 0) {
      pos[3 * i] += corrX * wA; pos[3 * i + 1] += corrY * wA; pos[3 * i + 2] += corrZ * wA;
    }
    if (wB > 0) {
      pos[3 * j] -= corrX * wB; pos[3 * j + 1] -= corrY * wB; pos[3 * j + 2] -= corrZ * wB;
    }
  }

  const initialDamping = damping;
  damping = 1.0;
  for (let s = 0; s < 360; s++) subStep(1 / 240);
  damping = initialDamping;

  const mat3R = new Float32Array([
    R0[0], R1[0], R2[0],
    R0[1], R1[1], R2[1],
    R0[2], R1[2], R2[2]
  ]);

  function renderFrame() {
    computeNormals();

    gl.bindBuffer(gl.ARRAY_BUFFER, posVbo);
    gl.bufferData(gl.ARRAY_BUFFER, pos, gl.DYNAMIC_DRAW);

    gl.bindBuffer(gl.ARRAY_BUFFER, normalVbo);
    gl.bufferData(gl.ARRAY_BUFFER, normals, gl.DYNAMIC_DRAW);

    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.viewport(0, 0, fboW, fboH);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.BLEND);

    gl.useProgram(shadowSilProgram);
    gl.uniformMatrix3fv(gl.getUniformLocation(shadowSilProgram, 'u_R'), false, mat3R);
    gl.uniform1f(gl.getUniformLocation(shadowSilProgram, 'u_cam'), CAM);
    gl.uniform1f(gl.getUniformLocation(shadowSilProgram, 'u_zoom'), zoom);
    gl.uniform1f(gl.getUniformLocation(shadowSilProgram, 'u_aspectRatio'), aspectRatio);
    gl.uniform2f(gl.getUniformLocation(shadowSilProgram, 'u_c'), cx, cy);

    const silPosLoc = gl.getAttribLocation(shadowSilProgram, 'a_position');
    gl.bindBuffer(gl.ARRAY_BUFFER, posVbo);
    gl.enableVertexAttribArray(silPosLoc);
    gl.vertexAttribPointer(silPosLoc, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
    gl.drawElements(gl.TRIANGLES, indices.length, gl.UNSIGNED_SHORT, 0);

    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.disable(gl.DEPTH_TEST);

    gl.useProgram(shadowBlurProgram);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, fboTex);
    gl.uniform1i(gl.getUniformLocation(shadowBlurProgram, 'u_shadowTex'), 0);

    const texelX = 1.0 / fboW, texelY = 1.0 / fboH;
    const spacingScale = 0.9 + 1.5 * zoom * heroHeight / 724.0;
    gl.uniform2f(gl.getUniformLocation(shadowBlurProgram, 'u_spacing'), texelX * spacingScale, texelY * spacingScale);
    gl.uniform2f(gl.getUniformLocation(shadowBlurProgram, 'u_shift'), -0.012 * zoom / aspectRatio, -0.045 * zoom);

    const blurPosLoc = gl.getAttribLocation(shadowBlurProgram, 'a_pos');
    gl.bindBuffer(gl.ARRAY_BUFFER, quadVbo);
    gl.enableVertexAttribArray(blurPosLoc);
    gl.vertexAttribPointer(blurPosLoc, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.disable(gl.BLEND);
    gl.disable(gl.CULL_FACE);

    gl.useProgram(clothProgram);
    gl.uniformMatrix3fv(gl.getUniformLocation(clothProgram, 'u_R'), false, mat3R);
    gl.uniform1f(gl.getUniformLocation(clothProgram, 'u_cam'), CAM);
    gl.uniform1f(gl.getUniformLocation(clothProgram, 'u_zoom'), zoom);
    gl.uniform1f(gl.getUniformLocation(clothProgram, 'u_aspectRatio'), aspectRatio);
    gl.uniform2f(gl.getUniformLocation(clothProgram, 'u_c'), cx, cy);

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, clothTexture);
    gl.uniform1i(gl.getUniformLocation(clothProgram, 'u_texture'), 0);
    gl.uniform1f(gl.getUniformLocation(clothProgram, 'u_hasTexture'), hasTexture);

    const clothPosLoc = gl.getAttribLocation(clothProgram, 'a_position');
    gl.bindBuffer(gl.ARRAY_BUFFER, posVbo);
    gl.enableVertexAttribArray(clothPosLoc);
    gl.vertexAttribPointer(clothPosLoc, 3, gl.FLOAT, false, 0, 0);

    const clothNormLoc = gl.getAttribLocation(clothProgram, 'a_normal');
    gl.bindBuffer(gl.ARRAY_BUFFER, normalVbo);
    gl.enableVertexAttribArray(clothNormLoc);
    gl.vertexAttribPointer(clothNormLoc, 3, gl.FLOAT, false, 0, 0);

    const clothTexLoc = gl.getAttribLocation(clothProgram, 'a_texCoord');
    gl.bindBuffer(gl.ARRAY_BUFFER, texVbo);
    gl.enableVertexAttribArray(clothTexLoc);
    gl.vertexAttribPointer(clothTexLoc, 2, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
    gl.drawElements(gl.TRIANGLES, indices.length, gl.UNSIGNED_SHORT, 0);
  }

  let isHeroVisible = true;
  let isDocVisible = !document.hidden;
  let isLoopRunning = false;
  let lastTime = performance.now();

  function updateLoopState() {
    const shouldRun = isHeroVisible && isDocVisible && !hero.classList.contains('no-cloth');
    if (shouldRun && !isLoopRunning) {
      isLoopRunning = true;
      lastTime = performance.now();
      requestAnimationFrame(loop);
    } else if (!shouldRun && isLoopRunning) {
      isLoopRunning = false;
    }
  }

  function loop(now) {
    if (!isLoopRunning) return;
    const elapsed = (now - lastTime) * 0.001;
    lastTime = now;

    const dt = Math.min(elapsed, 1 / 30);
    const h = dt / steps;

    for (let s = 0; s < steps; s++) {
      subStep(h);
    }

    renderFrame();

    if (isLoopRunning) {
      requestAnimationFrame(loop);
    }
  }

  const observer = new IntersectionObserver(function(entries) {
    for (let i = 0; i < entries.length; i++) {
      isHeroVisible = entries[i].isIntersecting;
      updateLoopState();
    }
  });
  observer.observe(hero);

  document.addEventListener('visibilitychange', function() {
    isDocVisible = !document.hidden;
    updateLoopState();
  });

  renderFrame();
  updateLoopState();

  return {
    setTexture: function(src) {
      loadTexture(src);
      // Gentle vibration to show it changed
      for (let i = 0; i < NUM_POINTS; i++) {
        if (i !== leftPinIdx && i !== rightPinIdx) {
          pos[3 * i + 2] += (Math.random() - 0.5) * 0.06;
        }
      }
    }
  };
};
