from os import getenv
from typing import Union

from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message, CallbackQuery

if getenv("ENVIRONMENT") == "testing":
    from database.Database import Database

else:
    from bot_engine.database.Database import Database


class AccessLevelFilter(AdvancedCustomFilter):
    key = 'access_level'

    def __init__(self, bot):
        self.bot = bot
        

    def check(self, message: Union[Message, CallbackQuery], access_level: str):
        print(f"Filters (check)")
        
        #? if user replies with a keyboard
        if not hasattr(message, 'chat'):
            self.log(f"no message.chat found: { message.message.chat.id }")
            message = message.message
            
        
        active_user = Database().get_active_user(message)

        # if a list...
        if isinstance(access_level, list):
            return active_user["access_level"] in access_level
       

