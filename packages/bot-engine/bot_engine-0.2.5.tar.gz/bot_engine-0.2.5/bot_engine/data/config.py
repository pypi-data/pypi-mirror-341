#? Keys named same as in Telegram's API
USER_ID_KEY = "user_id"
CHAT_ID_KEY = "chat_id"

USER_COLLECTION = "users"
DATABASE_CONNECTIONS_LIMIT=1


def change_db_connections_limit(new_value: int):
    global DATABASE_CONNECTIONS_LIMIT
    DATABASE_CONNECTIONS_LIMIT = int(new_value)

def change_users_collection_name(new_value: str):
    global USER_COLLECTION
    USER_COLLECTION = new_value