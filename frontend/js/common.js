// ==============================================
// AI Trading Assistant — shared config
// ==============================================

// Backend URL is user-configurable from the Settings page (stored in localStorage),
// because a PWA installed on your phone can't reach "localhost" — it needs the
// real address of wherever you deployed the backend (e.g. Render).
function getApiBase() {
  return localStorage.getItem("apiBase") || "https://YOUR-BACKEND-URL.onrender.com";
}

function setApiBase(url) {
  localStorage.setItem("apiBase", url.replace(/\/$/, ""));
}

const ASSET_GROUPS = {
  forex: {
    label: "Forex — Majors & Minors",
    symbols: [
      "EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD",
      "EURGBP","EURJPY","GBPJPY","AUDJPY","CHFJPY","EURAUD","GBPAUD",
      "EURCAD","GBPCAD","AUDCAD","AUDCHF","CADCHF","EURNZD","GBPNZD","NZDJPY"
    ]
  },
  commodities: {
    label: "Commodities",
    symbols: ["XAUUSD","XAGUSD","WTIUSD","BRENTUSD","NGASUSD","COPPERUSD"]
  },
  crypto: {
    label: "Crypto",
    symbols: [
      "BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT",
      "DOGEUSDT","TRXUSDT","AVAXUSDT","LINKUSDT","DOTUSDT","LTCUSDT"
    ]
  },
  favorites: {
    label: "Favorites",
    symbols: ["EURUSD","GBPUSD","XAUUSD","BTCUSDT","ETHUSDT"]
  }
};

function allSymbolsFlat() {
  const seen = new Set();
  const out = [];
  for (const key of ["forex", "commodities", "crypto"]) {
    for (const s of ASSET_GROUPS[key].symbols) {
      if (!seen.has(s)) { seen.add(s); out.push(s); }
    }
  }
  return out;
}

// Register the service worker on every page
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js");
  });
}

// PWA install prompt (button is optional per-page)
let deferredPrompt = null;
window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  const btn = document.getElementById("installButton");
  if (btn) btn.hidden = false;
});

function triggerInstall() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(() => { deferredPrompt = null; });
  const btn = document.getElementById("installButton");
  if (btn) btn.hidden = true;
}
