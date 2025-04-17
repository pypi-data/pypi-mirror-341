import asyncio
import aiohttp
import aiosqlite
import pandas as pd
import numpy as np
import pyttsx3
import logging
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from scipy.signal import savgol_filter
from typing import Optional, Tuple, Dict, Any

# === Configuration ===
STRATEGY_FILTER = {"momentum", "reversal"}
ALERT_CONFIDENCE_THRESHOLD = 0.8
REFRESH_INTERVAL = 10
GRANULARITY = 300
Z_SCORE_WINDOW = 20
VOLATILITY_THRESHOLD = 0.015
FLAT_SLOPE_THRESHOLD = 1e-4
API_URL = "https://api.exchange.coinbase.com/products/{}/candles"
RETRY_LIMIT = 3
DB_PATH = "signals.db"

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# === Console Setup ===
console = Console()

# === Asset Settings ===
SETTINGS: Dict[str, Dict[str, Any]] = {
    'BTC-USD': {'ema': (12, 26), 'z_thresh': 1.5},
    'ETH-USD': {'ema': (10, 21), 'z_thresh': 1.4},
    'SOL-USD': {'ema': (10, 21), 'z_thresh': 1.6},
    'ADA-USD': {'ema': (8, 19), 'z_thresh': 1.3},
    'AVAX-USD': {'ema': (9, 18), 'z_thresh': 1.4},
    'DOGE-USD': {'ema': (7, 17), 'z_thresh': 1.2},
    'SHIB-USD': {'ema': (6, 15), 'z_thresh': 1.1},
    'XRP-USD': {'ema': (9, 20), 'z_thresh': 1.4},
    'LINK-USD': {'ema': (9, 20), 'z_thresh': 1.5},
    'MATIC-USD': {'ema': (8, 19), 'z_thresh': 1.3},
    'ARB-USD': {'ema': (7, 18), 'z_thresh': 1.3},
    'OP-USD': {'ema': (8, 19), 'z_thresh': 1.4},
    'APT-USD': {'ema': (9, 21), 'z_thresh': 1.5},
    'INJ-USD': {'ema': (10, 22), 'z_thresh': 1.6},
    'RNDR-USD': {'ema': (9, 20), 'z_thresh': 1.4},
    'TIA-USD': {'ema': (8, 19), 'z_thresh': 1.4},
    'PEPE-USD': {'ema': (6, 15), 'z_thresh': 1.2},
    'FET-USD': {'ema': (9, 21), 'z_thresh': 1.5},
    'JTO-USD': {'ema': (8, 20), 'z_thresh': 1.4},
    'WIF-USD': {'ema': (7, 17), 'z_thresh': 1.3},
}
PRODUCTS = list(SETTINGS.keys())

# === Text-to-Speech Setup ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

def speak_alert(message: str) -> None:
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Text-to-Speech error: {e}")

# === Strategy Classification ===
def classify_strategy(z_score: float, slope: float) -> str:
    if abs(z_score) > 2.0 and abs(slope) > FLAT_SLOPE_THRESHOLD:
        return "momentum"
    elif abs(z_score) > 1.5 and abs(slope) <= FLAT_SLOPE_THRESHOLD:
        return "reversal"
    return "neutral"

# === Indicator Calculation ===
def calculate_indicators(df: pd.DataFrame, product: str) -> Tuple[str, float, float, float, str]:
    short_ema, long_ema = SETTINGS[product]['ema']
    z_thresh = SETTINGS[product]['z_thresh']

    if df is None or len(df) < long_ema + Z_SCORE_WINDOW:
        return 'HOLD', np.nan, np.nan, 0.0, "neutral"

    close = df['close']
    delta = close.ewm(span=short_ema).mean() - close.ewm(span=long_ema).mean()

    rolling_mean = delta.rolling(Z_SCORE_WINDOW).mean()
    rolling_std = delta.rolling(Z_SCORE_WINDOW).std(ddof=0).replace(0, 1e-8)
    z_scores = ((delta - rolling_mean) / rolling_std).replace([np.inf, -np.inf], 0).fillna(0)

    latest_price = float(close.iloc[-1])
    latest_z = float(z_scores.iloc[-1])

    # Savitzky-Golay filter for slope estimation
    if len(close) >= Z_SCORE_WINDOW:
        smoothed = savgol_filter(close[-Z_SCORE_WINDOW:], window_length=5, polyorder=2)
        slope = float(np.polyfit(range(len(smoothed)), smoothed, 1)[0])
    else:
        slope = 0.0

    volatility = float(close.pct_change().rolling(Z_SCORE_WINDOW).std().iloc[-1])

    signal = 'HOLD'
    confidence = 0.0

    if latest_z > z_thresh:
        signal = 'BUY'
        confidence = min((latest_z - z_thresh) / 2, 1.0)
    elif latest_z < -z_thresh:
        signal = 'SELL'
        confidence = min((-latest_z - z_thresh) / 2, 1.0)

    if signal != 'HOLD' and volatility > VOLATILITY_THRESHOLD:
        confidence = min(confidence * 1.2, 1.0)

    if abs(slope) < FLAT_SLOPE_THRESHOLD:
        signal = 'HOLD'
        confidence *= 0.25

    strategy = classify_strategy(latest_z, slope)

    logger.debug(f"{product}: Signal: {signal}, Z-Score: {latest_z:.2f}, Slope: {slope:.6f}, "
                 f"Volatility: {volatility:.4f}, Confidence: {confidence:.2%}, Strategy: {strategy}")

    return signal, latest_price, latest_z, confidence, strategy

