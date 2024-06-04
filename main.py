from Logic.logic import Running
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4
from bson import ObjectId
import json
from bson import json_util

import http.server
import socketserver
import webbrowser



app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


try:
    # Attempt to connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    # Access a test database and collection
    db = client["testdb"]
    collection = db["testcollection"]
    # Insert a test document to verify the connection
    collection.insert_one({"test": "connection"})
    # Print a success message
    print("Successfully connected to MongoDB")
except Exception as e:
    # Print an error message if connection fails
    print(f"Error connecting to MongoDB: {e}")





@app.route('/insert', methods=['POST'])
def insert_document():
    data = request.json
    if data:
        # Add a unique ID for each document
        data["_id"] = str(uuid4())
        data["timestamp"] = datetime.now()
        # Insert the document into the collection
        collection.insert_one(data)
        return jsonify({"message": "Document inserted successfully!"}), 201
    else:
        return jsonify({"error": "No data provided"}), 400

@app.route('/documents', methods=['GET'])
def get_documents():
    documents = list(collection.find({}, {"_id": 0}))
    return jsonify(documents), 200

@app.route('/run_script', methods=['GET'])
def run_script():
    print("Executing /run_script route...")
    response_data = {}
    try:
        with Running(teardown=True) as bot:
            bot.land_first_page()
            bot.SignIn()
            trending_topics = bot.extract_trending_topics()
            
            if trending_topics:
                document = {
                    "unique_id": str(uuid4()),  # Unique ID for each run
                    "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
                    "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
                    "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
                    "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
                    "trend5": trending_topics[4] if len(trending_topics) > 4 else None,
                    "timestamp": datetime.now(),
                    "ip_address": request.remote_addr
                }
                collection.insert_one(document)
                print("Document inserted:", document)
                
                response_data = {
                    "trends": trending_topics,
                    "ip": request.remote_addr,
                    "mongoRecord": document
                }
            else:
                print("No trending topics found.")
                response_data = {
                    "trends": [],
                    "ip": request.remote_addr,
                    "mongoRecord": {}
                }
                
        for document in collection.find():
            if '_id' in document:
                document['_id'] = str(document['_id'])
        print(response_data)
       
        return jsonify({"data": list(collection.find())}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
    print("Script executed successfully!")
    return jsonify(response_data), 200



@app.route('/hello/World', methods=['GET'])
def hello_world():
    json_data = {}
    print("Executing /run_script route...")
    try:
        with Running() as bot:
           bot.land_first_page()
           bot.SignIn()
           topics = bot.extract_trending_topics()
           if topics:
                document = {
                    "unique_id": str(uuid4()),  # Unique ID for each run
                    "trend1": topics[0] if len(topics) > 0 else None,
                    "trend2": topics[1] if len(topics) > 1 else None,
                    "trend3": topics[2] if len(topics) > 2 else None,
                    "trend4": topics[3] if len(topics) > 3 else None,
                    "trend5": topics[4] if len(topics) > 4 else None,
                    "timestamp": datetime.now(),
                    "ip_address": request.remote_addr
                }
                collection.insert_one(document)
                print("Document inserted:", document)

                json_data = json_util.dumps(document)
                print(json_data)
        return json_data


    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)