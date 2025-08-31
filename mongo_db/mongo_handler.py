# # mongo_db/mongo_handler.py

# from mongo_db.mongo import get_chat_collection, get_file_collection
# from datetime import datetime
# from mongo_db.mongo import get_mongo_client

# def save_chat(username, message, response):
#     get_chat_collection().insert_one({
#         "username": username,
#         "role": "user",
#         "content": message,
#         "timestamp": datetime.now()
#     })
#     get_chat_collection().insert_one({
#         "username": username,
#         "role": "ai",
#         "content": response,
#         "timestamp": datetime.now()
#     })

# def load_user_chats(username):
#     return list(get_chat_collection().find({"username": username}).sort("timestamp", 1))

# def save_uploaded_file(username, filename, metadata=None):
#     get_file_collection().insert_one({
#         "username": username,
#         "filename": filename,
#         "metadata": metadata or {},
#         "timestamp": datetime.now()
#     })

# def load_user_files(username):
#     return list(get_file_collection().find({"username": username}).sort("timestamp", 1))


# def get_user_uploads(email: str):
#     client = get_mongo_client()
#     db = client["Dynamic_Impact_Tool"]  
#     collection = db["uploads"]
#     uploads = list(collection.find({"email": email}, {"_id": 0}))
#     return uploads


# def get_user_chats(email: str):
#     client = get_mongo_client()
#     db = client["Dynamic_Impact_Tool"]
#     collection = db["chats"]
#     chats = list(collection.find({"email": email}, {"_id": 0}))
#     return chats

import os
from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

from mongo_db.mongo import get_chat_collection, get_file_collection
from datetime import datetime
from mongo_db.mongo import get_mongo_client

def save_chat(username, message, response):
    get_chat_collection().insert_one({
        "username": username,
        "role": "user",
        "content": message,
        "timestamp": datetime.now()
    })
    get_chat_collection().insert_one({
        "username": username,
        "role": "ai",
        "content": response,
        "timestamp": datetime.now()
    })

def load_user_chats(username):
    return list(get_chat_collection().find({"username": username}).sort("timestamp", 1))

def save_uploaded_file(username, filename, metadata=None):
    get_file_collection().insert_one({
        "username": username,
        "filename": filename,
        "metadata": metadata or {},
        "timestamp": datetime.now()
    })

def load_user_files(username):
    return list(get_file_collection().find({"username": username}).sort("timestamp", 1))


def get_user_uploads(username: str):
    client = get_mongo_client()
    db = client["dynamic_impact_tool"]
    collection = db["files"]
    uploads = list(collection.find({"username": username}, {"_id": 0}))
    return uploads

def get_user_chats(username: str):
    client = get_mongo_client()
    db = client["dynamic_impact_tool"]
    collection = db["chats"]
    chats = list(collection.find({"username": username}, {"_id": 0}))
    return chats


from .mongo import get_user_collection

def get_user_from_mongo(username):
    user_collection = get_user_collection()
    return user_collection.find_one({"username": username})

from mongo_db.mongo import get_chat_history_collection

def save_chat_to_history(username, message, response):
    get_chat_history_collection().insert_many([
        {
            "username": username,
            "role": "user",
            "content": message,
            "timestamp": datetime.now()
        },
        {
            "username": username,
            "role": "ai",
            "content": response,
            "timestamp": datetime.now()
        }
    ])

def load_chat_history(username):
    return list(get_chat_history_collection().find({"username": username}).sort("timestamp", 1))
