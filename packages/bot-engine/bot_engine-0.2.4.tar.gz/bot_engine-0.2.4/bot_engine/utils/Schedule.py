from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from bot_engine.utils.Logger import Logger
from bot_engine.languages.Languages import Language

from bot_engine.bot.Bot import Bot
from bot_engine.database.Database import Database

from bot_engine.database.MongoDB import MongoDB

# consts
SCHEDULE_DAYS = [
    {"id": 0, "name": "Понедельник", "lessons": ""},
    {"id": 1, "name": "Вторник", "lessons": ""},
    {"id": 2, "name": "Среда", "lessons": ""},
    {"id": 3, "name": "Четверг", "lessons": ""},
    {"id": 4, "name": "Пятница", "lessons": ""},
    {"id": 5, "name": "Суббота", "lessons": ""},
    {"id": 6, "name": "Воскресенье", "lessons": ""},
]

#! Previously Time.py

class Time:
    def __init__(self):
        self.log = Logger().info
        
        self.scheduler = BackgroundScheduler()
        
        self.bot = Bot()
        self.messages = Language().messages
        
        self.database = Database()
        
        
    def set_scheduled_tasks(self):
        self.set_weekly_tasks()
        self.set_monthly_tasks()
        
        self.scheduler.start()
        
        
        
    def set_weekly_tasks(self):
        self.scheduler.add_job(self.make_weekly_backup, CronTrigger(day_of_week='mon', hour=10, minute=0))
        self.log(f"Weekly tasks set! 🆗")
        

    def set_monthly_tasks(self):
        self.scheduler.add_job(self.make_monthly_data_refresh, 'cron', day='last', hour=10, minute=0)
        self.log(f"Monthly tasks set! 🆗")

    
    def get_current_time(self) -> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("Formatted date and time:", formatted_datetime)
        
        return formatted_datetime
        
        
    def make_monthly_data_refresh(self):
        self.bot.tell_admins(messages=self.messages["monthly_data_refresh"]["intro"])
        
        # updates user under the hood
        # ? no need to do "sync-cache-remote"
        Database().make_monthly_reset()
            
        self.log(f"Monthly reset completed 🤙")
        self.bot.tell_admins(messages=self.messages["monthly_data_refresh"]["success"])
            
        
    def make_weekly_backup(self):
        self.bot.tell_admins(messages=self.messages["weekly_replica"]["intro"])
        
        # replicate all collections
        MongoDB().replicate_collection(collection_name="users")
        MongoDB().replicate_collection(collection_name="versions")
        
        self.bot.tell_admins(messages=self.messages["weekly_replica"]["success"])
        
        
        
        
        