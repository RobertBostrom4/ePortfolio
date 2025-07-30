# NOTE: For my second enhancement (Algorithms and Datastructures), it further improves from my initial enhancements. They are as follows:
#   * Field projection (return only needed columns)
#   * Cached reads (avoid repeated network calls)
#   * Convenience read_df() that returns a clean pandas DataFrame
#   * Safe numeric conversion utilities
#   * Optional forced refresh / cache invalidation

from __future__ import annotations

from dotenv import load_dotenv
import os

load_dotenv()

from typing import Iterable, List, Optional, Dict, Any, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

import pandas as pd


class AnimalDatabaseManager:
    """Thin wrapper around MongoClient with small caching + helpers.

    This *isn't* a full ORM. It's intentionally lightweight for instructional use.
    """

    def __init__(self):
        try:
            username = os.getenv('MONGO_USER')
            password = os.getenv('MONGO_PASSWORD')
            host = os.getenv('MONGO_HOST')
            port = int(os.getenv('MONGO_PORT'))
            db_name = os.getenv('MONGO_DB')

            
            connection_uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=AAC"
            self.client = MongoClient(connection_uri)
            self.database = self.client[db_name]
        except Exception as e:
            print("Error connecting to MongoDB:", e)
            raise

        # Simple in-memory cache: {(query_tuple, fields_tuple): [docs, ...]}
        self._read_cache: dict[Tuple, list[dict]] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @property
    def animals(self) -> Collection:
        return self.database.animals

    @staticmethod
    def _normalize_query(query: Optional[dict]) -> dict:
        return query or {}

    @staticmethod
    def _normalize_fields(fields: Optional[Iterable[str]]) -> Optional[dict]:
        """Convert iterable of field names → Mongo projection dict.

        If fields is None, return None (no projection).
        """
        if not fields:
            return None
        proj = {f: 1 for f in fields}
        # Always include _id so we can drop or stringify; we *don't* exclude to avoid driver surprises.
        proj['_id'] = 1
        return proj

    @staticmethod
    def _cache_key(query: dict, fields: Optional[Iterable[str]]) -> Tuple:
        # Convert dicts to tuples so they can be keys; sorted for determinism.
        q_tuple = tuple(sorted(query.items()))
        f_tuple = tuple(sorted(list(fields))) if fields else None
        return (q_tuple, f_tuple)

    def _cache_get(self, key: Tuple) -> Optional[list[dict]]:
        return self._read_cache.get(key)

    def _cache_set(self, key: Tuple, docs: list[dict]) -> None:
        self._read_cache[key] = docs

    def clear_cache(self) -> None:
        self._read_cache.clear()

    # ------------------------------------------------------------------
    # CRUD ops
    # ------------------------------------------------------------------
    def create(self, document: dict) -> bool:
        if not isinstance(document, dict) or not document:
            raise ValueError("Document must be a non-empty dictionary.")
        try:
            result = self.animals.insert_one(document)
            # Invalidate cache – data changed.
            self.clear_cache()
            return True if result.inserted_id else False
        except Exception as e:
            print(e)
            return False

    def read(self, query: Optional[dict] = None, projection: Optional[dict] = None, *, sort: Optional[list] = None, limit: int = 0, use_cache: bool = True) -> list[dict]:
       
        query = self._normalize_query(query)

        # Build cache key from *field names* not projection dict (which may include _id).
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
            # Invalidate cache – data changed.
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
            # Invalidate cache – data changed.
            self.clear_cache()
            return result.deleted_count
        except Exception as e:
            print(e)
            return 0

    # ------------------------------------------------------------------
    # Higher-level helpers for Dash
    # ------------------------------------------------------------------
    def read_df(self, query: Optional[dict] = None, *, fields: Optional[Iterable[str]] = None, force_refresh: bool = False) -> pd.DataFrame:
        """Return a *clean* DataFrame based on a read(), projecting fields as requested.

        Enhancements:
          * Optional projection → less data transferred.
          * Cache-aware (unless force_refresh).
          * Automatic cleanup: drop _id or convert to str, numeric coercion.
        """
        projection = self._normalize_fields(fields)
        docs = self.read(query, projection, use_cache=not force_refresh)
        df = pd.DataFrame.from_records(docs)
        df = self._clean_df(df)
        return df

    # --- data cleanup -------------------------------------------------
    @staticmethod
    def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        # Convert ObjectId -> str then drop? We'll keep string version; drop raw column if needed.
        if '_id' in df.columns:
            try:
                df['_id'] = df['_id'].astype(str)
            except Exception:
                df['_id'] = df['_id'].apply(lambda x: str(x))
            # We don't surface _id to the UI; drop to avoid dash_table dtype confusion.
            df = df.drop(columns=['_id'])

        # Safe numeric coercions (errors='coerce' gives NaN for bad entries).
        for col in ('age_upon_outcome_in_weeks', 'location_lat', 'location_long'):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # String tidy – strip whitespace.
        for col in ('name', 'breed', 'animal_type', 'sex_upon_outcome'):
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        return df
