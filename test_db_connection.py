from pymongo import MongoClient
import os
from dotenv import load_dotenv
import os

load_dotenv()  # This loads variables from .env into os.environ

def test_mongo_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # List all databases
        dbs = client.list_database_names()
        print("MongoDB connected successfully!")
        print("Available Databases:", dbs)
    except Exception as e:
        print("MongoDB connection failed:", e)

if __name__ == "__main__":
    test_mongo_connection()


# test_mongo_connection.py

from mongo_db.mongo import get_mongo_client

def test_connection():
    try:
        client = get_mongo_client()
        db_names = client.list_database_names()
        print("✅ Connected to MongoDB Atlas")
        print("Available databases:", db_names)

        # Optional: check your specific DB/collection
        db = client["Admin"]  # replace with actual name
        collections = db.list_collection_names()
        print("Collections in DB:", collections)

    except Exception as e:
        print("❌ Failed to connect to MongoDB:", e)

if __name__ == "__main__":
    test_connection()


# check_mongo_users.py

from mongo_db.mongo_handler import get_user_from_mongo

username = "Admin"
user_doc = get_user_from_mongo(username)

if user_doc:
    print("✅ Found user in MongoDB:", user_doc)
else:
    print("❌ User not found in MongoDB.")


# check_all_users.py
from mongo_db.mongo import get_user_collection

users = get_user_collection().find()
print("📋 All users in MongoDB Atlas:")
for user in users:
    print(user)


# insert_test_user.py
from mongo_db.mongo import get_user_collection

user_collection = get_user_collection()
test_user = {
    "username": "Admin",
    "password": "test123",  # Ideally hashed
    "role": "admin"
}

# Insert only if not already there
if not user_collection.find_one({"username": "Admin"}):
    user_collection.insert_one(test_user)
    print("✅ Test user inserted.")
else:
    print("⚠️ User already exists.")


from mongo_db.mongo_handler import get_user_from_mongo

username = "Admin"
user_doc = get_user_from_mongo(username)

if user_doc:
    print("✅ Found user in MongoDB:", user_doc)
else:
    print("❌ User not found in MongoDB.")

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get Mongo URI
mongo_uri = os.getenv("MONGO_URI")
print("🔍 MONGO_URI from .env:", mongo_uri)

# Connect
client = MongoClient(mongo_uri)
print("✅ Connected to MongoDB at:", client.address)

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["dynamic_impact_tool"]

from pymongo import MongoClient

uri = "mongodb+srv://Admin:Admin@cluster0.wtjtgf3.mongodb.net/dynamic_impact_tool?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri, tls=True, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)


from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not set in .env file")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # force connection test
except ServerSelectionTimeoutError as e:
    raise RuntimeError("❌ MongoDB Atlas connection failed: " + str(e))

db = client["dynamic_impact_tool"]

from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("✅ MongoDB connection successful.")
except Exception as e:
    print("❌ MongoDB connection failed:", str(e))
