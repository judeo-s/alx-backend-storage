#!/usr/bin/env python3
"""Script that prints stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def log_stats():
    """prints stats about Nginx logs stored in MongoDB"""
    with MongoClient() as client:
        collection = client.logs.nginx
        print("{} logs".format(collection.count_documents({})))
        print("Methods:")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods:
            print("    method {}: {}".format(
                method,
                collection.count_documents({"method": method})))
        print("{} status check".format(
            collection.count_documents({"method": "GET", "path": "/status"})))


if __name__ == "__main__":
    log_stats()
