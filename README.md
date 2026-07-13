# AI Trading Assistant

A signal app that analyzes forex majors/minors, commodities (gold, silver, oil, gas, copper),
and crypto (BTC, ETH, and 10 more) across multiple timeframes — giving you a Buy/Sell signal,
Entry, Stop Loss, Take Profit 1/2/3, and a binary next-candle prediction. Installable as an
app on Android straight from your browser.

## How it's built

- **Backend** (`/backend`) — Python + FastAPI. Runs the actual analysis: market structure,
  support/resistance, supply/demand zones, fair value gaps, liquidity, order blocks, candle
  patterns, and 15+ technical indicators, combined into a confidence-scored signal.
  - Crypto prices come live from **Binance's public API** (no key needed, genuinely real-time).
  - Forex/commodity prices come from **Yahoo Finance** (free, no key, but can lag ~15 min on
    some symbols — see "Upgrading data" below).
- **Frontend** (`/frontend`) — a Progressive Web App (PWA): plain HTML/CSS/JS, installable on
  your phone's home screen, works offline for the UI shell (signals still need a live connection).

## 1. Deploy the backend (free, ~5 minutes)

The frontend on your phone can't run Python — it needs a live server to call. Render's free
tier works well for this:

1. Create a free account at https://render.com
2. Push this project (or just the `backend/` folder) to a GitHub repo
3. In Render: **New +** → **Blueprint** → connect your repo → it will detect `render.yaml`
   automatically and set everything up
   - Alternatively: **New +** → **Web Service** → set root directory to `backend`,
     build command `pip install -r requirements.txt`, start command
     `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy. Render gives you a URL like `https://ai-trading-assistant-xxxx.onrender.com`
5. Visit `<your-url>/health` in a browser — you should see `{"status":"OK"}`

Note: Render's free tier sleeps after inactivity and takes ~30-60s to wake up on the first
request. That's normal for a free deployment.

## 2. Point the app at your backend

Open the frontend (see step 3), go to **Settings**, paste your Render URL, tap
**Save & Test Connection**. It's stored on your device — you only do this once.

## 3. Install the PWA on Android

Easiest: host `frontend/` for free too (GitHub Pages, Netlify, Vercel, Cloudflare Pages all
work — drag-and-drop the folder onto Netlify's dashboard for the fastest path). Then on your
Android phone:

1. Open the site URL in **Chrome**
2. Tap the **⋮** menu → **Install app** (or you'll see an **Install App** button in the app itself)
3. It installs like a native app, with its own icon on your home screen

You can also open `frontend/index.html` directly from a local web server (e.g. `python -m
http.server` on your PC, then visit `http://<your-pc-ip>:8000` from your phone on the same
Wi-Fi) if you don't want to host it publicly yet.

## Upgrading data quality later

To move off Yahoo Finance's delay for forex/commodities, sign up for a free Twelve Data key
(twelvedata.com) and swap the `_from_yfinance` branch in `backend/market_data.py` for a Twelve
Data REST call — the rest of the app (indicators, scoring, signals) doesn't need to change.

## Endpoints

- `GET /signal/{symbol}/{timeframe}` — full buy/sell signal with entry/SL/TP1-3
- `GET /binary/{symbol}/{timeframe}` — next-candle bullish/bearish prediction (1m/3m/5m)
- `POST /signals` — batch signals: `{"symbols": [...], "timeframe": "1h"}`
- `GET /assets` — full symbol list by category
- `GET /watchlist`, `POST /watchlist`, `DELETE /watchlist/{symbol}` — manage your watchlist
- `GET /history/{symbol}` — recently scanned signals for a symbol (background scanner runs
  every 15 min against your watchlist)

## Important

Signals are generated from technical analysis (indicators, structure, patterns) — they are
not guaranteed predictions, especially the binary next-candle feature. Treat this as a
decision-support tool, not financial advice, and always manage your own risk.
