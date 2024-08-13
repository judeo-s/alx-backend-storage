#!/usr/bin/env python3

"""Script that lists all documents in the collection"""


def list_all(mongo_collection):
    """lists all documents in the collection"""
    return mongo_collection.find()
