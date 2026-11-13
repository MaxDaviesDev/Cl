// Backdrop: the world changes as you climb. Seven zones blend into each other:
// Sunset Skies → Aurora Heights → Low Orbit → Neon Nebula → Spiral Galaxy →
// Event Horizon → Hyperspace (endless).
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const ZONE_H = 2400;                      // camera pixels climbed per zone
  const BLEND_START = 0.7;                  // start fading into the next zone at 70%

  let W = 0, H = 0, DPR = 1;
  let stars = [], clouds = [], blobs = [], flares = [], warp = [], swirl = [];
  let citySprite = null, cloudSprite = null, galaxySprite = null;
  let shooting = null, lastT = 0, dt = 0;

  // ── helpers ───────────────────────────────────────────────
  const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const smooth = (t) => t * t * (3 - 2 * t);
  const mod = (a, n) => ((a % n) + n) % n;
  function seeded(seed) { return () => (seed = (seed * 16807) % 2147483647) / 2147483647; }
  function hsl2rgb(h, s, l) {
    h = mod(h, 360) / 360;
    const f = (n) => { const k = (n + h * 12) % 12; const a = s * Math.min(l, 1 - l); return Math.round(255 * (l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)))); };
    return [f(0), f(8), f(4)];
  }
  function offscreen(w, h) {
    const c = document.createElement('canvas');
    c.width = Math.ceil(w * DPR); c.height = Math.ceil(h * DPR);
    const g = c.getContext('2d'); g.scale(DPR, DPR);
    return [c, g];
  }

  // ── sprites (built on resize) ────────────────────────────
  function buildCity() {
    const h = 190;
    const [c, g] = offscreen(W, h);
    const r = seeded(11);
    const layer = (color, scale, windows) => {
      let x = -10;
      while (x < W + 10) {
        const bw = 18 + r() * 42, bh = h * (0.2 + r() * 0.6) * scale;
        g.fillStyle = color;
        g.fillRect(x, h - bh, bw, bh);
        if (r() < 0.25) g.fillRect(x + bw / 2 - 1, h - bh - 14, 2, 14);   // antenna
        if (windows) {
          for (let wy = h - bh + 6; wy < h - 6; wy += 9) {
            for (let wx = x + 4; wx < x + bw - 5; wx += 7) {
              if (r() < 0.28) { g.fillStyle = r() < 0.8 ? 'rgba(255,214,140,.85)' : 'rgba(130,230,255,.85)'; g.fillRect(wx, wy, 3, 4); }
            }
          }
        }
        x += bw + r() * 5;
      }
    };
    layer('#4a2360', 0.75, false);
    layer('#1a0c2e', 1, true);
    citySprite = c;
  }

  function buildCloud() {
    const [c, g] = offscreen(260, 110);
    const r = seeded(3);
    for (let i = 0; i < 9; i++) {
      const x = 40 + r() * 180, y = 45 + r() * 35, rad = 25 + r() * 35;
      const gr = g.createRadialGradient(x, y, 0, x, y, rad);
      gr.addColorStop(0, 'rgba(255,200,225,.55)');
      gr.addColorStop(1, 'rgba(255,170,210,0)');
      g.fillStyle = gr; g.beginPath(); g.arc(x, y, rad, 0, TAU); g.fill();
    }
    cloudSprite = c;
  }

  function buildGalaxy() {
    const S = 420, R = S / 2;
    const [c, g] = offscreen(S, S);
    const r = seeded(42);
    const gauss = () => (r() + r() + r() - 1.5);
    const core = g.createRadialGradient(R, R, 0, R, R, R * 0.35);
    core.addColorStop(0, 'rgba(255,250,230,1)');
    core.addColorStop(0.25, 'rgba(255,200,120,.7)');
    core.addColorStop(1, 'rgba(255,140,80,0)');
    g.fillStyle = core; g.fillRect(0, 0, S, S);
    for (let i = 0; i < 3500; i++) {
      const arm = i % 3;
      const d = Math.pow(r(), 0.65);
      const a = arm * TAU / 3 + d * 5 + gauss() * 0.45 * (1 - d * 0.4);
      const rr = d * R * 0.95 + gauss() * 6;
      const x = R + Math.cos(a) * rr, y = R + Math.sin(a) * rr;
      const hue = 40 + d * 180 + gauss() * 20;
      g.fillStyle = `hsla(${hue},90%,${70 + r() * 25}%,${0.35 + r() * 0.6})`;
      const s = 0.5 + r() * 1.4;
      g.fillRect(x, y, s, s);
    }
    galaxySprite = c;
  }

  function resize(w, h, dpr) {
    W = w; H = h; DPR = dpr || 1;
    const r = seeded(99);
    stars = [];
    const n = Math.round((W * H) / 3200);
    for (let i = 0; i < n; i++) stars.push({ x: r() * W, y: r() * H, z: 0.05 + r() * 0.35, s: 0.5 + r() * 1.4, tw: r() * TAU, hue: r() < 0.15 ? 200 + r() * 160 : 0 });
    clouds = [];
    for (let i = 0; i < 8; i++) clouds.push({ x: r() * (W + 300), y: r() * H * 1.5, sc: 0.6 + r() * 0.9, sp: 6 + r() * 14 });
    const hues = [285, 320, 200, 250, 335, 185, 300, 220];
    blobs = hues.map((hue) => ({ x: r() * W, y: r() * H * 1.6, rad: 140 + r() * 220, hue }));
    flares = [];
    for (let i = 0; i < 7; i++) flares.push({ x: r() * W, y: r() * H * 1.6, s: 6 + r() * 10, hue: 180 + r() * 160 });
    warp = [];
    for (let i = 0; i < 110; i++) warp.push({ a: r() * TAU, d: 5 + r() * Math.max(W, H), sp: 0.8 + r() * 1.6 });
    swirl = [];
    for (let i = 0; i < 40; i++) swirl.push({ a: r() * TAU, d: r(), sp: 0.5 + r() });
    buildCity(); buildCloud(); buildGalaxy();
  }

  // ── zone layers ───────────────────────────────────────────
  // Each gets (ctx, local, t, w): local = pixels climbed relative to the
  // zone's start (negative while fading in), w = blend weight 0..1.

  function drawSunset(ctx, local, t, w) {
    // Retro striped sun
    const cx = W / 2, cy = H * 0.6 + local * 0.35, r = Math.min(W, H) * 0.24;
    ctx.globalAlpha = w;
    const glow = ctx.createRadialGradient(cx, cy, r * 0.5, cx, cy, r * 2.4);
    glow.addColorStop(0, 'rgba(255,120,110,.45)'); glow.addColorStop(1, 'rgba(255,90,120,0)');
    ctx.fillStyle = glow; ctx.fillRect(cx - r * 2.4, cy - r * 2.4, r * 4.8, r * 4.8);
    ctx.save();
    ctx.beginPath();
    ctx.rect(cx - r, cy - r, r * 2, r * 1.1);
    let y = cy + r * 0.1, gap = 2, band = 10;
    const shift = (t * 8) % (band + gap);
    y -= shift;
    while (y < cy + r) { ctx.rect(cx - r, Math.max(y, cy + r * 0.1), r * 2, band); y += band + gap; gap += 1.6; band = Math.max(3, band - 0.6); }
    ctx.clip();
    const sg = ctx.createLinearGradient(0, cy - r, 0, cy + r);
    sg.addColorStop(0, '#fff3a0'); sg.addColorStop(0.5, '#ffb057'); sg.addColorStop(1, '#ff3d8b');
    ctx.fillStyle = sg; ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.fill();
    ctx.restore();

    // Drifting clouds
    for (const c of clouds) {
      const cyy = mod(c.y + local * 0.5, H * 1.5) - H * 0.25;
      const cxx = mod(c.x + t * c.sp, W + 300) - 150;
      ctx.globalAlpha = w * 0.8;
      ctx.drawImage(cloudSprite, cxx - 130 * c.sc, cyy - 55 * c.sc, 260 * c.sc, 110 * c.sc);
    }

    // City skyline sinking away below you
    const ch = 190, top = H - ch + 6 + local * 0.7;
    if (top < H) {
      ctx.globalAlpha = w;
      ctx.drawImage(citySprite, 0, top, W, ch);
      ctx.fillStyle = '#1a0c2e';
      if (top + ch < H) ctx.fillRect(0, top + ch - 1, W, H - top - ch + 1);
    }
  }

  function drawAurora(ctx, local, t, w) {
    ctx.globalCompositeOperation = 'lighter';
    const ribbons = [
      { hue: 150, base: 0.22, amp: 38, h: 150 },
      { hue: 172, base: 0.36, amp: 30, h: 110 },
      { hue: 285, base: 0.12, amp: 46, h: 120 },
    ];
    ribbons.forEach((rb, k) => {
      const baseY = H * rb.base + local * 0.16;
      const yAt = (x) => baseY + Math.sin(x * 0.008 + t * 0.5 + k * 2) * rb.amp + Math.sin(x * 0.021 - t * 0.8 + k) * rb.amp * 0.4;
      const hAt = (x) => rb.h * (0.55 + 0.45 * Math.sin(x * 0.03 + t * 1.2 + k * 3));
      // curtain of vertical rays that fade upward and shimmer sideways
      const gr = ctx.createLinearGradient(0, baseY - rb.amp - rb.h, 0, baseY + rb.amp);
      gr.addColorStop(0, `hsla(${rb.hue + 50},100%,60%,0)`);
      gr.addColorStop(0.55, `hsla(${rb.hue + 20},100%,60%,.22)`);
      gr.addColorStop(0.85, `hsla(${rb.hue},100%,65%,.55)`);
      gr.addColorStop(1, `hsla(${rb.hue},100%,75%,.7)`);
      ctx.strokeStyle = gr;
      ctx.lineWidth = 3.2;
      for (let x = -6; x <= W + 6; x += 3) {
        const y = yAt(x);
        ctx.globalAlpha = w * (0.35 + 0.65 * Math.pow(0.5 + 0.5 * Math.sin(x * 0.09 + t * 2.4 + k * 5 + Math.sin(x * 0.013 + t) * 3), 2));
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - hAt(x)); ctx.stroke();
      }
      ctx.globalAlpha = w;
      ctx.strokeStyle = `hsla(${rb.hue},100%,80%,.35)`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let x = -10; x <= W + 10; x += 8) ctx.lineTo(x, yAt(x));
      ctx.stroke();
    });
    ctx.globalCompositeOperation = 'source-over';
  }

  function drawOrbit(ctx, local, t, w) {
    // Moon
    const mx = W * 0.8, my = H * 0.18 + local * 0.12, mr = 26;
    ctx.globalAlpha = w;
    const mg = ctx.createRadialGradient(mx - 8, my - 8, 2, mx, my, mr);
    mg.addColorStop(0, '#f2f2f7'); mg.addColorStop(1, '#7c7c92');
    ctx.fillStyle = mg; ctx.beginPath(); ctx.arc(mx, my, mr, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(70,70,90,.45)';
    [[-8, -4, 6], [7, 6, 4], [4, -11, 3], [-3, 11, 3.5]].forEach(([dx, dy, rr]) => { ctx.beginPath(); ctx.arc(mx + dx, my + dy, rr, 0, TAU); ctx.fill(); });

    // Satellite with blinking light
    const sx = mod(t * 28, W + 120) - 60, sy = H * 0.34 + local * 0.28 + Math.sin(t * 0.3) * 20;
    ctx.fillStyle = '#9fb3c8'; ctx.fillRect(sx - 2, sy - 2, 4, 4);
    ctx.fillStyle = '#4c7fb8'; ctx.fillRect(sx - 12, sy - 1, 8, 2); ctx.fillRect(sx + 4, sy - 1, 8, 2);
    if (Math.sin(t * 6) > 0.6) { ctx.fillStyle = '#ff4d4d'; ctx.beginPath(); ctx.arc(sx, sy - 4, 1.6, 0, TAU); ctx.fill(); }

    // Earth's curved limb rising from below, then sinking away
    const R = Math.max(W, H) * 1.15;
    const cx = W / 2, cy = H + R - H * 0.2 + local * 0.24;
    if (cy - R < H + 60) {
      ctx.save();
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.clip();
      const eg = ctx.createLinearGradient(0, cy - R, 0, cy - R + H * 0.5);
      eg.addColorStop(0, '#2f8fe0'); eg.addColorStop(0.4, '#0b3f8a'); eg.addColorStop(1, '#020c26');
      ctx.fillStyle = eg; ctx.fillRect(cx - R, cy - R, R * 2, H);
      // continents rolling past
      const r = seeded(5);
      for (let i = 0; i < 14; i++) {
        const lx = mod(r() * W * 2 + t * 10, W * 2) - W * 0.5;
        const ly = cy - R + 25 + r() * H * 0.35;
        ctx.fillStyle = r() < 0.7 ? 'rgba(60,150,90,.55)' : 'rgba(170,140,90,.5)';
        ctx.beginPath(); ctx.ellipse(lx, ly, 30 + r() * 70, 12 + r() * 26, r() * 0.6, 0, TAU); ctx.fill();
      }
      // cloud swirls
      for (let i = 0; i < 10; i++) {
        const lx = mod(r() * W * 2 + t * 16, W * 2) - W * 0.5;
        const ly = cy - R + 15 + r() * H * 0.3;
        ctx.fillStyle = 'rgba(255,255,255,.22)';
        ctx.beginPath(); ctx.ellipse(lx, ly, 40 + r() * 60, 6 + r() * 8, 0, 0, TAU); ctx.fill();
      }
      ctx.restore();
      // atmosphere glow
      ctx.save();
      ctx.shadowColor = '#5fd0ff'; ctx.shadowBlur = 40;
      ctx.strokeStyle = 'rgba(110,200,255,.55)'; ctx.lineWidth = 6;
      ctx.beginPath(); ctx.arc(cx, cy, R + 2, 0, TAU); ctx.stroke();
      ctx.restore();
      const ag = ctx.createRadialGradient(cx, cy, R, cx, cy, R + 70);
      ag.addColorStop(0, 'rgba(90,190,255,.35)'); ag.addColorStop(1, 'rgba(90,190,255,0)');
      ctx.globalAlpha = w; ctx.fillStyle = ag;
      ctx.beginPath(); ctx.arc(cx, cy, R + 70, 0, TAU); ctx.fill();
    }
  }

  function drawNebula(ctx, local, t, w) {
    ctx.globalCompositeOperation = 'lighter';
    for (const b of blobs) {
      const y = mod(b.y + local * 0.22, H * 1.6) - H * 0.3;
      const x = b.x + Math.sin(t * 0.15 + b.hue) * 25;
      const hue = b.hue + Math.sin(t * 0.2 + b.x) * 18;
      const g = ctx.createRadialGradient(x, y, 0, x, y, b.rad);
      g.addColorStop(0, `hsla(${hue},95%,58%,.30)`);
      g.addColorStop(0.5, `hsla(${hue + 20},90%,45%,.12)`);
      g.addColorStop(1, `hsla(${hue},90%,40%,0)`);
      ctx.globalAlpha = w; ctx.fillStyle = g;
      ctx.fillRect(x - b.rad, y - b.rad, b.rad * 2, b.rad * 2);
    }
    // young stars with lens flares
    for (const f of flares) {
      const y = mod(f.y + local * 0.3, H * 1.6) - H * 0.3;
      const s = f.s * (0.8 + 0.2 * Math.sin(t * 3 + f.x));
      ctx.globalAlpha = w * 0.9;
      ctx.strokeStyle = `hsla(${f.hue},100%,85%,.8)`; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(f.x - s * 2, y); ctx.lineTo(f.x + s * 2, y); ctx.moveTo(f.x, y - s * 2); ctx.lineTo(f.x, y + s * 2); ctx.stroke();
      const g = ctx.createRadialGradient(f.x, y, 0, f.x, y, s);
      g.addColorStop(0, 'rgba(255,255,255,.95)'); g.addColorStop(1, `hsla(${f.hue},100%,70%,0)`);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(f.x, y, s, 0, TAU); ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  function drawGalaxy(ctx, local, t, w) {
    ctx.globalCompositeOperation = 'lighter';
    const S = Math.min(W, H) * 1.25;
    const cx = W / 2, cy = H * 0.42 + local * 0.2;
    ctx.save();
    ctx.globalAlpha = w;
    ctx.translate(cx, cy); ctx.rotate(-0.35); ctx.scale(1, 0.48); ctx.rotate(t * 0.05);
    ctx.drawImage(galaxySprite, -S / 2, -S / 2, S, S);
    ctx.restore();
    // a distant companion galaxy
    ctx.save();
    ctx.globalAlpha = w * 0.6;
    ctx.translate(W * 0.18, cy - H * 0.32); ctx.rotate(0.6); ctx.scale(1, 0.35); ctx.rotate(-t * 0.08);
    ctx.drawImage(galaxySprite, -S * 0.13, -S * 0.13, S * 0.26, S * 0.26);
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';
  }

  function drawBlackHole(ctx, local, t, w) {
    const cx = W / 2, cy = H * 0.42 + local * 0.2;
    const rh = Math.min(W, H) * 0.12;
    ctx.globalAlpha = w;
    const glow = ctx.createRadialGradient(cx, cy, rh, cx, cy, rh * 6);
    glow.addColorStop(0, 'rgba(255,150,60,.35)'); glow.addColorStop(1, 'rgba(255,90,40,0)');
    ctx.fillStyle = glow; ctx.fillRect(cx - rh * 6, cy - rh * 6, rh * 12, rh * 12);

    const disk = (from, to) => {
      ctx.save();
      ctx.translate(cx, cy); ctx.scale(1, 0.24);
      ctx.globalCompositeOperation = 'lighter';
      const N = 48;
      for (let i = 0; i < N; i++) {
        const a0 = from + (to - from) * (i / N), a1 = from + (to - from) * ((i + 1) / N);
        const b = 0.5 + 0.5 * Math.sin(a0 * 3 - t * 2.2);
        for (let ring = 0; ring < 3; ring++) {
          ctx.strokeStyle = `hsla(${25 + ring * 12 + b * 15},100%,${45 + b * 25 + ring * 5}%,${(0.55 - ring * 0.13) * w})`;
          ctx.lineWidth = rh * (0.55 - ring * 0.12);
          ctx.beginPath(); ctx.arc(0, 0, rh * (1.7 + ring * 0.55), a0, a1 + 0.02); ctx.stroke();
        }
      }
      // infalling sparks
      for (const s of swirl) {
        const a = s.a + t * s.sp * (2 - s.d);
        if (mod(a, TAU) < from || mod(a, TAU) > to) continue;
        const rr = rh * (1.3 + s.d * 2.2);
        ctx.fillStyle = `rgba(255,230,190,${0.8 * w})`;
        ctx.fillRect(Math.cos(a) * rr, Math.sin(a) * rr, 2.5, 2.5 / 0.24);
      }
      ctx.restore();
    };

    // lensed halo bending over the top
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.strokeStyle = `rgba(255,170,90,${0.55 * w})`;
    ctx.lineWidth = rh * 0.35;
    ctx.beginPath(); ctx.ellipse(cx, cy, rh * 1.45, rh * 1.3, 0, 0, TAU); ctx.stroke();
    ctx.restore();

    disk(Math.PI, TAU);                       // far side
    ctx.globalAlpha = w;
    ctx.fillStyle = '#000';
    ctx.beginPath(); ctx.arc(cx, cy, rh, 0, TAU); ctx.fill();
    ctx.save();
    ctx.shadowColor = '#ffb060'; ctx.shadowBlur = 18;
    ctx.strokeStyle = `rgba(255,225,180,${0.9 * w})`; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(cx, cy, rh + 1.5, 0, TAU); ctx.stroke();
    ctx.restore();
    disk(0, Math.PI);                         // near side
  }

  function drawHyper(ctx, local, t, w) {
    const cx = W / 2, cy = H * 0.45;
    const h0 = (t * 25) % 360;
    ctx.globalCompositeOperation = 'lighter';
    const pulse = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) * 0.5);
    pulse.addColorStop(0, `hsla(${h0 + 180},100%,70%,${0.18 + 0.08 * Math.sin(t * 4)})`);
    pulse.addColorStop(1, `hsla(${h0 + 180},100%,50%,0)`);
    ctx.globalAlpha = w; ctx.fillStyle = pulse; ctx.fillRect(0, 0, W, H);
    const maxD = Math.hypot(W, H) * 0.6;
    ctx.lineCap = 'round';
    for (const s of warp) {
      s.d *= 1 + dt * s.sp * 1.4;
      if (s.d > maxD) { s.d = 4 + Math.random() * 30; s.a = Math.random() * TAU; }
      const len = s.d * 0.22;
      const x0 = cx + Math.cos(s.a) * s.d, y0 = cy + Math.sin(s.a) * s.d;
      const x1 = cx + Math.cos(s.a) * (s.d + len), y1 = cy + Math.sin(s.a) * (s.d + len);
      ctx.strokeStyle = `hsla(${h0 + s.a * 40},100%,72%,${Math.min(1, s.d / 140) * w})`;
      ctx.lineWidth = 0.5 + s.d / 160;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  const hyperSky = (t) => { const h = (t * 25) % 360; return [hsl2rgb(h, 0.7, 0.05), hsl2rgb(h + 40, 0.7, 0.09), hsl2rgb(h + 90, 0.8, 0.15)]; };

  const ZONES = [
    { name: 'Sunset Skies',   sky: ['#1d1650', '#6a2c78', '#ff7e63'], stars: 0.15, draw: drawSunset },
    { name: 'Aurora Heights', sky: ['#020617', '#051c34', '#0c3a4e'], stars: 0.75, draw: drawAurora },
    { name: 'Low Orbit',      sky: ['#00010a', '#020615', '#07142e'], stars: 1,    draw: drawOrbit },
    { name: 'Neon Nebula',    sky: ['#0b0218', '#1a0630', '#2a0a3e'], stars: 0.9,  draw: drawNebula },
    { name: 'Spiral Galaxy',  sky: ['#06040d', '#110a1b', '#1d1024'], stars: 1,    draw: drawGalaxy },
    { name: 'Event Horizon',  sky: ['#000000', '#040108', '#0d0512'], stars: 0.6,  draw: drawBlackHole },
    { name: 'Hyperspace',     sky: null,                              stars: 0.3,  draw: drawHyper },
  ].map((z) => (z.sky ? Object.assign(z, { skyRGB: z.sky.map(hex) }) : z));

  function weights(alt) {
    const pos = Math.max(0, alt) / ZONE_H;
    const last = ZONES.length - 1;
    const i = Math.floor(pos);
    if (i >= last) return [{ i: last, w: 1, local: alt - last * ZONE_H }];
    const t = smooth(Math.max(0, (pos - i - BLEND_START) / (1 - BLEND_START)));
    const out = [{ i, w: 1 - t, local: alt - i * ZONE_H }];
    if (t > 0.001) out.push({ i: i + 1, w: t, local: alt - (i + 1) * ZONE_H });
    return out;
  }

  function zoneIndex(alt) {
    return weights(alt).reduce((a, b) => (b.w > a.w ? b : a)).i;
  }

  function draw(ctx, alt, t) {
    dt = Math.min(0.05, Math.max(0, t - lastT)); lastT = t;
    const ws = weights(alt);

    // Sky gradient (blended between zones)
    const cols = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    let starA = 0;
    for (const z of ws) {
      const zone = ZONES[z.i];
      const s = zone.skyRGB || hyperSky(t);
      for (let k = 0; k < 3; k++) for (let j = 0; j < 3; j++) cols[k][j] += s[k][j] * z.w;
      starA += zone.stars * z.w;
    }
    const g = ctx.createLinearGradient(0, 0, 0, H);
    cols.forEach((c, k) => g.addColorStop(k / 2, `rgb(${c.map(Math.round).join(',')})`));
    ctx.globalAlpha = 1;
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // Stars
    for (const s of stars) {
      const y = mod(s.y + alt * s.z, H);
      ctx.globalAlpha = starA * (0.35 + 0.65 * Math.abs(Math.sin(t * 1.5 + s.tw)));
      ctx.fillStyle = s.hue ? `hsl(${s.hue},80%,80%)` : '#fff';
      ctx.fillRect(s.x, y, s.s, s.s);
    }

    // Shooting stars
    if (!shooting && starA > 0.5 && Math.random() < dt * 0.25) {
      const fromLeft = Math.random() < 0.5;
      shooting = { x: fromLeft ? -20 : W + 20, y: Math.random() * H * 0.5, vx: (fromLeft ? 1 : -1) * (500 + Math.random() * 300), vy: 160 + Math.random() * 120, life: 0 };
    }
    if (shooting) {
      const s = shooting;
      s.x += s.vx * dt; s.y += s.vy * dt; s.life += dt;
      const gr = ctx.createLinearGradient(s.x, s.y, s.x - s.vx * 0.12, s.y - s.vy * 0.12);
      gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.globalAlpha = starA; ctx.strokeStyle = gr; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(s.x - s.vx * 0.12, s.y - s.vy * 0.12); ctx.stroke();
      if (s.life > 2.5) shooting = null;
    }

    // Zone set pieces
    for (const z of ws) {
      ctx.save();
      ZONES[z.i].draw(ctx, z.local, t, z.w);
      ctx.restore();
    }
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';
  }

  window.Backdrop = { ZONES, ZONE_H, resize, draw, zoneIndex };
})();
