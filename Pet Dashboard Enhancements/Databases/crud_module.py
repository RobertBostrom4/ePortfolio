from __future__ import annotations

from dotenv import load_dotenv
import os

load_dotenv()

from typing import Iterable, Optional, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

import pandas as pd

class AnimalDatabaseManager:
    """
    This class handles database operations for the Grazioso Salvare project.
    As a student, I wanted to build a clean separation between my database logic and the app logic.
    This made it easier to test, reuse, and enhance just the data layer without touching the UI.
    """

    def __init__(self):
        try:
            # As a best practice, I'm loading my DB credentials from a .env file.
            # This avoids hardcoding sensitive values and makes the app more secure and portable.
            username = os.getenv('MONGO_USER')
            password = os.getenv('MONGO_PASSWORD')
            host = os.getenv('MONGO_HOST')
            port = int(os.getenv('MONGO_PORT'))
            db_name = os.getenv('MONGO_DB')

            # Construct the MongoDB URI (authSource is required for SNHU's Apporto environment).
            connection_uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=AAC"
            self.client = MongoClient(connection_uri)
            self.database = self.client[db_name]
        except Exception as e:
            print("Error connecting to MongoDB:", e)
            raise

        # I'm using a simple in-memory cache to avoid re-querying MongoDB with the same filters.
        # This is especially useful for filtering since many filters are repeated often.
        self._read_cache: dict[Tuple, list[dict]] = {}

    @property
    def animals(self) -> Collection:
        # Shortcut to access the animals collection from the database.
        return self.database.animals

    @staticmethod
    def _normalize_query(query: Optional[dict]) -> dict:
        # Helper to ensure we always work with a dictionary, even if None is passed.
        return query or {}

    @staticmethod
    def _normalize_fields(fields: Optional[Iterable[str]]) -> Optional[dict]:
        """
        Converts a list of field names into a MongoDB projection dictionary.
        Projection reduces the amount of data transferred from MongoDB.
        I added this to improve performance by only fetching fields we actually use.
        """
        if not fields:
            return None
        proj = {f: 1 for f in fields}
        proj['_id'] = 1  # Always include _id for internal handling (we'll remove or convert it later).
        return proj

    @staticmethod
    def _cache_key(query: dict, fields: Optional[Iterable[str]]) -> Tuple:
        # Creates a unique and deterministic cache key based on query and fields.
        q_tuple = tuple(sorted(query.items()))
        f_tuple = tuple(sorted(list(fields))) if fields else None
        return (q_tuple, f_tuple)

    def _cache_get(self, key: Tuple) -> Optional[list[dict]]:
        return self._read_cache.get(key)

    def _cache_set(self, key: Tuple, docs: list[dict]) -> None:
        self._read_cache[key] = docs

    def clear_cache(self) -> None:
        self._read_cache.clear()

    def create(self, document: dict) -> bool:
        if not isinstance(document, dict) or not document:
            raise ValueError("Document must be a non-empty dictionary.")
        try:
            result = self.animals.insert_one(document)
            self.clear_cache()  # Clear the cache since the data changed.
            return True if result.inserted_id else False
        except Exception as e:
            print(e)
            return False

    def read(self, query: Optional[dict] = None, projection: Optional[dict] = None,
             *, sort: Optional[list] = None, limit: int = 0, use_cache: bool = True) -> list[dict]:
        """
        Generic read wrapper around MongoDB's find() method.
        I added caching and field projection support to reduce workload and improve responsiveness.
        """
        query = self._normalize_query(query)

        fields = None
        if projection is not None:
            fields = [k for k in projection.keys() if k != '_id']
        key = self._cache_key(query, fields)
        if use_cache:
            cached = self._cache_get(key)
            if cached is not None:
                return cached

        try:
            cursor = self.animals.find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            docs = list(cursor)
            if use_cache:
                self._cache_set(key, docs)
            return docs
        except Exception as e:
            print(e)
            return []

    def update(self, query: dict, update_data: dict) -> int:
        if not isinstance(query, dict) or not query:
            raise ValueError("Query must be a non-empty dictionary.")
        if not isinstance(update_data, dict) or not update_data:
            raise ValueError("Update data must be a non-empty dictionary.")
        try:
            result = self.animals.update_many(query, {'$set': update_data})
            self.clear_cache()
            return result.modified_count
        except Exception as e:
            print(e)
            return 0

    def delete(self, query: dict) -> int:
        if not isinstance(query, dict) or not query:
            raise ValueError("Query must be a non-empty dictionary.")
        try:
            result = self.animals.delete_many(query)
            self.clear_cache()
            return result.deleted_count
        except Exception as e:
            print(e)
            return 0

    def read_df(self, query: Optional[dict] = None, *, fields: Optional[Iterable[str]] = None,
                force_refresh: bool = False) -> pd.DataFrame:
        """
        This is a helper function I created to convert MongoDB results directly into a pandas DataFrame.
        It uses the caching and projection features I built above, and then cleans the data.
        This helped me bridge database access with my dashboard in a structured way.
        """
        projection = self._normalize_fields(fields)
        docs = self.read(query, projection, use_cache=not force_refresh)
        df = pd.DataFrame.from_records(docs)
        df = self._clean_df(df)
        return df

    @staticmethod
    def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans up the DataFrame returned by MongoDB:
        - Converts ObjectId to strings
        - Drops _id column (to avoid breaking Dash tables)
        - Converts numeric fields safely
        - Strips whitespace from string fields
        
        I added this to make sure the data is safe to use in Dash without type errors.
        """
        if df.empty:py
            return df

        if '_id' in df.columns:
            try:
                df['_id'] = df['_id'].astype(str)
            except Exception:
                df['_id'] = df['_id'].apply(lambda x: str(x))
            df = df.drop(columns=['_id'])

        for col in ('age_upon_outcome_in_weeks', 'location_lat', 'location_long'):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in ('name', 'breed', 'animal_type', 'sex_upon_outcome'):
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        return df
