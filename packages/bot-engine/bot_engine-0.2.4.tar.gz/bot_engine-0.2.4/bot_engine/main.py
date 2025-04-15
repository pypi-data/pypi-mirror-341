from data.env import SUPER_ADMIN_ID
from data.initial_users import INITIAL_USERS

from server.FastAPIServer import FastAPIServer
from bot.Bot import Bot
from database.Database import Database




# bot = Bot()

# super_admin_messages = ["Привет, Дамир!\nБот запущен!"]
# admin_messages = ["Привет, админ!\nБот запущен!"]
# bot._send_messages(chat_id=SUPER_ADMIN_ID, messages=messages)
# bot.tell_super_admin(super_admin_messages)

# not_formatted_messages = ["Привет, {}", "Я - бот-помощник {}!"]
# format_variables = ["Юзер", "Дамира"]
# bot.tell_admins(admin_messages)

# bot.start()

# bot._send_messages(
#     chat_id=SUPER_ADMIN_ID,
#     messages=not_formatted_messages,
#     format_variables=format_variables,
# )



db = Database()

# db.clean_users()
db.add_users(INITIAL_USERS)

print(db.Cache.users)