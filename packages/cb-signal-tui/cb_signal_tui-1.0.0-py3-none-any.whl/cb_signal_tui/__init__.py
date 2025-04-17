"""
cb_signal_tui
=============

A high-performance, terminal-based crypto signal scanner for Coinbase assets.
This scanner utilizes Z-score anomaly detection, volatility-adjusted momentum
analysis, and strategy classification (momentum vs. reversal) to surface
actionable BUY/SELL opportunities in real-time.

Core Features:
--------------
- Strategy-aware Z-score signal generation
- Volatility and slope-aware confidence modeling
- Adaptive EMA configuration per asset
- Live TUI updates via Rich
- Audio alerts via pyttsx3
- Asynchronous execution with aiohttp and aiosqlite
- Persistent signal logging to SQLite

Exposes:
--------
- main():    Main asynchronous event loop
- cli():     Interactive command-line runner with live Rich output
- SETTINGS:  Fine-tuned per-asset configuration for signal sensitivity
"""

from .__main__ import main, cli, SETTINGS

__version__ = "0.1.0"
__author__ = "LoQiseaking69"