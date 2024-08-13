#!/usr/bin/env python3

"""Script that lists all schools having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """lists all schools having a specific topic"""
    return mongo_collection.find({"topics": topic})
