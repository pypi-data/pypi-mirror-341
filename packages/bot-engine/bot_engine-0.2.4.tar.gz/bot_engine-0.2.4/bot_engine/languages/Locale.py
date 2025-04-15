from dataclasses import dataclass, field
from telebot.types import BotCommand


@dataclass
class Locale:
    lang: str
    menu_commands: list[BotCommand]
    messages: list[dict[str, str]]