"""
Mora: A self-contained Python remote administration library.
Author: omar
"""
import os
from .file_ops import list_all_files, delete_path, read_file, write_file
from .sys_info import get_system_info, get_network_info
from .command_exec import run_command
from .bot import TelegramBot
from .handlers import register_default_handlers

__all__ = [
    "list_all_files", "delete_path", "read_file", "write_file",
    "get_system_info", "get_network_info",
    "run_command", "TelegramBot", "start_bot"
]

def start_bot(token: str = None) -> TelegramBot:
    """
    Start the Telegram bot with the given token.
    If no token is passed, falls back to MORA_TOKEN environment variable.
    Returns the TelegramBot instance.
    """
    token = token or os.getenv("MORA_TOKEN")
    if not token:
        raise ValueError("Telegram token not provided. Pass it to start_bot() or set MORA_TOKEN.")
    bot = TelegramBot(token)
    register_default_handlers(bot)
    bot.start()
    return bot