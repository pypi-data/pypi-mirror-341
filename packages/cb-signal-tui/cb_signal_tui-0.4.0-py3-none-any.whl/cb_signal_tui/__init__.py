"""
cb_signal_tui
=============

An advanced, high-efficiency terminal-based crypto signal scanner for Coinbase assets.
This scanner fuses Z-score anomaly detection, EMA momentum tracking, volatility- and
slope-adjusted confidence modeling, and strategy classification to surface high-confidence
BUY/SELL signals in real-time — with auto-evaluated accuracy via built-in backtesting.

Core Features:
--------------
- Strategy fusion: Z-score, EMA differentials, volatility, and slope
- Momentum vs. reversal strategy classification
- Adaptive, asset-specific signal sensitivity (EMA + Z-score thresholds)
- Dynamic confidence scoring based on volatility and trend slope
- Live auto-refreshing terminal UI with Rich
- Real-time voice alerts via pyttsx3 (BUY/SELL signals only)
- Asynchronous architecture with aiohttp and aiosqlite
- Persistent signal logging to local SQLite DB
- Resilient fetch logic with intelligent retry/backoff
- Built-in post-session backtesting to validate signal performance
- Extensible CLI modes (run, export, backtest, etc.)

Exposes:
--------
- main():        Main async runtime loop for live signal scanning
- cli():         Interactive CLI entry point with live TUI and extended options
- run_backtest(): Async accuracy validation via real-time market fetch
- SETTINGS:      Asset-level strategy sensitivity configuration dictionary
"""

from .__main__ import main, cli, run_backtest, SETTINGS

__version__ = "0.4.0"
__author__ = "LoQiseaking69"
