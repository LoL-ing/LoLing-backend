from pymongo import MongoClient
from os import environ
from dotenv.main import load_dotenv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()

def get_db_connection():
    print("--db connect 시작 --")
    print("Mongo_user_name", environ['MONGO_USERNAME'])
    print("Mongo_user_pwd", environ['MONGO_PASSWORD'])
    client = MongoClient(f"mongodb+srv://{environ['MONGO_USERNAME']}:{environ['MONGO_PASSWORD']}@private-k.rxdi7.mongodb.net/?retryWrites=true&w=majority")
        
    print("--db connect 끝 --")
    return client['LoLing']


