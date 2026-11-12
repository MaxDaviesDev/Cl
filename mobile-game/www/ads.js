// Ads abstraction: AdMob on native (Capacitor), H5 Games Ads on web,
// and a mock ad in plain browsers so every flow can be tested.
(function () {
  'use strict';
  const cfg = window.ADS_CONFIG || {};
  const cap = window.Capacitor;
  const isNative = !!(cap && cap.isNativePlatform && cap.isNativePlatform());
  const platform = isNative ? cap.getPlatform() : 'web';
  const AdMob = isNative && cap.Plugins ? cap.Plugins.AdMob : null;
  const ids = AdMob ? (cfg.admob[platform] || cfg.admob.android) : null;

  let mode = 'none';           // 'admob' | 'h5' | 'mock' | 'none'
  let interstitialReady = false;
  let rewardedReady = false;
  let bannerShown = false;
  let lastInterstitial = 0;
  let gameOversSinceAd = 0;
  let gameOversTotal = 0;
  let h5Ready = false;

  const listeners = { pause: [], resume: [] };
  const emit = (t) => listeners[t].forEach((f) => { try { f(); } catch (e) {} });
  const setBannerHeight = (px) =>
    document.documentElement.style.setProperty('--banner-h', Math.round(px || 0) + 'px');

  // ── AdMob (native) ─────────────────────────────────────────
  async function initAdMob() {
    try {
      await AdMob.initialize({
        initializeForTesting: !!cfg.testMode,
        requestTrackingAuthorization: true,
      });
    } catch (e) { console.warn('AdMob init failed', e); return false; }

    // GDPR / UMP consent
    try {
      const info = await AdMob.requestConsentInfo();
      if (info && info.isConsentFormAvailable && info.status === 'REQUIRED') {
        await AdMob.showConsentForm();
      }
    } catch (e) { console.warn('Consent flow failed', e); }

    try {
      AdMob.addListener('bannerAdSizeChanged', (s) => setBannerHeight(bannerShown ? s.height : 0));
      AdMob.addListener('onRewardedVideoAdReward', () => { rewardFlag = true; });
    } catch (e) {}

    prepareInterstitial();
    prepareRewarded();
    return true;
  }

  async function prepareInterstitial() {
    interstitialReady = false;
    try {
      await AdMob.prepareInterstitial({ adId: ids.interstitial, isTesting: !!cfg.testMode });
      interstitialReady = true;
    } catch (e) { setTimeout(prepareInterstitial, 30000); }
  }

  let rewardFlag = false;
  async function prepareRewarded() {
    rewardedReady = false;
    try {
      await AdMob.prepareRewardVideoAd({ adId: ids.rewarded, isTesting: !!cfg.testMode });
      rewardedReady = true;
    } catch (e) { setTimeout(prepareRewarded, 30000); }
  }

  // ── H5 Games Ads (web) ─────────────────────────────────────
  function initH5() {
    window.adsbygoogle = window.adsbygoogle || [];
    window.adBreak = window.adConfig = function (o) { window.adsbygoogle.push(o); };
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + cfg.h5.client;
    s.setAttribute('data-ad-client', cfg.h5.client);
    s.setAttribute('crossorigin', 'anonymous');
    if (cfg.testMode) s.setAttribute('data-adbreak-test', 'on');
    s.setAttribute('data-ad-frequency-hint', cfg.interstitialMinSeconds + 's');
    document.head.appendChild(s);
    window.adConfig({ preloadAdBreaks: 'on', sound: 'on', onReady: () => { h5Ready = true; } });

    if (cfg.h5.bannerSlot) {
      const host = document.getElementById('webBanner');
      const ins = document.createElement('ins');
      ins.className = 'adsbygoogle';
      ins.style.cssText = 'display:block;width:100%;height:60px';
      ins.setAttribute('data-ad-client', cfg.h5.client);
      ins.setAttribute('data-ad-slot', cfg.h5.bannerSlot);
      if (cfg.testMode) ins.setAttribute('data-adtest', 'on');
      host.appendChild(ins);
      window.adsbygoogle.push({});
    }
  }

  // ── Mock ads (dev) ─────────────────────────────────────────
  function mockFullscreen(kind) {
    return new Promise((resolve) => {
      const el = document.getElementById('mockAd');
      const label = el.querySelector('.mock-label');
      const btn = el.querySelector('button');
      let t = kind === 'rewarded' ? 5 : 3;
      let done = false;
      label.textContent = (kind === 'rewarded' ? 'Rewarded' : 'Interstitial') + ' test ad';
      btn.disabled = true;
      el.hidden = false;
      const tick = () => {
        if (t > 0) { btn.textContent = 'Close in ' + t; t--; setTimeout(tick, 1000); }
        else { btn.disabled = false; btn.textContent = kind === 'rewarded' ? 'Claim reward ✓' : 'Close ✕'; }
      };
      tick();
      btn.onclick = () => { if (done) return; done = true; el.hidden = true; resolve(true); };
    });
  }

  // ── Public API ─────────────────────────────────────────────
  const Ads = {
    get mode() { return mode; },
    on(t, f) { listeners[t].push(f); },

    async init() {
      if (AdMob && ids) { if (await initAdMob()) mode = 'admob'; }
      else if (!isNative && cfg.h5 && cfg.h5.client) { initH5(); mode = 'h5'; }
      else if (cfg.mockInBrowser) mode = 'mock';
    },

    rewardedAvailable() {
      if (mode === 'admob') return rewardedReady;
      if (mode === 'h5') return h5Ready;
      return mode === 'mock';
    },

    async showBanner() {
      if (bannerShown) return;
      bannerShown = true;
      if (mode === 'admob') {
        try {
          await AdMob.showBanner({
            adId: ids.banner, adSize: 'ADAPTIVE_BANNER', position: 'BOTTOM_CENTER',
            margin: 0, isTesting: !!cfg.testMode,
          });
        } catch (e) { bannerShown = false; }
      } else if (mode === 'h5') {
        const b = document.getElementById('webBanner');
        if (cfg.h5.bannerSlot) { b.hidden = false; setBannerHeight(60); }
      } else if (mode === 'mock') {
        document.getElementById('mockBanner').hidden = false;
        setBannerHeight(50);
      }
    },

    async hideBanner() {
      if (!bannerShown) return;
      bannerShown = false;
      setBannerHeight(0);
      if (mode === 'admob') { try { await AdMob.removeBanner(); } catch (e) {} }
      document.getElementById('mockBanner').hidden = true;
      document.getElementById('webBanner').hidden = true;
    },

    // Call on every game over; returns after an ad (if one was due) closes.
    async gameOverBreak() {
      gameOversTotal++;
      gameOversSinceAd++;
      const now = Date.now();
      if (gameOversTotal <= (cfg.adFreeFirstGames || 0)) return;
      if (gameOversSinceAd < cfg.interstitialEvery) return;
      if (now - lastInterstitial < cfg.interstitialMinSeconds * 1000) return;
      const shown = await this.showInterstitial();
      if (shown) { gameOversSinceAd = 0; lastInterstitial = Date.now(); }
    },

    async showInterstitial() {
      if (mode === 'admob') {
        if (!interstitialReady) return false;
        emit('pause');
        try { await AdMob.showInterstitial(); } catch (e) { emit('resume'); return false; }
        emit('resume');
        prepareInterstitial();
        return true;
      }
      if (mode === 'h5') {
        return new Promise((resolve) => {
          window.adBreak({
            type: 'next', name: 'game-over',
            beforeAd: () => emit('pause'),
            afterAd: () => emit('resume'),
            adBreakDone: (i) => resolve(i && i.breakStatus === 'viewed'),
          });
        });
      }
      if (mode === 'mock') { emit('pause'); await mockFullscreen('interstitial'); emit('resume'); return true; }
      return false;
    },

    // Resolves true only if the player earned the reward.
    async showRewarded(name) {
      if (mode === 'admob') {
        if (!rewardedReady) return false;
        rewardFlag = false;
        emit('pause');
        let item = null;
        try { item = await AdMob.showRewardVideoAd(); } catch (e) {}
        emit('resume');
        prepareRewarded();
        return rewardFlag || !!(item && item.amount !== undefined);
      }
      if (mode === 'h5') {
        return new Promise((resolve) => {
          let earned = false;
          window.adBreak({
            type: 'reward', name: name || 'reward',
            beforeAd: () => emit('pause'),
            afterAd: () => emit('resume'),
            beforeReward: (showAdFn) => showAdFn(),
            adDismissed: () => {},
            adViewed: () => { earned = true; },
            adBreakDone: () => resolve(earned),
          });
        });
      }
      if (mode === 'mock') { emit('pause'); const r = await mockFullscreen('rewarded'); emit('resume'); return r; }
      return false;
    },
  };

  window.Ads = Ads;
})();
