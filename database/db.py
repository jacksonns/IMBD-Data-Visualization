from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def imdb_database():
    load_dotenv()

    client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))

    return client["imdb"]
