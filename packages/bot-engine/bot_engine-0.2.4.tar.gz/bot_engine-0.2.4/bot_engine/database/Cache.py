from os import getenv

if getenv("ENVIRONMENT") == "testing":
    from data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID
    from data.config import USER_ID_KEY
    from users.UserT import UserT    
    from users.NewUser import NewUser

else:
    from bot_engine.data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID
    from bot_engine.data.config import USER_ID_KEY
    from bot_engine.users.NewUser import NewUser
    from bot_engine.users.UserT import UserT    



class Cache:
    _cache_instance: "Cache" = None
    users: list[UserT] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._cache_instance is None:
            cls._cache_instance = super().__new__(cls)
            cls._cache_instance.users = []
        
        return cls._cache_instance
    
    def __init__(self):
        pass
    
            
    def cache_user(self, new_user: UserT) -> None:
        is_user_in_cache = self.check_if_user_exists(new_user[USER_ID_KEY])

        if is_user_in_cache:
            return
        else: 
            self.users.append(new_user)
        
        
    def get_users_from_cache(self) -> list:
        if len(self.users) > 0:
            # self.log(f"🟢 users in cache: { self.cached_users }")
            return self.users
        else:
            # self.log(f"❌ no users in cache: { self.cached_users }")
            return []
    
    
    def get_admin_ids(self) -> list:
        # self.log(f"admin ids: { self.admin_ids }")
        return self.admin_ids
    
    
    def find_active_user(self, user_id):
        # self.log(f"user_id (Cache.find_active_user): { user_id }")
        for user in self.users:
            # self.log(f"user: { user }")
            if user["user_id"] == user_id:
                return user
        # if user not found
        return None
    

    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        for user in self.users:
            if user["user_id"] == user_id:
                user[key] = new_value
                
                # real_name, last_name = Database().get_real_name(active_user=user)
                # self.log(f"user { user_name } updated: key: {key} and value {new_value}")
                
    def get_user(self, user_id: int) -> dict:
        for user in self.users:
            if user["user_id"] == user_id:
                return user
            
            
    def remove_user(self, user_id: int) -> None:
        for cache_user in self.users:
            if user_id == cache_user["user_id"]:
                self.users.remove(cache_user)
                print(f"User removed from cache!")
                
    
    def check_if_user_exists(self, user_id: int) -> bool:
        for user in self.users:
            if user[USER_ID_KEY] == user_id:
                print(f"🟡 user exists in Cache: {user_id}")
                return True
            else:
                print(f"🔴 user doesn't exists in Cache: {user_id}")
                return False
        

    
    def find_user_by_property(self, property_name, value):
        for user in self.users:
            if property_name in user:
                if value == user[property_name]:
                    print("🐍 user (find_user_by_property): ",user)
                    return user
                

    def clean_users(self):
        """ cleans all users, except super_admin """
        self.users = []
        
        for user in self.users:
            if user[USER_ID_KEY] == SUPER_ADMIN_ID:
                pass
            else:
                self.users.remove(user)
        
        print(f"Кеш пользователей очищен! 🧹\n{self.users}")
