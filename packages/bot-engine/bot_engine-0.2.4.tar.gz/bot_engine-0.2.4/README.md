The universal bot engine framework. Made on top of pytelegrambotapi

# Starting your development journey

## Step 1. .env file example

Example of ready-to-work .env file:
```
ENVIRONMENT=development
PORT=8000

BOT_TOKEN=your_token
MONGODB_TOKEN=your_token

ADMIN_IDS=1,2
SUPER_ADMIN_ID=1
```

### Accessing .env data

You can import all this variables from bot_engine.data.env file. 
There you will see ready-to-use constants loaded right from your .env file.


## Step 2. First users! (optional)

You can easily create initial users in your DB by doing this:

1. Create folder "data" with a file "initials_users.py". Place an array of initial users with dictionaries:

INITIAL_USERS = 
[
    {
        "real_name": "Valeriy",
        "id": 123,
        "access_level": "user" or "admin",
        "any_other_data": any,
    },
    ...
]

Then call method Database().add_users(INITIAL_USERS) to fill your DB with initial users. This is an optional one-time operation for setting up your first users in DB. That's simple!


### A data security minute

You can leave the file "initials_users.py" in your project. Just add it to .gitignore to prevent the leakout of the data.


## Step 3. Run the bot

Call Bot().start() to start bot. It handles all .env file data automatically using data/env.py file - no need to import / load your .env data  
