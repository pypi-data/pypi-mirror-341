# Cb-signalTUI
[![Build and Publish](https://github.com/LoQiseaking69/Cb-signalTUI/actions/workflows/build.yml/badge.svg)](https://github.com/LoQiseaking69/Cb-signalTUI/actions/workflows/build.yml)

![screenshot](https://github.com/LoQiseaking69/Cb-signalTUI/blob/main/8247439A-0E30-439A-AD1B-E41A16CC9891.png)

**Cb-signalTUI** is a real-time, terminal-native crypto signal scanner built for Coinbase assets.  
It uses Z-score anomaly detection, adaptive EMA momentum modeling, trend slope analysis, and confidence scoring to classify trading opportunities as **momentum**, **reversal**, or **neutral** strategies—complete with voice alerts and persistent logging.

---

## Features

- **Real-Time Signal Detection**: Continuously monitors supported Coinbase pairs for actionable trade signals.
- **Smart Signal Fusion**: Combines Z-score, EMA differentials, volatility, and slope for more reliable detection.
- **Strategy Classification**: Flags opportunities as **momentum**, **reversal**, or **neutral** based on composite indicators.
- **Confidence-Weighted Alerts**: Dynamic scoring adjusts based on trend slope and volatility.
- **Rich Terminal UI**: Auto-refreshing, color-coded interface with real-time stats and categorized signals.
- **Voice Alerts**: Uses `pyttsx3` for BUY/SELL vocal alerts when confidence is high.
- **Asynchronous Execution**: Built on `asyncio`, `aiohttp`, and `aiosqlite` for high throughput and reliability.
- **SQLite Logging**: Every signal gets logged to `signals.db` for backtesting or historical review.
- **Custom Per-Asset Configs**: Fine-tune EMA periods and sensitivity thresholds for each asset.
- **Modular CLI Modes**: Supports future extensions like `--backtest`, `--export`, etc.
- **Resilient Networking**: Intelligent retry/backoff logic prevents flake-outs on rate limits or network errors.

---

## Project Structure

```
Cb-signalTUI/
├── cb_signal_tui/             # Core signal scanner package
│   ├── __init__.py            # Package definition
│   └── __main__.py            # Runtime, config, CLI
├── built/                     # Auto-built wheels/tarballs on push
│   └── cb_signal_tui-*.whl
├── dist/                      # Local pip builds (ignored by git)
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions for CI/CD
├── requirements.txt           # Runtime dependencies
├── pyproject.toml             # Build metadata (PEP 621)
├── README.md                  # You are here.
└── signals.db                 # SQLite runtime DB (auto-created)
```

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/LoQiseaking69/Cb-signalTUI.git
   cd Cb-signalTUI
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install from a local build:

   ```bash
   pip install built/cb_signal_tui-*.whl
   ```

---

## Dependencies

```
aiohttp
aiosqlite
pandas
numpy
pyttsx3
rich
scipy
```

---

## Usage

To launch the live scanner with the terminal UI:

```bash
cb-signal-tui
```

### Live Output

![output](https://github.com/LoQiseaking69/Cb-signalTUI/blob/main/IMG_1053.jpeg)

---

## Configuration

Configuration is handled in `cb_signal_tui/__main__.py`.

Key tunables:

- `PRODUCTS`: Coinbase trading pairs to monitor (`BTC-USD`, `ETH-USD`, etc.)
- `SETTINGS`: Per-asset strategy config (`fast_ema`, `slow_ema`, `zscore_threshold`)
- `Z_SCORE_WINDOW`, `VOLATILITY_THRESHOLD`, `FLAT_SLOPE_THRESHOLD`: Core tuning params
- `STRATEGY_FILTER`: Filter strategy types (`momentum`, `reversal`)
- `ALERT_CONFIDENCE_THRESHOLD`: Minimum confidence required to trigger a voice alert
- `REFRESH_INTERVAL`: UI update frequency (seconds)

---

## Database

Signal logs are persisted to `signals.db`.

### Schema:

```sql
CREATE TABLE IF NOT EXISTS signals (
    timestamp TEXT,
    asset TEXT,
    price REAL,
    z_score REAL,
    signal TEXT,
    confidence REAL,
    strategy TEXT
);
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b my-feature`)
3. Push your changes
4. Open a pull request

---

**Built for precision. Tuned for real-time alpha.  
Get signals. Not noise.**  
— `LoQiseaking69`