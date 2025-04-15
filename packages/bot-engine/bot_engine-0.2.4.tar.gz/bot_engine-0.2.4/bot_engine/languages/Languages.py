from os import getenv

from dataclasses import dataclass, field
from typing import ClassVar


if getenv("ENVIRONMENT") == "testing":
    from languages.Locale import Locale

else:
    from bot_engine.languages.Locale import Locale



@dataclass
class Languages:
    active_lang: str = "ru"
    languages: ClassVar[dict[str, Locale]] = {}

    def add_locale(self, locale: Locale):
        self.languages[locale.lang] = locale
        print(f"🔷 {locale.lang} is added to languages!")

    def get_active_locale(self) -> Locale | None:
        return self.languages.get(self.active_lang)

    def get_messages(self, user_language: str | None = None) -> list[dict[str, str]]:
        active_language = user_language or self.active_lang
        locale = self.languages.get(active_language)

        if not locale:
            raise ValueError(f"Locale '{active_language}' not found.")
        
        return locale.messages

