from os import getenv
from typing import Union

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot.states.sync.middleware import StateMiddleware
from telebot.custom_filters import StateFilter, IsDigitFilter, TextMatchFilter


if getenv("ENVIRONMENT") == "testing":
    from bot.Filters import AccessLevelFilter
    from data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID

else:
    from bot_engine.bot.Filters import AccessLevelFilter
    from bot_engine.data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID



class Bot:
    """class to connect and run bot"""

    _instance = None
    _bot: TeleBot = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)

            cls._instance._bot = TeleBot(
                token=BOT_TOKEN, use_class_middlewares=True
            )

        return cls._instance


    def __init__(self):
        pass


    def get_bot_instance(self):
        return self._bot


    def start(self) -> TeleBot:
        if self._bot:
            self.set_middleware()

            self.tell_super_admin(["Начинаю работу..."])
            self.tell_super_admin(["/start"])

        bot_username = self.get_bot_data(bot=self._bot, requested_data="username")
        print(f"🟢 Бот @{bot_username} подключён! Нажми /start для начала")

        if ENVIRONMENT == "testing" or ENVIRONMENT == "development":
            self._bot.infinity_polling(
                timeout=5,
                skip_pending=True,
                long_polling_timeout=20,
                restart_on_change=True,
            )

        self._bot.infinity_polling(
            timeout=5, skip_pending=True, long_polling_timeout=20
        )

    def disconnect(self) -> None:
        """kills the active bot instance, drops connection"""
        self._bot.stop_bot()
        print("бот выключен ❌")


    def get_bot_data(self, bot: TeleBot, requested_data: str) -> str:
        """gets bot's name, @username etc"""

        all_bot_info = bot.get_me()

        desired_info = getattr(all_bot_info, requested_data)
        return desired_info


    def set_middleware(self) -> None:
        self._bot.add_custom_filter(StateFilter(self._bot))
        self._bot.add_custom_filter(IsDigitFilter())
        self._bot.add_custom_filter(TextMatchFilter())
        self._bot.add_custom_filter(AccessLevelFilter(self._bot))

        self._bot.setup_middleware(StateMiddleware(self._bot))


    def tell_admins(self, messages: Union[str, list[str]]):
        for admin_id in ADMIN_IDS:
            print("🐍 admin_id",admin_id)
            self._send_messages(chat_id=admin_id, messages=messages)


    def tell_super_admin(self, messages: Union[str, list[str]]):
        self._send_messages(chat_id=SUPER_ADMIN_ID, messages=messages)


    # ? send formatted messages
    # ? messages count should be equal to format variables
    def _send_messages(
        self,
        chat_id: int,
        messages: list[str],
        parse_mode="Markdown",
        format_variables: Union[str, int] = [],
        reply_markup: InlineKeyboardMarkup = None,
        disable_preview=False,
    ):

        # ? if format variables exist
        if len(format_variables) > 0:
            for message, format_variable in zip(messages, format_variables):
                formatted_message = message.format(format_variable)
                self._bot.send_message(
                    chat_id=chat_id,
                    text=formatted_message,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_preview,
                )

        # ? send simple messages
        else:
            for message in messages:
                self._bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_preview,
                )

    #! Придумать, как отправлять formatted_messages, когда нужно впихнуть несколько переменных в одну строку

