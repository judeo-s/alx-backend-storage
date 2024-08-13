#!/usr/bin/env python3
"""Script that updates all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """
    A Python function that updates all topics of a school document
    based on the name

    Args:
        mongo_collection: collection
        name: name
        topics: topics
    """
    return mongo_collection.update_many({"name": name},
                                        {"$set": {"topics": topics}})
