// ==============================================
// AI Trading Assistant — frontend/js/app.js
// ==============================================

const marketType = document.getElementById("marketType");
const symbolSelector = document.getElementById("symbolSelector");
const timeframe = document.getElementById("timeframeSelector");
const modeSelector = document.getElementById("modeSelector");

const analyzeButton = document.getElementById("analyzeButton");
const installButton = document.getElementById("installButton");

const signalEl = document.getElementById("signal");
const confidenceEl = document.getElementById("confidence");
const nextCandleEl = document.getElementById("nextCandle");

const entry = document.getElementById("entry");
const sl = document.getElementById("sl");
const tp1 = document.getElementById("tp1");
const tp2 = document.getElementById("tp2");
const tp3 = document.getElementById("tp3");
const tradeCard = document.getElementById("tradeCard");

const trend = document.getElementById("trend");
const quality = document.getElementById("quality");
const volatility = document.getElementById("volatility");
const volume = document.getElementById("volume");
const alignment = document.getElementById("alignment");

const reasonList = document.getElementById("reasonList");
const binaryCard = document.getElementById("binaryCard");
const binarySignal = document.getElementById("binarySignal");

const BINARY_TIMEFRAMES = ["1m", "3m", "5m"];

function loadSymbols() {
  symbolSelector.innerHTML = "";
  const group = ASSET_GROUPS[marketType.value];
  group.symbols.forEach((symbol) => {
    const option = document.createElement("option");
    option.value = symbol;
    option.textContent = symbol;
    symbolSelector.appendChild(option);
  });
}

marketType.addEventListener("change", loadSymbols);
loadSymbols();

function applyMode() {
  const isBinary = modeSelector.value === "binary";

  timeframe.innerHTML = "";
  const frames = isBinary ? BINARY_TIMEFRAMES : ["1m","3m","5m","15m","30m","1h","4h","1d"];
  frames.forEach((tf) => {
    const opt = document.createElement("option");
    opt.value = tf;
    opt.textContent = tf;
    if (tf === (isBinary ? "5m" : "1h")) opt.selected = true;
    timeframe.appendChild(opt);
  });

  tradeCard.hidden = isBinary;
  document.getElementById("statusCard").hidden = isBinary;
  binaryCard.hidden = !isBinary;
}
modeSelector.addEventListener("change", applyMode);
applyMode();

async function analyze() {
  const symbol = symbolSelector.value;
  const tf = timeframe.value;
  const isBinary = modeSelector.value === "binary";

  analyzeButton.disabled = true;
  analyzeButton.textContent = "Analyzing...";

  try {
    const apiBase = getApiBase();
    const url = isBinary
      ? `${apiBase}/binary/${symbol}/${tf}`
      : `${apiBase}/signal/${symbol}/${tf}`;

    const response = await fetch(url);
    const data = await response.json();

    if (!data.status) {
      signalEl.textContent = "ERROR";
      alert(data.message || "Could not fetch a signal. Check your backend URL in Settings.");
      return;
    }

    if (isBinary) {
      binarySignal.textContent = `${data.prediction} (${data.confidence}%)`;
      binarySignal.className = "";
      binarySignal.classList.add(data.prediction === "BULLISH" ? "buy" : data.prediction === "BEARISH" ? "sell" : "wait");

      reasonList.innerHTML = "";
      (data.reasons || []).forEach((reason) => {
        const li = document.createElement("li");
        li.textContent = reason;
        reasonList.appendChild(li);
      });
      signalEl.textContent = "\u2014";
      confidenceEl.textContent = "";
      nextCandleEl.textContent = "Current price: " + data.current_price;
      return;
    }

    signalEl.textContent = data.signal;
    confidenceEl.textContent = data.confidence + " %";
    nextCandleEl.textContent = "Next candle: " + data.next_candle;

    entry.textContent = data.entry;
    sl.textContent = data.stop_loss;
    tp1.textContent = data.take_profit_1;
    tp2.textContent = data.take_profit_2;
    tp3.textContent = data.take_profit_3;

    trend.textContent = data.trend;
    quality.textContent = "\u2605".repeat(data.trade_quality || 0) || "-";
    volatility.textContent = data.volatility + " %";
    volume.textContent = data.volume_strength;
    alignment.textContent = (data.timeframe_alignment ?? "-") + " %";

    reasonList.innerHTML = "";
    (data.reasons || []).forEach((reason) => {
      const li = document.createElement("li");
      li.textContent = reason;
      reasonList.appendChild(li);
    });

    signalEl.className = "";
    if (data.signal.includes("BUY")) signalEl.classList.add("buy");
    else if (data.signal.includes("SELL")) signalEl.classList.add("sell");
    else signalEl.classList.add("wait");
  } catch (error) {
    console.error(error);
    signalEl.textContent = "Connection Error";
    alert("Couldn't reach the backend. Set your backend URL in Settings first.");
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.textContent = "Analyze";
  }
}

analyzeButton.addEventListener("click", analyze);

if (installButton) {
  installButton.addEventListener("click", triggerInstall);
}
