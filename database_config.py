from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("databaseURI")
client = MongoClient(mongo_uri)
db = client["youtubeRAG"]
user_collection = db["user"]
