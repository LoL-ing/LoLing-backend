from pymongo import MongoClient
from os import environ
from dotenv.main import load_dotenv

load_dotenv()

def get_db_connection():
    print("--db connect 시작 --")
    client = MongoClient(f"mongodb+srv://{environ['MONGO_USERNAME']}:{environ['MONGO_PASSWORD']}@private-k.rxdi7.mongodb.net/?retryWrites=true&w=majority")
    print("--db connect 끝 --")
    return client['LoLing']


