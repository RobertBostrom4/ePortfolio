from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalDatabaseManager:
    def __init__(self, user='aacuser', password='Succees11!', host='nv-desktop-services.apporto.com', port=31194, db_name='AAC'):
        try:
            # Build the connection URI with the given credentials and connection details
            connection_uri = f"mongodb://{user}:{password}@{host}:{port}"
            # Create a MongoClient instance to manage the connection        
            self.client = MongoClient(connection_uri)
            # Access the database
            self.database = self.client[db_name]
        except Exception as e:
            print(e)
            raise
            
    # Inserts a new document into the animals collection
    def create(self, document):
        if not isinstance(document, dict) or not document:
            raise ValueError("Document must be a non-empty dictionary.")
        try:
            # Attempt to insert the document into the collection
            result = self.database.animals.insert_one(document)
            # Return True if an inserted_id is present
            return True if result.inserted_id else False
        except Exception as e:
            print(e)
            return False
        
    # Retrieves documents from the animals collection that match the query
    def read(self, query=None):
        if query is None:
            query = {}
        try:
            cursor = self.database.animals.find(query)
            return list(cursor)
        except Exception as e:
            print(e)
            return []
    # Updates document(s) in the animals collection that match the query   
    def update(self, query, update_data):
        if not isinstance(query, dict) or not query:
            raise ValueError("Query must be a non-empty dictionary.")
        if not isinstance(update_data, dict) or not update_data:
            raise ValueError("Update data must be a non-empty dictionary.")
        try:
            # Updating documents that match the query with the provided update data
            result = self.database.animals.update_many(query, {'$set': update_data})
            # Returns the count of documents that were modified
            return result.modified_count
        except Exception as e:
            print(e)
            return 0
    # Deletes document(s) from the animals collection that match the query.
    def delete(self, query):
        if not isinstance(query, dict) or not query:
            raise ValueError("Query must be a non-empty dictionary.")
        try:
            # Deleting documents that match the query
            result = self.database.animals.delete_many(query)
            # Returns the number of documents deleted
            return result.deleted_count
        except Exception as e:
            # This prints the exception and returns 0 if the deletion fails
            print(e)
            return 0
