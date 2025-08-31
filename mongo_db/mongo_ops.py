# from mongo_db.mongo import get_chat_collection, get_file_collection
# from pymongo import MongoClient
# from datetime import datetime
# from bson.json_util import dumps

# def save_chat(username, message, response):
#     get_chat_collection().insert_one({
#         "username": username,
#         "message": message,
#         "response": response
#     })

# def load_user_chats(username):
#     return list(get_chat_collection().find({"username": username}))

# def save_uploaded_file(username, filename, metadata=None):
#     get_file_collection().insert_one({
#         "username": username,
#         "filename": filename,
#         "metadata": metadata or {}
#     })

# def load_user_files(username):
#     return list(get_file_collection().find({"username": username}))

# client = MongoClient("mongodb://localhost:27017/")
# db = client["streamlit_chat_db"]
# chats_collection = db["chats"]

# def get_user_chats(username):
#     """
#     Retrieve all chat sessions for a given user from MongoDB.
#     Returns a list of sessions with messages grouped by date.
#     """
#     results = chats_collection.find({"username": username}).sort("timestamp", -1)
#     chat_sessions = []

#     for doc in results:
#         session = {
#             "date": doc.get("timestamp", datetime.now()).strftime("%Y-%m-%d %H:%M"),
#             "messages": doc.get("messages", [])
#         }
#         chat_sessions.append(session)

#     return chat_sessions

# from mongo_db.mongo import get_mongo_client
# from bson.binary import Binary

# def get_user_files(username):
#     client = get_mongo_client()
#     db = client['streamlit_chat_db']
#     files_collection = db['files']
    
#     user_files = list(files_collection.find({"username": username}))
    
#     # Optionally decode binary file content
#     for file in user_files:
#         if isinstance(file.get("content"), Binary):
#             file["content"] = file["content"]  # Leave as-is or decode if needed
    
#     return user_files


# mongo_db/mongo_ops.py
import os
from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

from mongo_db.mongo import (
    get_chat_collection,
    get_file_collection,
    get_mongo_client
)
from datetime import datetime
from bson.binary import Binary

# === Save / Load Chats ===
def save_chat(username, message, response):
    get_chat_collection().insert_one({
        "username": username,
        "message": message,
        "response": response,
        "timestamp": datetime.utcnow()
    })

def load_user_chats(username):
    return list(get_chat_collection().find({"username": username}).sort("timestamp", 1))

# === Save / Load Uploaded Files ===
def save_uploaded_file(username, filename, metadata=None):
    get_file_collection().insert_one({
        "username": username,
        "filename": filename,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow()
    })

def load_user_files(username):
    return list(get_file_collection().find({"username": username}).sort("timestamp", -1))

# === Get Chat Sessions (Grouped if needed) ===
def get_user_chats(username):
    db = get_mongo_client()["dynamic_impact_tool"]

    chats_collection = db["chats"]

    results = chats_collection.find({"username": username}).sort("timestamp", -1)
    chat_sessions = []

    for doc in results:
        session = {
            "date": doc.get("timestamp", datetime.now()).strftime("%Y-%m-%d %H:%M"),
            "messages": doc.get("messages", [])
        }
        chat_sessions.append(session)

    return chat_sessions

# === Get Uploaded Files ===
def get_user_files(username):
    db = get_mongo_client()["dynamic_impact_tool"]
    files_collection = db["files"]

    user_files = list(files_collection.find({"username": username}).sort("timestamp", -1))

    for file in user_files:
        if isinstance(file.get("content"), Binary):
            file["content"] = file["content"]  # You can decode it if needed

    return user_files

from mongo_db.mongo import get_chat_history_collection
# === Save to Chat History ===
def save_chat_to_history(username, user_message, ai_response):
    get_chat_history_collection().insert_many([
        {
            "username": username,
            "role": "user",
            "content": user_message,
            "timestamp": datetime.utcnow()
        },
        {
            "username": username,
            "role": "ai",
            "content": ai_response,
            "timestamp": datetime.utcnow()
        }
    ])

# === Load Chat History ===
def load_chat_history(username):
    return list(get_chat_history_collection().find({"username": username}).sort("timestamp", 1))
