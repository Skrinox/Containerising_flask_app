
"""
simple python flask application
"""

##########################################################################
## Imports
##########################################################################

import os

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask.json import jsonify
from pymongo import MongoClient
import json

##########################################################################
## Application Setup
##########################################################################

app = Flask(__name__)

def check_mongo_connection(client):
    res = None
    try:
        client = MongoClient(os.getenv("MONGO_HOST", "localhost"), 27017, serverSelectionTimeoutMS=2000)
        res = client.server_info()  # Force connection

        return res
    except Exception as e:
        return res

def populate_db(client):
    db = client["testdb"]
    collection = db["users"]

    # checks if users already exists
    if collection.count_documents({}) == 0:
        data = [
        {"name": "test", "email": "test@gmail.com"},
        {"name": "lala", "email": "lala@gmail.com"},
        {"name": "lala2", "email": "lala2@gmail.com"}
        ]
        collection.insert_many(data)

##########################################################################
## Routes
##########################################################################

@app.route("/")
def home():
    client = MongoClient(os.getenv("MONGO_HOST", "localhost"), 27017, serverSelectionTimeoutMS=2000)

    connected = check_mongo_connection(client)
    populate_db(client)
    db = client["testdb"]
    collection = db["users"]
    users = list(collection.find())

    return render_template("home.html", mongo_status=connected, users=users)

@app.route("/api/hello")
def hello():
    """
    Return a hello message
    """
    return jsonify({"hello": "world"})

@app.route("/api/hello/<name>")
def hello_name(name):
    """
    Return a hello message with name
    """
    return jsonify({"hello": name})

@app.route("/api/whoami")
def whoami():
    """
    Return a JSON object with the name, ip, and user agent
    """
    return jsonify(
        name=request.remote_addr,
        ip=request.remote_addr,
        useragent=request.user_agent.string
    )

@app.route("/api/whoami/<name>")
def whoami_name(name):
    """
    Return a JSON object with the name, ip, and user agent
    """
    return jsonify(
        name=name,
        ip=request.remote_addr,
        useragent=request.user_agent.string
    )

##########################################################################
## Main
##########################################################################

if __name__ == '__main__':
    app.run()