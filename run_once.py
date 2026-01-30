#!/usr/bin/env python3
"""Run bot once and exit"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram_bot_module.main import TelegramBot

asyncio.run(TelegramBot().run_once())

