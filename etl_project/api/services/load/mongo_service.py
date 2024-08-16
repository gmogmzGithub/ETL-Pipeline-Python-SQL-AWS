from pymongo import MongoClient
from bson import ObjectId

class MongoService:
    @staticmethod
    def get_mongo_client():
        # Replace with your connection details
        client = MongoClient('mongodb://localhost:27017/')
        return client

    @staticmethod
    def insert_transformed_data(data, db_name='etl_database', collection_name='transformed_data'):
        client = MongoService.get_mongo_client()
        db = client[db_name]
        collection = db[collection_name]

        # Insert data into MongoDB
        if isinstance(data, list):  # Insert multiple documents
            result = collection.insert_many(data)
            # Convert inserted ids to strings
            inserted_ids = [str(inserted_id) for inserted_id in result.inserted_ids]
            return inserted_ids
        else:  # Insert a single document
            result = collection.insert_one(data)
            return str(result.inserted_id)