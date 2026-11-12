// ─────────────────────────────────────────────────────────────
//  Ad configuration for Orbit Hop
//
//  The IDs below are Google's official TEST ids. They always
//  serve test ads and are safe to click while developing.
//  Before publishing, replace them with your own ids from
//  https://admob.google.com (native apps) and
//  https://adsense.google.com (web build) and set testMode=false.
// ─────────────────────────────────────────────────────────────
window.ADS_CONFIG = {
  testMode: true,

  // Native (Android / iOS via Capacitor + @capacitor-community/admob)
  admob: {
    android: {
      banner:       'ca-app-pub-3940256099942544/6300978111',
      interstitial: 'ca-app-pub-3940256099942544/1033173712',
      rewarded:     'ca-app-pub-3940256099942544/5224354917',
    },
    ios: {
      banner:       'ca-app-pub-3940256099942544/2934735716',
      interstitial: 'ca-app-pub-3940256099942544/4411468910',
      rewarded:     'ca-app-pub-3940256099942544/1712485313',
    },
  },

  // Web build (Google AdSense H5 Games Ads). Leave client empty to disable.
  h5: {
    client: '',        // e.g. 'ca-pub-1234567890123456'
    bannerSlot: '',    // optional AdSense display ad slot id for the menu banner
  },

  // Pacing: an interstitial shows at most every N game-overs and
  // never more often than every M seconds. Players get the first
  // couple of runs ad-free.
  interstitialEvery: 3,
  interstitialMinSeconds: 60,
  adFreeFirstGames: 2,

  // When no real ad network is available (e.g. desktop browser
  // during development), show a fake "test ad" so flows can be tried.
  mockInBrowser: true,
};
