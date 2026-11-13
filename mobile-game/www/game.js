// Orbit Hop — a one-tap orbit-jumping arcade game.
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const TAU = Math.PI * 2;
  const rand = (a, b) => a + Math.random() * (b - a);
  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  // ── Persistence ───────────────────────────────────────────
  const SAVE_KEY = 'orbithop.save.v1';
  const save = Object.assign(
    { best: 0, coins: 0, skin: 'comet', owned: ['comet'], lastDaily: null, streak: 0, games: 0, sound: true },
    (() => { try { return JSON.parse(localStorage.getItem(SAVE_KEY)) || {}; } catch (e) { return {}; } })()
  );
  const persist = () => { try { localStorage.setItem(SAVE_KEY, JSON.stringify(save)); } catch (e) {} };

  const SKINS = [
    { id: 'comet',  name: 'Comet',  cost: 0,    color: '#7df9ff' },
    { id: 'sun',    name: 'Sun',    cost: 100,  color: '#ffcc4d' },
    { id: 'mint',   name: 'Mint',   cost: 200,  color: '#5dffa8' },
    { id: 'rose',   name: 'Rose',   cost: 350,  color: '#ff5ea8' },
    { id: 'plasma', name: 'Plasma', cost: 500,  color: '#b07dff' },
    { id: 'ember',  name: 'Ember',  cost: 750,  color: '#ff6a3d' },
    { id: 'ice',    name: 'Ice',    cost: 1000, color: '#e6f6ff' },
    { id: 'void',   name: 'Void',   cost: 1500, color: '#1b1b2f', outline: '#b07dff' },
    { id: 'prism',  name: 'Prism',  cost: 2500, color: 'rainbow' },
  ];
  const skinOf = (id) => SKINS.find((s) => s.id === id) || SKINS[0];

  // ── Audio ─────────────────────────────────────────────────
  let actx = null, muted = false;
  function beep(freq, dur, type = 'sine', vol = 0.15, slide = 0) {
    if (!save.sound || muted) return;
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const t = actx.currentTime;
      const o = actx.createOscillator(), g = actx.createGain();
      o.type = type;
      o.frequency.setValueAtTime(freq, t);
      if (slide) o.frequency.exponentialRampToValueAtTime(Math.max(30, freq + slide), t + dur);
      g.gain.setValueAtTime(vol, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(actx.destination);
      o.start(t); o.stop(t + dur);
    } catch (e) {}
  }
  const sfx = {
    launch: () => beep(320, 0.12, 'triangle', 0.12, 280),
    land: (c) => beep(520 + c * 70, 0.14, 'sine', 0.16),
    perfect: (c) => { beep(660 + c * 60, 0.1, 'square', 0.07); setTimeout(() => beep(990 + c * 60, 0.16, 'square', 0.07), 70); },
    coin: () => { beep(1320, 0.06, 'square', 0.06); setTimeout(() => beep(1760, 0.1, 'square', 0.06), 50); },
    die: () => beep(220, 0.5, 'sawtooth', 0.14, -180),
    best: () => [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, 0.18, 'triangle', 0.12), i * 110)),
    click: () => beep(700, 0.05, 'sine', 0.08),
  };
  const vibrate = (ms) => { try { if (save.sound && navigator.vibrate) navigator.vibrate(ms); } catch (e) {} };

  // ── Canvas ────────────────────────────────────────────────
  const canvas = $('game');
  const ctx = canvas.getContext('2d');
  let W = 0, H = 0, DPR = 1;
  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 3);
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    makeStars();
  }

  let stars = [];
  function makeStars() {
    stars = [];
    const n = Math.round((W * H) / 3500);
    for (let i = 0; i < n; i++) {
      stars.push({ x: Math.random() * W, y: Math.random() * H, z: rand(0.05, 0.4), s: rand(0.5, 1.8), tw: rand(0, TAU) });
    }
  }

  // ── Game state ────────────────────────────────────────────
  const FLY_SPEED = 560;
  const CAPTURE_SCALE = 1.5;     // pickup range as a multiple of the orbit radius
  // Spin speed ramps up with every planet you land on, then caps.
  const SPIN_BASE = 2.0;         // radians/second on the first planet
  const SPIN_MAX = 4.2;          // top speed
  const SPIN_RAMP_HOPS = 45;     // landings needed to reach top speed
  const spinSpeed = () => lerp(SPIN_BASE, SPIN_MAX, clamp(hops / SPIN_RAMP_HOPS, 0, 1));
  let state = 'menu';          // menu | play | dying | over
  let planets = [], coins = [], particles = [], floaters = [], trail = [];
  let player, camY = 0, score = 0, runCoins = 0, combo = 0, shake = 0, revived = false;
  let hops = 0, planetCount = 0, flyTime = 0, dyingT = 0, time = 0, firstTap = true;

  function makePlanet(y, idx) {
    const d = clamp(idx / 60, 0, 1);
    const orbitR = clamp(lerp(60, 40, d) + rand(-6, 6), 34, 70);
    const r = orbitR * rand(0.36, 0.5);
    const margin = orbitR + 12;
    let moving = null;
    let x = rand(margin, W - margin);
    if (idx > 8 && Math.random() < lerp(0.15, 0.55, d)) {
      const maxAmp = Math.max(0, (W - 2 * margin) / 2);
      const amp = Math.min(rand(30, 120), maxAmp);
      if (amp > 15) {
        x = rand(margin + amp, W - margin - amp);
        moving = { amp, freq: rand(0.45, lerp(0.8, 1.3, d)), phase: rand(0, TAU) };
      }
    }
    const spd = rand(0.92, 1.08) * (Math.random() < 0.5 ? -1 : 1);   // per-planet variation × global spin speed
    return { x, baseX: x, y, r, orbitR, spd, moving, hue: Math.floor(rand(0, 360)), idx, pulse: 0 };
  }

  function addPlanet() {
    const prev = planets[planets.length - 1];
    const d = clamp(planetCount / 60, 0, 1);
    const gap = rand(lerp(170, 215, d), lerp(225, 285, d));
    const p = makePlanet(prev.y - gap, planetCount++);
    planets.push(p);
    // Coin between planets
    if (Math.random() < 0.55) {
      const t = rand(0.35, 0.65);
      coins.push({ x: lerp(prev.baseX, p.baseX, t) + rand(-40, 40), y: lerp(prev.y, p.y, t), spin: rand(0, TAU) });
    }
  }

  function resetRun() {
    planets = []; coins = []; particles = []; floaters = []; trail = [];
    score = 0; runCoins = 0; combo = 0; shake = 0; revived = false; hops = 0; planetCount = 0; firstTap = true;
    const first = makePlanet(H * 0.7, planetCount++);
    first.x = first.baseX = W / 2; first.moving = null; first.spd = 2.0;
    planets.push(first);
    while (planets.length < 8) addPlanet();
    player = { mode: 'orbit', planet: first, angle: -Math.PI / 2, r: first.orbitR, dir: 1, x: 0, y: 0, vx: 0, vy: 0 };
    camY = first.y - H * 0.7;
    updateHud();
  }

  // ── Input ─────────────────────────────────────────────────
  function tap() {
    if (state !== 'play' || player.mode !== 'orbit') return;
    if (firstTap) { firstTap = false; $('tapHint').classList.add('hidden'); }
    const a = player.angle, s = player.dir;
    player.vx = -Math.sin(a) * s * FLY_SPEED;
    player.vy = Math.cos(a) * s * FLY_SPEED;
    player.mode = 'fly';
    flyTime = 0;
    sfx.launch();
    burst(player.x, player.y, skinColor(), 6, 120);
  }
  canvas.addEventListener('pointerdown', (e) => { e.preventDefault(); tap(); });
  window.addEventListener('keydown', (e) => { if (e.code === 'Space' || e.code === 'ArrowUp') { e.preventDefault(); tap(); } });

  // ── Update ────────────────────────────────────────────────
  function planetX(p) { return p.moving ? p.baseX + Math.sin(time * p.moving.freq * TAU / 2 + p.moving.phase) * p.moving.amp : p.baseX; }

  function update(dt) {
    time += dt;
    for (const p of planets) { p.x = planetX(p); p.pulse = Math.max(0, p.pulse - dt * 2.5); }

    if (state === 'play') {
      if (player.mode === 'orbit') {
        const p = player.planet;
        player.angle += spinSpeed() * Math.abs(p.spd) * player.dir * dt;
        player.r = lerp(player.r, p.orbitR, Math.min(1, dt * 6));
        player.x = p.x + Math.cos(player.angle) * player.r;
        player.y = p.y + Math.sin(player.angle) * player.r;
      } else {
        flyTime += dt;
        player.x += player.vx * dt;
        player.y += player.vy * dt;
        checkCapture();
        if (player.mode === 'fly' &&
            (player.x < -30 || player.x > W + 30 || player.y > camY + H + 40 || player.y < camY - 80 || flyTime > 2.6)) {
          die();
        }
      }

      // Coins
      for (let i = coins.length - 1; i >= 0; i--) {
        const c = coins[i];
        if (Math.hypot(c.x - player.x, c.y - player.y) < 26) {
          coins.splice(i, 1);
          runCoins++;
          sfx.coin();
          burst(c.x, c.y, '#ffd34d', 10, 160);
          floaters.push({ x: c.x, y: c.y, text: '+1', color: '#ffd34d', t: 0 });
          updateHud();
        }
      }

      trail.push({ x: player.x, y: player.y });
      if (trail.length > 22) trail.shift();

      // Camera follows the current planet
      const target = (player.mode === 'orbit' ? player.planet.y : player.y) - H * 0.68;
      if (player.mode === 'orbit' || target < camY) camY = lerp(camY, target, Math.min(1, dt * 3));

      // Spawn / cull
      while (planets.length < 8 || planets[planets.length - 1].y > camY - H) addPlanet();
      planets = planets.filter((p) => p.y < camY + H + 200 || p === player.planet);
      coins = coins.filter((c) => c.y < camY + H + 100);
    } else if (state === 'dying') {
      dyingT += dt;
      if (dyingT > 0.9) showGameOver();
    }

    // Effects
    for (let i = particles.length - 1; i >= 0; i--) {
      const q = particles[i];
      q.t += dt; q.x += q.vx * dt; q.y += q.vy * dt; q.vx *= 0.96; q.vy *= 0.96;
      if (q.t > q.life) particles.splice(i, 1);
    }
    for (let i = floaters.length - 1; i >= 0; i--) {
      floaters[i].t += dt; floaters[i].y -= 40 * dt;
      if (floaters[i].t > 1) floaters.splice(i, 1);
    }
    shake = Math.max(0, shake - dt * 30);
  }

  function checkCapture() {
    const cur = player.planet;
    for (const p of planets) {
      if (p === cur || p.idx < cur.idx || p.idx > cur.idx + 3) continue;
      const rx = player.x - p.x, ry = player.y - p.y;
      const dist = Math.hypot(rx, ry);
      if (dist > p.orbitR * CAPTURE_SCALE) continue;

      // Captured!
      const cross = rx * player.vy - ry * player.vx;
      const miss = Math.abs(cross) / FLY_SPEED;          // closest-approach distance to the centre
      const perfect = miss < p.orbitR * 0.3;
      const skipped = p.idx - cur.idx;

      player.mode = 'orbit';
      player.planet = p;
      player.dir = cross >= 0 ? 1 : -1;
      player.angle = Math.atan2(ry, rx);
      player.r = dist;
      p.pulse = 1;

      let pts = skipped;
      if (perfect) {
        combo++;
        pts += combo;
        floaters.push({ x: p.x, y: p.y - p.orbitR - 10, text: combo > 1 ? `PERFECT ×${combo}` : 'PERFECT!', color: '#ffd34d', t: 0, big: true });
        sfx.perfect(Math.min(combo, 10));
        vibrate(25);
        burst(p.x, p.y, '#ffd34d', 18 + combo * 2, 240);
      } else {
        combo = 0;
        sfx.land(0);
        vibrate(10);
        burst(player.x, player.y, `hsl(${p.hue},90%,65%)`, 8, 140);
      }
      if (skipped > 1) floaters.push({ x: p.x, y: p.y + p.orbitR + 20, text: `SKIP +${skipped}`, color: '#7df9ff', t: 0 });
      score += pts;
      const tierBefore = Math.floor(clamp(hops / SPIN_RAMP_HOPS, 0, 1) * 4);
      hops += skipped;
      const tierAfter = Math.floor(clamp(hops / SPIN_RAMP_HOPS, 0, 1) * 4);
      if (tierAfter > tierBefore) {
        floaters.push({ x: W / 2, y: camY + H * 0.4, text: tierAfter >= 4 ? 'MAX SPEED!' : 'SPEED UP!', color: '#ff5ea8', t: 0, big: true });
        beep(440, 0.25, 'sawtooth', 0.08, 440);
      }
      updateHud(true);
      return;
    }
  }

  function burst(x, y, color, n, speed) {
    for (let i = 0; i < n; i++) {
      const a = rand(0, TAU), v = rand(speed * 0.3, speed);
      particles.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, t: 0, life: rand(0.35, 0.8), color, s: rand(1.5, 3.5) });
    }
  }

  // ── Render ────────────────────────────────────────────────
  function skinColor(t = time) {
    const s = skinOf(save.skin);
    return s.color === 'rainbow' ? `hsl(${(t * 180) % 360},100%,65%)` : s.color;
  }

  function render() {
    // Background
    const g = ctx.createLinearGradient(0, 0, 0, H);
    const hueShift = (-camY / 40) % 360;
    g.addColorStop(0, `hsl(${(235 + hueShift * 0.15) % 360},55%,8%)`);
    g.addColorStop(1, `hsl(${(260 + hueShift * 0.15) % 360},50%,5%)`);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    for (const s of stars) {
      const y = (((s.y - camY * s.z) % H) + H) % H;
      ctx.globalAlpha = 0.4 + 0.6 * Math.abs(Math.sin(time * 1.5 + s.tw));
      ctx.fillStyle = '#fff';
      ctx.fillRect(s.x, y, s.s, s.s);
    }
    ctx.globalAlpha = 1;

    ctx.save();
    const sx = shake ? rand(-shake, shake) : 0, sy = shake ? rand(-shake, shake) : 0;
    ctx.translate(sx, -camY + sy);

    // Planets
    const cur = player && player.planet;
    for (const p of planets) {
      const isNext = cur && p.idx === cur.idx + 1;
      // pickup zone
      ctx.fillStyle = `hsla(${p.hue},90%,65%,${isNext ? 0.07 : 0.03})`;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.orbitR * CAPTURE_SCALE, 0, TAU); ctx.fill();
      // orbit ring
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.orbitR + p.pulse * 10, 0, TAU);
      ctx.setLineDash(isNext ? [6, 6] : [3, 7]);
      ctx.lineDashOffset = -time * 20 * Math.sign(p.spd);
      ctx.strokeStyle = isNext ? `hsla(${p.hue},100%,75%,${0.55 + 0.25 * Math.sin(time * 6)})` : `hsla(${p.hue},80%,70%,.25)`;
      ctx.lineWidth = isNext ? 2 : 1.5;
      ctx.stroke();
      ctx.setLineDash([]);
      // body
      ctx.shadowColor = `hsl(${p.hue},90%,60%)`;
      ctx.shadowBlur = 24 + p.pulse * 30;
      const bg = ctx.createRadialGradient(p.x - p.r * 0.35, p.y - p.r * 0.35, p.r * 0.1, p.x, p.y, p.r);
      bg.addColorStop(0, `hsl(${p.hue},90%,78%)`);
      bg.addColorStop(1, `hsl(${(p.hue + 30) % 360},70%,38%)`);
      ctx.fillStyle = bg;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r * (1 + p.pulse * 0.15), 0, TAU); ctx.fill();
      ctx.shadowBlur = 0;
      if (p.moving) {
        ctx.strokeStyle = `hsla(${p.hue},80%,70%,.15)`;
        ctx.beginPath(); ctx.moveTo(p.baseX - p.moving.amp, p.y); ctx.lineTo(p.baseX + p.moving.amp, p.y); ctx.stroke();
      }
    }

    // Coins
    for (const c of coins) {
      const sc = Math.abs(Math.cos(time * 4 + c.spin));
      ctx.shadowColor = '#ffd34d'; ctx.shadowBlur = 14;
      ctx.fillStyle = '#ffd34d';
      ctx.beginPath(); ctx.ellipse(c.x, c.y + Math.sin(time * 3 + c.spin) * 4, 9 * Math.max(sc, 0.15), 9, 0, 0, TAU); ctx.fill();
      ctx.shadowBlur = 0;
    }

    // Aim guide while orbiting (first few planets help new players)
    if (state === 'play' && player.mode === 'orbit' && score < 3) {
      const a = player.angle, s = player.dir;
      const dx = -Math.sin(a) * s, dy = Math.cos(a) * s;
      ctx.strokeStyle = 'rgba(255,255,255,.18)';
      ctx.setLineDash([4, 8]);
      ctx.beginPath(); ctx.moveTo(player.x, player.y); ctx.lineTo(player.x + dx * 160, player.y + dy * 160); ctx.stroke();
      ctx.setLineDash([]);
    }

    // Player + trail
    if (player && state !== 'dying' && state !== 'over') {
      const col = skinColor();
      for (let i = 1; i < trail.length; i++) {
        const t = i / trail.length;
        ctx.strokeStyle = skinOf(save.skin).color === 'rainbow' ? `hsla(${(time * 180 - (trail.length - i) * 12) % 360},100%,65%,${t * 0.8})` : col;
        ctx.globalAlpha = skinOf(save.skin).color === 'rainbow' ? 1 : t * 0.7;
        ctx.lineWidth = t * 10;
        ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(trail[i - 1].x, trail[i - 1].y); ctx.lineTo(trail[i].x, trail[i].y); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      const sk = skinOf(save.skin);
      ctx.shadowColor = sk.outline || col; ctx.shadowBlur = 22;
      ctx.fillStyle = col;
      ctx.beginPath(); ctx.arc(player.x, player.y, 9, 0, TAU); ctx.fill();
      if (sk.outline) { ctx.strokeStyle = sk.outline; ctx.lineWidth = 2; ctx.stroke(); }
      ctx.shadowBlur = 0;
      ctx.fillStyle = 'rgba(255,255,255,.85)';
      ctx.beginPath(); ctx.arc(player.x - 3, player.y - 3, 2.5, 0, TAU); ctx.fill();
    }

    // Particles
    for (const q of particles) {
      ctx.globalAlpha = 1 - q.t / q.life;
      ctx.fillStyle = q.color;
      ctx.beginPath(); ctx.arc(q.x, q.y, q.s, 0, TAU); ctx.fill();
    }
    ctx.globalAlpha = 1;

    // Floating text
    ctx.textAlign = 'center';
    for (const f of floaters) {
      ctx.globalAlpha = 1 - f.t;
      ctx.fillStyle = f.color;
      ctx.font = `900 ${f.big ? 22 + (1 - f.t) * 6 : 16}px system-ui, sans-serif`;
      ctx.fillText(f.text, f.x, f.y);
    }
    ctx.globalAlpha = 1;
    ctx.restore();
  }

  // ── Loop ──────────────────────────────────────────────────
  let last = performance.now(), paused = false;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (!paused) { update(dt); render(); }
    requestAnimationFrame(frame);
  }

  // ── Flow ──────────────────────────────────────────────────
  const screens = ['menu', 'over', 'shop', 'daily'];
  function show(id) {
    screens.forEach((s) => $(s).classList.toggle('hidden', s !== id));
    $('hud').classList.toggle('hidden', id !== null);
  }

  function updateHud(bump) {
    $('score').textContent = score;
    $('hudCoinCount').textContent = save.coins + runCoins;
    $('combo').textContent = combo > 1 ? `COMBO ×${combo}` : '';
    if (bump) {
      const el = $('score');
      el.animate([{ transform: 'scale(1.35)' }, { transform: 'scale(1)' }], { duration: 180, easing: 'ease-out' });
    }
  }

  function startGame() {
    resetRun();
    state = 'play';
    show(null);
    $('tapHint').classList.remove('hidden');
    Ads.hideBanner();
  }

  function die() {
    state = 'dying';
    dyingT = 0;
    shake = 12;
    combo = 0;
    sfx.die();
    vibrate([40, 30, 60]);
    burst(player.x, player.y, skinColor(), 40, 320);
    $('tapHint').classList.add('hidden');
  }

  let lastRunWasBest = false;
  function showGameOver() {
    state = 'over';
    const isBest = score > save.best;
    if (isBest) { save.best = score; sfx.best(); }
    lastRunWasBest = isBest;
    save.coins += runCoins;
    save.games++;
    persist();

    $('overScore').textContent = score;
    $('overBest').textContent = save.best;
    $('overCoins').textContent = runCoins;
    $('newBest').classList.toggle('hidden', !isBest);
    $('continueBtn').classList.toggle('hidden', revived || score < 3 || !Ads.rewardedAvailable());
    $('doubleBtn').classList.toggle('hidden', runCoins < 3 || !Ads.rewardedAvailable());
    show('over');
    Ads.showBanner();
  }

  function revive() {
    revived = true;
    // Undo the coins banked at game over — the run continues.
    save.coins -= runCoins; save.games--;
    persist();
    const p = player.planet;
    player.mode = 'orbit';
    player.r = p.orbitR;
    trail = [];
    // Clear out anything weird and put the camera back
    camY = p.y - H * 0.68;
    state = 'play';
    show(null);
    $('tapHint').classList.remove('hidden');
    firstTap = true;
    Ads.hideBanner();
    updateHud();
  }

  function toast(msg) {
    const t = $('toast');
    t.textContent = msg;
    t.classList.remove('hidden');
    clearTimeout(toast._t);
    toast._t = setTimeout(() => t.classList.add('hidden'), 1800);
  }

  // ── Menu / shop / daily ───────────────────────────────────
  function refreshMenu() {
    $('menuBest').textContent = save.best;
    $('menuCoins').textContent = save.coins;
    $('soundBtn').textContent = save.sound ? '🔊' : '🔇';
    $('dailyBtn').hidden = save.lastDaily === today();
  }

  function goMenu() {
    state = 'menu';
    resetRun();
    refreshMenu();
    show('menu');
    Ads.showBanner();
  }

  function today(offset = 0) {
    const d = new Date(Date.now() + offset * 864e5);
    return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
  }
  function dailyInfo() {
    const streak = save.lastDaily === today(-1) ? Math.min(save.streak + 1, 7) : 1;
    return { streak, amount: 25 * streak };
  }
  function openDaily() {
    const { streak, amount } = dailyInfo();
    $('streakDay').textContent = streak;
    $('dailyAmount').textContent = amount;
    $('dailyTriple').classList.toggle('hidden', !Ads.rewardedAvailable());
    show('daily');
  }
  function claimDaily(mult) {
    const { streak, amount } = dailyInfo();
    save.streak = streak;
    save.lastDaily = today();
    save.coins += amount * mult;
    persist();
    sfx.coin();
    toast(`+${amount * mult} coins!`);
    goMenu();
  }

  function renderShop() {
    $('shopCoins').textContent = save.coins;
    const grid = $('skinGrid');
    grid.innerHTML = '';
    for (const s of SKINS) {
      const owned = save.owned.includes(s.id);
      const b = document.createElement('button');
      b.className = 'skin' + (save.skin === s.id ? ' equipped' : '') + (owned ? '' : ' locked');
      const bg = s.color === 'rainbow'
        ? 'conic-gradient(red,orange,yellow,lime,cyan,blue,magenta,red)'
        : s.color;
      b.innerHTML = `<span class="ball" style="background:${bg};box-shadow:0 0 14px ${s.outline || (s.color === 'rainbow' ? '#fff' : s.color)};${s.outline ? 'border:2px solid ' + s.outline : ''}"></span>
        <span>${s.name}</span>
        ${owned ? `<span>${save.skin === s.id ? 'EQUIPPED' : 'Tap to use'}</span>` : `<span class="price"><span class="coin-ic"></span>${s.cost}</span>`}`;
      b.onclick = () => {
        if (owned) { save.skin = s.id; sfx.click(); }
        else if (save.coins >= s.cost) { save.coins -= s.cost; save.owned.push(s.id); save.skin = s.id; sfx.best(); toast(`Unlocked ${s.name}!`); }
        else { toast(`Need ${s.cost - save.coins} more coins`); return; }
        persist(); renderShop();
      };
      grid.appendChild(b);
    }
    $('freeCoinsBtn').classList.toggle('hidden', !Ads.rewardedAvailable());
  }

  async function rewarded(name, onReward) {
    sfx.click();
    const ok = await Ads.showRewarded(name);
    if (ok) onReward(); else toast('Ad not available — try again soon');
  }

  // Buttons
  const on = (id, f) => $(id).addEventListener('click', (e) => { e.stopPropagation(); f(); });
  on('playBtn', () => { sfx.click(); startGame(); });
  on('retryBtn', async () => { sfx.click(); await Ads.gameOverBreak(); startGame(); });
  on('homeBtn', () => { sfx.click(); goMenu(); });
  on('continueBtn', () => rewarded('continue', revive));
  on('doubleBtn', () => rewarded('double-coins', () => {
    save.coins += runCoins; persist();
    $('overCoins').textContent = runCoins * 2;
    $('doubleBtn').classList.add('hidden');
    sfx.coin(); toast(`+${runCoins} bonus coins!`);
  }));
  on('shopBtn', () => { sfx.click(); renderShop(); show('shop'); });
  on('shopBack', () => { sfx.click(); goMenu(); });
  on('freeCoinsBtn', () => rewarded('free-coins', () => { save.coins += 40; persist(); renderShop(); sfx.coin(); toast('+40 coins!'); }));
  on('dailyBtn', () => { sfx.click(); openDaily(); });
  on('dailyClaim', () => claimDaily(1));
  on('dailyTriple', () => rewarded('daily-x3', () => claimDaily(3)));
  on('soundBtn', () => { save.sound = !save.sound; persist(); refreshMenu(); sfx.click(); });

  // Pause the game & audio while an ad is on screen or the app is backgrounded
  Ads.on('pause', () => { paused = true; muted = true; });
  Ads.on('resume', () => { paused = false; muted = false; last = performance.now(); });
  document.addEventListener('visibilitychange', () => { last = performance.now(); });

  // ── Boot ──────────────────────────────────────────────────
  window.addEventListener('resize', resize);
  resize();
  goMenu();
  requestAnimationFrame(frame);
  Ads.init().then(() => { if (state === 'menu') { Ads.hideBanner(); Ads.showBanner(); refreshMenu(); } });

  // Debug hook for automated tests
  window.__orbit = { get state() { return state; }, get score() { return score; }, get player() { return player; }, get planets() { return planets; }, tap };
})();