# === Networking: Fetch Candle Data ===
async def fetch_candles(session: aiohttp.ClientSession, product_id: str) -> Optional[pd.DataFrame]:
    url = API_URL.format(product_id)
    params = {'granularity': GRANULARITY}

    for attempt in range(RETRY_LIMIT):
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if isinstance(data, dict) and data.get("message"):
                    raise ValueError(data["message"])
                df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df.sort_values('time').reset_index(drop=True)
        except Exception as e:
            logger.error(f"Error fetching {product_id} data: {e}")
            if attempt == RETRY_LIMIT - 1:
                console.print(f"[magenta]Fetch failed for {product_id}: {e}[/magenta]")
            await asyncio.sleep(min(2 ** attempt * 0.2, 2.0))
    return None

# === Scanner Logic ===
async def scan_product(session: aiohttp.ClientSession, product_id: str, db_conn: aiosqlite.Connection) -> Optional[Tuple[str, float, Tuple[str, str, str, str, str]]]:
    df = await fetch_candles(session, product_id)
    if df is None:
        return None

    signal, price, z_score, confidence, strategy = await asyncio.to_thread(calculate_indicators, df, product_id)
    if np.isnan(price) or strategy not in STRATEGY_FILTER:
        return None

    timestamp = datetime.utcnow().isoformat()

    try:
        # Use aiosqlite for database operations
        async with db_conn.execute("INSERT INTO signals VALUES (?, ?, ?, ?, ?, ?, ?)", (
            timestamp, product_id, price, z_score, signal, confidence, strategy
        )):
            await db_conn.commit()
    except Exception as e:
        logger.error(f"Database error for {product_id}: {e}")

    if signal in {"BUY", "SELL"} and confidence >= ALERT_CONFIDENCE_THRESHOLD:
        alert_msg = f"{signal.capitalize()} signal for {product_id}. Confidence {confidence:.0%}"
        color = "green" if signal == "BUY" else "red"
        console.print(f"[bold {color} blink]{alert_msg}[/bold {color} blink]")
        speak_alert(alert_msg)

    price_fmt = f"${price:,.6f}" if price < 1 else f"${price:,.2f}"
    signal_color = {'BUY': 'green', 'SELL': 'red', 'HOLD': 'yellow'}[signal]

    return signal, confidence, (
        f"[bold]{product_id}[/bold]",
        f"[white]{price_fmt}[/white]",
        f"[cyan]{z_score:.2f}[/cyan]",
        f"[{signal_color}]{signal}[/{signal_color}]",
        f"[bold]{confidence:.2%}[/bold]"
    )

# === UI Table Builder ===
def build_table(results: list) -> Table:
    table = Table(title=f"📡 Crypto Signals @ {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    table.add_column("Asset", justify="left", style="bold")
    table.add_column("Price", justify="right")
    table.add_column("Z-Score", justify="center")
    table.add_column("Signal", justify="center")
    table.add_column("Confidence", justify="right")

    for _, _, (asset, price, z, signal, conf) in sorted(filter(None, results), key=lambda x: (x[0] == 'HOLD', -x[1])):
        table.add_row(asset, price, z, signal, conf)

    return table

# === Main Runner ===
async def main():
    console.print(f"\n[bold cyan]Smart Coinbase Signal Scanner Initialized[/bold cyan]\n")

    # Use aiosqlite to open the database connection asynchronously
    async with aiosqlite.connect(DB_PATH) as db_conn:
        await db_conn.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                timestamp TEXT, asset TEXT, price REAL, z_score REAL,
                signal TEXT, confidence REAL, strategy TEXT
            )
        """)
        await db_conn.commit()

        timeout = aiohttp.ClientTimeout(sock_connect=5, sock_read=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            with Live(console=console, refresh_per_second=2, screen=False) as live:
                while True:
                    tasks = [scan_product(session, product, db_conn) for product in PRODUCTS]
                    results = await asyncio.gather(*tasks)
                    live.update(build_table(results))
                    await asyncio.sleep(REFRESH_INTERVAL)

def cli():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red]Scanner stopped by user.[/red]")

if __name__ == '__main__':
    cli()