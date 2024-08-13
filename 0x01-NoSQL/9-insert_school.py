#!/usr/bin/env python3
"""Script that inserts a document in the collection"""


def insert_school(mongo_collection, **kwargs):
    """
    A Python function that inserts a new document in a collection
    based on kwargs

    Args:
        mongo_collection: collection
        **kwargs: key-value pairs
    """
    return mongo_collection.insert_one(kwargs)