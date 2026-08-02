from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("databaseURI")
print(mongo_uri)
client = MongoClient(mongo_uri)
db = client["youtubeRAG"]
user_collection = db["user"]
