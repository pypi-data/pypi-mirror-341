from bot_engine.utils.Dotenv import Dotenv
from bot_engine.utils.Logger import Logger
#! Это нужно передавать в конструктор класса Cache и Database (?)
# from users.initial_users_list import INITIAL_USERS


class InitialUsers:
    _users_instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._users_instance is None:
            cls._users_instance = super(InitialUsers, cls).__new__(cls)
            # cls._users_instance.initial_users = INITIAL_USERS
            cls._users_instance.admin_ids = []
            
        return cls._users_instance
    
    
    def __init__(self):
        self.log = Logger().info
        self.initial_admins = 1
    
    
    def pin_ids_to_users(self) -> None:
        self.user_ids: list = Dotenv().user_ids
        print("🐍 self.user_ids (pin ids): ", self.user_ids)
        
        for user_id, user in zip(self.user_ids, self.initial_users):
            user["user_id"] = user_id
            user["chat_id"] = user_id

            # print("🐍 user (pin_ids_to_users): ", user)
            
        # self.log(f"ids for users pinned ☑")
        
        
    def get_admin_ids(self):
        if len(self.initial_users) > 0:
            for admin in self.initial_users[0:self.initial_admins]:
                self.admin_ids.append(admin["user_id"])
                
                # self.log(f"admin in cache: {admin}")
                # self.log(f"admin ids: {self.admin_ids}")
            return self.admin_ids
        else: 
            self.log(f"❌ no admins found! ")
            
            
    def get_user(self, user_id) -> dict:
         for user in self.initial_users:
            if user_id == user["user_id"]:
                return user
            
            
    def get_initial_users(self) -> list:
        # self.log(f"self.initial_users: { self.initial_users }")
        return self.initial_users