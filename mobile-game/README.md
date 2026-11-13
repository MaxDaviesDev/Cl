# Orbit Hop 🪐

A one-tap arcade game for phones, with Google ads built in.

You orbit a planet. **Tap** to fly off in a straight line and land on the next planet's orbit. If you fly into empty space, the run is over.

## What keeps players coming back

| Hook | How it works |
|---|---|
| Short sessions | You can die within seconds and restart with one tap |
| PERFECT combos | Flying close to a planet's centre builds a combo multiplier, with rising sound pitch and screen bursts |
| Skips | Land on a planet further up to earn bonus points |
| Rising difficulty | Orbits get smaller and faster, and planets start moving |
| 7 zones to discover | The world changes as you climb: **Sunset Skies → Aurora Heights → Low Orbit → Neon Nebula → Spiral Galaxy → Event Horizon → Hyperspace**. Each new zone shows a banner, and discovering one for the first time pays bonus coins. The menu shows your furthest zone |
| Coins + 9 skins | Every run earns something to spend in the shop |
| Daily gift | A login streak (up to 7 days) pays out more each day |
| Best score | "NEW BEST" fanfare when you beat it |
| Juice | Particles, screen shake, vibration, trails, and synthesized sound effects (no audio files) |

## Google ads

| Format | Where it shows | Network |
|---|---|---|
| Banner | Menu, game over and shop screens only, **never during play** | AdMob (native) / AdSense (web) |
| Interstitial | Between runs: at most every 3 game overs, at least 60 s apart, and never in the first 2 games | AdMob / H5 Games Ads |
| Rewarded | Opt-in only: *Continue* (once per run), *2× coins*, *+40 coins*, *Daily ×3* | AdMob / H5 Games Ads |

`www/ads.js` chooses the network automatically:
- **Android/iOS app** → [`@capacitor-community/admob`](https://github.com/capacitor-community/admob), including the GDPR consent form (UMP) and the iOS tracking (ATT) prompt
- **Website** → [Google H5 Games Ads](https://developers.google.com/ad-placement) (AdSense `adBreak()`)
- **Local browser** → a fake "test ad" so you can try every flow

The game pauses and mutes while an ad is on screen.

All IDs ship as **Google's official test IDs**, so you can't earn money until you swap in your own (see below).

## Play it now (browser)

```bash
cd mobile-game
npm run serve      # then open http://localhost:8080 on your phone/desktop
```

## Build the Android / iOS app

You need Node 20+, Android Studio (for Android) and Xcode on a Mac (for iOS).

```bash
cd mobile-game
npm install
npm run android    # adds the Android project, injects the AdMob app id, opens Android Studio
npm run ios        # same for iOS (macOS only)
```

After changing anything in `www/`, run `npm run sync`.

## Going live with real ads (checklist)

1. Create an app in [AdMob](https://admob.google.com). Copy the **App ID** (`ca-app-pub-…~…`) into `admob.config.json`.
2. Create 3 ad units (Banner, Interstitial, Rewarded). Paste their IDs (`ca-app-pub-…/…`) into `www/ads-config.js`.
3. In `www/ads-config.js`, set `testMode: false`.
4. Change `appId` in `capacitor.config.json` (e.g. `com.yourname.orbithop`).
5. Run `npm run sync`, then build a signed release in Android Studio / Xcode.
6. Publish an `app-ads.txt` file on your developer website (AdMob shows you what to put in it).
7. Set up the GDPR message in AdMob → *Privacy & messaging*. The app already shows it.
8. For the **web** version: put your AdSense publisher id in `h5.client`. Your site must be approved for AdSense / H5 Games Ads.

⚠️ Don't click your own live ads. Use test IDs or test devices while developing, or AdMob may suspend your account.

## Files

```
www/index.html         screens & ad containers
www/backgrounds.js     the 7 climbing zones (sky, sun, aurora, Earth, nebula, galaxy, black hole, warp)
www/game.js            game engine, shop, daily reward, save data (localStorage)
www/ads.js             AdMob / H5 / mock ad layer
www/ads-config.js      ad unit ids + pacing   ← edit me
admob.config.json      AdMob app ids          ← edit me
scripts/configure-native.js   patches AndroidManifest.xml / Info.plist
scripts/smoke-test.js         headless Playwright test with an auto-playing bot
```
