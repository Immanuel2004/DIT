# # mongo_db/check_saved_chats.py
# from mongo_db.mongo import get_mongo_client
# import os
# from dotenv import load_dotenv
# load_dotenv()

# mongo_uri = os.getenv("MONGO_URI")
# username = "data_comparison"

# client = get_mongo_client()
# db = client["chat_db"]  # or whatever your DB name is
# collection = db["chat_history"]  # 👈 make sure this is chat_history

# history = list(collection.find({"username": username}))

# if history:
#     print(f"Found {len(history)} messages for {username} in chat_history")
#     for msg in history:
#         print(msg)
# else:
#     print("No chat history found in chat_history.")


# from mongo_db.mongo import get_chat_history_collection

# username = "data_comparison"
# collection = get_chat_history_collection()

# history = list(collection.find({"username": username}))

# if history:
#     print(f"Found {len(history)} messages for {username} in chat_history")
#     for msg in history:
#         print(msg)
# else:
#     print("No chat history found in chat_history.")
