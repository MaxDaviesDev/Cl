#!/usr/bin/env node
// Injects the AdMob app id (and iOS privacy keys) into the native projects
// created by `npx cap add android|ios`. Safe to run repeatedly.
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const cfg = JSON.parse(fs.readFileSync(path.join(root, 'admob.config.json'), 'utf8'));

// ── Android ──────────────────────────────────────────────
const manifest = path.join(root, 'android/app/src/main/AndroidManifest.xml');
if (fs.existsSync(manifest)) {
  let xml = fs.readFileSync(manifest, 'utf8');
  const tag = `<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="${cfg.androidAppId}"/>`;
  if (xml.includes('com.google.android.gms.ads.APPLICATION_ID')) {
    xml = xml.replace(/<meta-data android:name="com\.google\.android\.gms\.ads\.APPLICATION_ID"[^>]*\/>/, tag);
  } else {
    xml = xml.replace(/<application([^>]*)>/, (m) => `${m}\n        ${tag}`);
  }
  if (!xml.includes('com.google.android.gms.permission.AD_ID')) {
    xml = xml.replace('</manifest>', '    <uses-permission android:name="com.google.android.gms.permission.AD_ID"/>\n</manifest>');
  }
  // Lock to portrait
  if (!xml.includes('android:screenOrientation')) {
    xml = xml.replace(/<activity(\s)/, '<activity android:screenOrientation="portrait"$1');
  }
  fs.writeFileSync(manifest, xml);
  console.log('✓ Android: AdMob app id set in AndroidManifest.xml');
} else {
  console.log('· Android project not found (run `npx cap add android` first) — skipped');
}

// ── iOS ──────────────────────────────────────────────────
const plist = path.join(root, 'ios/App/App/Info.plist');
if (fs.existsSync(plist)) {
  let xml = fs.readFileSync(plist, 'utf8');
  const setKey = (key, valueXml) => {
    const re = new RegExp(`<key>${key}</key>\\s*(<string>[^<]*</string>|<array>[\\s\\S]*?</array>)`);
    if (re.test(xml)) xml = xml.replace(re, `<key>${key}</key>\n\t${valueXml}`);
    else xml = xml.replace(/<\/dict>\s*<\/plist>\s*$/, `\t<key>${key}</key>\n\t${valueXml}\n</dict>\n</plist>\n`);
  };
  setKey('GADApplicationIdentifier', `<string>${cfg.iosAppId}</string>`);
  setKey('NSUserTrackingUsageDescription', `<string>${cfg.iosTrackingMessage}</string>`);
  // Google's own SKAdNetwork id (add the full list from Google's docs for best fill)
  setKey('SKAdNetworkItems',
    '<array>\n\t\t<dict>\n\t\t\t<key>SKAdNetworkIdentifier</key>\n\t\t\t<string>cstr6suwn9.skadnetwork</string>\n\t\t</dict>\n\t</array>');
  fs.writeFileSync(plist, xml);
  console.log('✓ iOS: GADApplicationIdentifier / ATT / SKAdNetwork set in Info.plist');
} else {
  console.log('· iOS project not found (run `npx cap add ios` first) — skipped');
}
