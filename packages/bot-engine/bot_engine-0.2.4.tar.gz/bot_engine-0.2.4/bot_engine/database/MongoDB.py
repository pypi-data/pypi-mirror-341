# from calendar import c
from os import getenv
from datetime import datetime, timedelta

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

if getenv("ENVIRONMENT") == "testing":
    from data.env import ENVIRONMENT, MONGODB_TOKEN, DATABASE_NAME, REPLICA_NAME, SUPER_ADMIN_ID
    from data.config import USER_ID_KEY, USER_COLLECTION, DATABASE_CONNECTIONS_LIMIT
    from users.UserT import UserT

else:
    from bot_engine.data.env import ENVIRONMENT, MONGODB_TOKEN, DATABASE_NAME, REPLICA_NAME, SUPER_ADMIN_ID
    from bot_engine.data.config import USER_ID_KEY, USER_COLLECTION,DATABASE_CONNECTIONS_LIMIT
    from bot_engine.users.UserT import UserT


#! data has to be created manually, but can be add as consts
# from languages.Ru import MONTHS_RU
# from data.schedule_days import SCHEDULE_DAYS


class MongoDB:
    _mongoDB_instance = None
    _client: MongoClient = None

    database: Database = None
    replica_db: Database = None

    def __new__(cls, *args, **kwargs):
        if cls._mongoDB_instance is None:
            cls._mongoDB_instance = super().__new__(cls)
            cls._mongoDB_instance._client = MongoClient(MONGODB_TOKEN, maxPoolSize=DATABASE_CONNECTIONS_LIMIT)
            cls._mongoDB_instance.database = cls._mongoDB_instance._client[DATABASE_NAME]
            cls._mongoDB_instance.replica_db = cls._mongoDB_instance._client[
                REPLICA_NAME
            ]
            print(f"🏗 База данных {DATABASE_NAME} подключена!")

        return cls._mongoDB_instance


    def __init__(self) -> None:
        # ? bot's collections
        self.users_collection: Collection = self.database[USER_COLLECTION]
        self.versions_collection: Collection = self.database["versions"]
        self.schedule_collection: Collection = self.database["schedule"]

        #? handles schedule days
        # self.ScheduleDays = ScheduleDays(self.schedule_collection)


    def show_users(self):
        print(f"Коллекция юзеров: {list(self.users_collection.find({}))}")


    def get_all_users(self):
        return list(self.users_collection.find({}))


    def get_all_versions(self):
        return list(self.versions_collection.find({}))


    def get_replica_documents(self, collection_name="users"):
        return list(self.replica_db[collection_name].find({}))


    def get_all_documents(self, database_name="school-bot", collection_name="users"):
        database = self._client[database_name]

        return list(database[collection_name].find({}))


    def check_if_user_exists(self, user_id: int):
        """returns True if user is in the collection, False - if not"""
        user = self.users_collection.find_one({USER_ID_KEY: user_id})

        if user:
            return True
        else:
            return False


    #! Ещё оно должно формировать NewUser / NewGuest
    def add_user(self, new_user: UserT) -> None:
        user_is_in_db = self.check_if_user_exists(new_user[USER_ID_KEY])

        if not user_is_in_db:
            self.users_collection.insert_one(new_user)
            print(f"🟢 Юзер с id { new_user[USER_ID_KEY] } сохранён в БД")
        else: 
            print(f"🟡 Юзер с id { new_user[USER_ID_KEY] } уже есть в БД")


    def remove_user(self, user_id: int) -> None:
        filter = {"user_id": user_id}
        self.users_collection.delete_one(filter=filter)
        print(f"User removed from MongoDB!")


    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        filter_by_id = {USER_ID_KEY: user_id}
        update_operation = {"$set": {key: new_value}}

        self.users_collection.update_one(filter=filter_by_id, update=update_operation)


    # ? Admin commands
    def clean_users(self):
        delete_filter = {USER_ID_KEY: {"$nin": [SUPER_ADMIN_ID]}}
        # delete_filter = {}

        self.users_collection.delete_many(filter=delete_filter)
        print(f"🧹 Коллекция users очищена (все, кроме админа {SUPER_ADMIN_ID})!")


    # ? Versions
    def get_latest_versions_info(self, versions_limit: int = 3):
        self.versions_collection = self.database["versions"]
        latest_versions = list(
            self.versions_collection.find({}).sort("id", -1).limit(versions_limit)
        )

        latest_versions.reverse()
        print("🐍 latest_versions from mongo: ", latest_versions)

        return latest_versions


    def send_new_version_update(self, version_number: int, changelog: str):
        now = datetime.now()

        if ENVIRONMENT == "production":
            now = now + timedelta(hours=3)

        #! 
        # current_time = now.strftime(f"%d {MONTHS_RU[now.month]}, %H:%M")

        versions_count = self.versions_collection.count_documents({})

        new_update = {
            "id": versions_count + 1,
            # "date": current_time,
            "version": version_number,
            "changelog": changelog,
        }

        self.versions_collection.insert_one(new_update)

        print(f"⌛ New version { version_number } published! ")


    def replicate_collection(self, collection_name: str = "users"):
        """replicates users or versions collection"""
        existing_documents = self.get_all_users()

        if collection_name == "versions":
            existing_documents = self.get_all_versions()

        replica_collection = self.replica_db[collection_name]

        # ? clear replica
        replica_collection.delete_many({})
        replica_collection.insert_many(existing_documents)

        print(f"Коллекция {collection_name} успешно реплицирована 🐱‍🐉")


    def load_replica(self, collection_name: str = "users"):
        collection_to_erase = self.database[collection_name]
        collection_to_erase.delete_many({})

        new_documents = self.get_all_documents(
            database_name="replica", collection_name=collection_name
        )

        collection_to_erase.insert_many(new_documents)

        print(
            f"Коллекция {collection_name} успешно восстановлена из реплики в основную базу данных! 🐱‍🐉"
        )


class ScheduleDays:
    def __init__(self, schedule_collection: Collection):
        self.schedule_collection = schedule_collection
        self.days = list(schedule_collection.find({}))
        # print("🐍 self.days", self.days)

    def get_days(self):
        return list(self.schedule_collection.find({}))
    
    #? get scheduled lessons from a specific day
    def get_schedule(self, day_id: int) -> str: 
        day = self.schedule_collection.find_one(filter={"id": day_id})
        print("🐍 day info (mongo): ",day)
        return day["lessons"] 

    def check_days_integrity(self):
        if len(self.days) < 7:
            print("Не все дни в порядке...")
            self.create_days()
        else: print("Все 7 дней расписания на месте!")

    #! depends on SCHEDULE_DAYS
    # def create_days(self):
    #     for day in SCHEDULE_DAYS:
    #         self.schedule_collection.insert_one(day)
    #         print(f"day {day} created in schedule!")
    
    #! depends on SCHEDULE_DAYS
    # def change_day_schedule(self, day_id: int, new_schedule: str):
    #     self.schedule_collection.update_one(filter={"id": day_id}, update={"$set": {"lessons": new_schedule} })
    #     print(f"Schedule for { SCHEDULE_DAYS[day_id]["name"]} successfully changed! ")

    def create_schedule_messages(self):
        days = self.get_days()
        messages = []

        for day in days:
            # print(f"day: {day}")
            if day["lessons"] != "":
                messages.append(day["lessons"])
            
            print("🐍 messages: ",messages)
        
        return messages
    
    def clear_schedule(self):
        self.schedule_collection.update_many({}, {"$set": {"lessons": ""}})
        print("Schedule cleared!")
