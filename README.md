# Project: CRUD Python module for MongoDB (AnimalShelter) 🐾

## Purpose 🎯
  * Provide a simple, reusable Python CRUD layer for an `animals` collection in MongoDB, focused on Animal Shelter data and workflows.

## Driver used 🧭
  * `pymongo` - the official MongoDB Python driver.

Module: `AnimalShelter` (summary) 🏷️
  * Purpose: Encapsulate CRUD operations for aac.animals
  * Connection (in `__init__`): uses pymongo.MongoClient with configurable USER/PASS/HOST/PORT/DB/COL
  * Security note 🔒: do NOT hard-code credentials in production — use environment variables or a secrets manager.

---
# Methods & behavior 🔁

* create(self, data) ➕
    * Inserts a single document.
    * Raises ValueError if `data` is None.
    * Returns True on success, False on failure.
 

* read(self, query) 🔎
    * Returns a list of documents matching `query`.
    * If `_id` provided as string, attempts conversion to `ObjectId`.
    * Returns [] for None query or on failure.
 
* update(self, query, update_values, upsert=False, multi=False) ✏️
    * Performs `$set` with `update_values`.
    * `multi=True` uses `update_many`; otherwise `update_one`.
    * `upsert=True` allows insert when no match.
    * Returns True if modified or upserted; False otherwise.
 
* delete(self, query, multi=False) 🗑️
    * `multi=True` uses `delete_many`; otherwise `delete_one`.
    * Returns True if at least one document was deleted; False otherwise.
 
## Error handling & validation ⚠️

  * Methods raise ValueError for missing required inputs.
  * PyMongo errors are caught and result in False or empty results as appropriate.

