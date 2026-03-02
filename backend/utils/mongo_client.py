import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database():
    """
    Returns a pymongo database instance.
    The URI is fetched from the 'DATABASE_URL' or 'MONGO_URI' environment variable.
    """
    # Support both commonly used env vars
    mongo_uri = os.environ.get('MONGO_URI') or os.environ.get('DATABASE_URL')
    
    if not mongo_uri:
        raise ValueError("MONGO_URI or DATABASE_URL environment variable is not set. Cannot connect to MongoDB via PyMongo.")
        
    client = MongoClient(mongo_uri)
    
    # Parse the database name out of the URI if possible, or fallback to default
    db_name = os.environ.get('MONGO_DB_NAME', 'django_microservices_db')
    
    return client[db_name]

def get_collection(collection_name):
    """
    Helper function to get a specific MongoDB collection.
    """
    db = get_database()
    return db[collection_name]
