from os import getenv
from datetime import datetime

from typing import List, Optional
from telebot.types import Message


if getenv("ENVIRONMENT") == "testing":
    from data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID
    from data.config import USER_ID_KEY
    from users.UserT import UserT  

    from users.NewUser import NewGuest, NewUser

    from database.MongoDB import MongoDB
    from database.Cache import Cache

else:
    from bot_engine.data.env import ENVIRONMENT, BOT_TOKEN, ADMIN_IDS, SUPER_ADMIN_ID
    from bot_engine.data.config import USER_ID_KEY
    from bot_engine.users.UserT import UserT  

    from bot_engine.users.NewUser import NewGuest, NewUser

    from bot_engine.database.MongoDB import MongoDB
    from bot_engine.database.Cache import Cache



class Database:
    """ Higher-level class for syncing data in MongoDB and Cache (users, versions etc)"""

    _db_instance: Optional["Database"] = None
    Cache: Optional["Cache"] = None
    MongoDB: "MongoDB" = None
    

    def __new__(cls, *args, **kwargs):
        if cls._db_instance is None:
            cls._db_instance = super(Database, cls).__new__(cls)
            cls._db_instance.Cache = Cache()
            cls._db_instance.MongoDB = MongoDB()    
            
        return cls._db_instance
    
    
    def __init__(self):
        pass


    def add_user(self, new_user: UserT):
        self.MongoDB.add_user(new_user)
        self.Cache.cache_user(new_user)
    

    def add_users(self, users: list[UserT]):
        """saves user to MongoDB and Cache"""
        for user in users:
            self.MongoDB.add_user(user)
            self.Cache.cache_user(user)
        

    def get_users(self):
        return self.Cache.users
        

    #! reduce number of times this method has been called
    #! for super fast time-to-response
    #! Now it's called 3 times: Filters, / command and maybe somewhere else (use search for set_active_user)
    def get_active_user(self, message: Message):
        # self.log(f"looking for user_id { message.from_user.id }...")
        active_user = self.Cache.find_active_user(user_id=message.chat.id)
        
        if active_user:
            self.log(f"👌 this user is in cache: { active_user }")

            # add some data from telegram
            self.complete_user_profile(active_user, message)
            
            return active_user
        
        if not active_user:
            # self.log(f"👐 wow, it's someone new: { active_user }")
            new_guest = NewGuest(message).create_new_guest()
            
            self.MongoDB.add_user(new_guest)
            
            # cache user after it's being registered
            self.update_cache_users()
            return new_guest


    def remove_user(self, user_id: int = None) -> None:
        self.MongoDB.remove_user(user_id)
        self.Cache.remove_user(user_id)
        print(f"User fully removed from Database!")
         

    def sync_cache_and_remote_users(self):
        """ Sync users across sources: 
            1) initial users with mongoDB
            2) mongoDB with cache 
            3) make local backup if MongoDB data isn't available  
        """
        
        self.update_remote_users()
        self.update_cache_users()
    
            
    # def update_remote_users(self):
    #     # save initial users to database
    #     for initial_user in self.initial_users:
    #         filter_by_id = { "user_id": initial_user["user_id"] }
    #         is_user_exists_in_db = self.MongoDB.users_collection.find_one(filter=filter_by_id)
            
    #         if not is_user_exists_in_db:
    #             # self.log(f"❌ user doesn't exist, here's id: { initial_user["user_id"] }")

    #             new_user = NewUser().create_new_user(initial_user)
    #             # self.complete_user_profile(new_user)
                
    #             self.MongoDB.save_user(new_user)
            
    #         # if user exists:
    #         # self.log(f"✔ user exist: { initial_user["real_name"]}")


    # def update_cache_users(self):
    #     mongo_users = self.MongoDB.get_all_users()
        
    #     # self.log(f"mongo_users len: { len(mongo_users) }")
    #     # self.log(f"initial_users len: { len(self.initial_users) }")

    #     # no Mongo backup
    #     if not len(mongo_users) or len(mongo_users) == 0:
    #         self.cache_initial_users()
        
    #     # fetch users by default (once)
    #     else:
    #         self.cache_mongo_users()
            
        
            
    # def cache_initial_users(self):
    #     for initial_user in self.initial_users:
    #         new_user = NewUser().create_new_user(initial_user)
    #         self.Cache.cache_user(new_user)
            # self.cached_users.append(new_user)

        # self.log(f"🔀 saved initial users to cache: { self.cache.cached_users }")


    def cache_mongo_users(self):
        self.Cache.clean_users() # 1 user is left: admin
        mongo_users = self.MongoDB.get_all_users()
        
        #! Костыль detected
        #! skip first user from db: admin
        for mongo_user in mongo_users:
            self.Cache.cache_user(mongo_user)
            # self.cached_users.append(mongo_user)
            
        # self.log(f"🏡 cache filled with MongoDB: { self.cache.cached_users }")
            
            
    def clean_users(self):
        """ cleans users in MongoDB and Cache"""
        self.MongoDB.clean_users()
        self.Cache.clean_users()
        
        
    #? active user methods
    def complete_user_profile(self, active_user: dict, message: Message):
        # add first_name
        if not active_user.get("first_name"):
            self.update_user(user=active_user, key="first_name", new_value=message.from_user.first_name)
            # self.log(f"first_name updated: { message.from_user.first_name }")
            
        
        # add username
        if not active_user.get("username"):
            username = message.from_user.username 
            
            if username == None or username == "None":
                self.update_user(user=active_user, key="username", new_value="not set")
            else:
                self.update_user(user=active_user, key="username", new_value=username)
                
            # self.log(f"username updated: { message.from_user.username }")
        
        
    
    def get_real_name(self, active_user: dict):
        real_name = ""
        last_name = ""
        
        if active_user["access_level"] == "student" or active_user["access_level"] == "admin":
            real_name = active_user.get("real_name") 
            last_name = active_user.get("last_name")
        
        if active_user["access_level"] == "guest":
            real_name = active_user.get("first_name") 
        
        return real_name, last_name
    
    
    def update_user(self, user: dict, key: str, new_value: str | int | bool):
        self.MongoDB.update_user(user_id=user["user_id"], key=key, new_value=new_value)
        self.Cache.update_user(user_id=user["user_id"], key=key, new_value=new_value)
        
        real_name, last_name = self.get_real_name(user)
        self.log(f"📅 Пользователь обновлён (update_user): { real_name } { last_name }")


    #! maybe there's a need to separate this from Database class?
    def update_lessons(self, message: Message):
        # работа с данными, затем с кешом и монго
        active_user = self.get_active_user(message)
                
        if active_user["done_lessons"] < active_user["max_lessons"]:
            active_user["done_lessons"] += 1
        
        if active_user["lessons_left"] > 0:
            active_user["lessons_left"] -= 1
            
        self.update_user(user=active_user, key="done_lessons", new_value=active_user["done_lessons"])
        self.update_user(user=active_user, key="lessons_left", new_value=active_user["lessons_left"])
            
        return {
            "done_lessons": active_user["done_lessons"],
            "lessons_left": active_user["lessons_left"]
        }
        
    #! maybe there's a need to separate this from Database class?
    def check_done_reports_limit(self, max_lessons: int, done_lessons: int) -> bool:
        is_report_allowed = False
        
        limit_multiplier = 1

        if max_lessons == 8:
            limit_multiplier = 2
       
        if max_lessons == 12:
            limit_multiplier = 3
            
        
        #? Тут делаем проверку
        now = datetime.now()
        current_week_number = self.week_of_month(now)
        
        current_time = now.strftime(f"%d %B, %H:%M")

        print(f"Current time: {current_time}")
        print(f"Current week in month: {current_week_number}")
        
        allowed_reports_limit = current_week_number * limit_multiplier # 2 * 1 или 2 * 2
        print("🐍allowed_reports_limit: ", allowed_reports_limit)
        
        
        if done_lessons < allowed_reports_limit:
            is_report_allowed = True

        # else...        
        self.log(f"is_report_allowed: { is_report_allowed }")
        return is_report_allowed
        

    #! Вынести в класс Schedule
    def week_of_month(self, dt):
        first_day = dt.replace(day=1)
        date_of_month = dt.day
        adjusted_dom = date_of_month + first_day.weekday()  # Weekday ranges from 0 (Monday) to 6 (Sunday)
        return (adjusted_dom - 1) // 7 + 1
    

    #! Вынести в класс Schedule
    def make_monthly_reset(self):
        users = self.get_users()
        
        for user in users:
            #? reset lessons
            if user["access_level"] == "student":
                self.update_user(user=user, key="done_lessons", new_value=0)
                self.update_user(user=user, key="lessons_left", new_value=user["max_lessons"])
                self.update_user(user=user, key="payment_status", new_value=False)
            
        self.log(f"Monthly reset completed 🤙")


