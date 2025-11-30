from pymongo import MongoClient 
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self):
        
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'MiiUnHy02i1L3' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # C in CRUD (Create)
    def create(self, data):
        if data is None:
            raise ValueError("Nothing to save, because data parameter is empty")
        try:
            result = self.collection.insert_one(data)
            return bool(result.inserted_id)
        except PyMongoError:
            return False
        
    # R in CRUD (Read)
    def read(self, query):
        if query is None:
            return []
        if "_id" in query and isinstance(query["_id"], str):
            try:
                query["_id"] = ObjectId(query["_id"])
            except Exception:
                return []
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError:
            return []
        
    # U in CRUD (Update)
    def update(self, query, update_values, upsert=False, multi=False):
        """Update documents matching 'query' with update_values.
           'update_values' should be a dict of fields to set (not full replacement).
           If multi=True, uses update_many; otherwise update_one.
           Returns true if at least one document was modified (or upserted when upsert=True), else False.
        """
        if query is None or update_values is None:
            raise ValueError("query and update values must be provided")
        try:
            update_doc = {"$set": update_values}
            if multi:
                result = self.collection.update_many(query, update_doc, upsert=upsert)
                return (result.modified_count > 0) or (upsert and result.upserted_id is not None)
            else:
                result = self.collection.update_one(query, update_doc, upsert=upsert)
                return (result.modified_count > 0) or (upsert and result.upserted_id is not None)
        except PyMongoError:
            return False
    
    # D in CRUD
    def delete (self, query, multi=False):
        """
        Delete documents matching query.
        If multi is True, delets all matching documents; otherwise deletes a single document.]
        Returns True if at least one document was deleted, else False.
        """
        if query is None:
            raise ValueError("query must be provided")
        try:
            if multi:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except PyMongoError:
            return False