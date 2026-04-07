from flask import Flask, request, jsonify
from pymongo import MongoClient, WriteConcern
from pymongo.read_preferences import ReadPreference

app = Flask(__name__)

connection_string = "mongodb+srv://shajra2_db:Sohan2026@hw3.pitsr3c.mongodb.net/?appName=hw3"
client = MongoClient(connection_string)
db = client.ev_db

@app.route('/insert-fast', methods=['POST'])
def insert_fast():
    data = request.json
    collection = db.vehicles.with_options(write_concern=WriteConcern(w=1))
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route('/insert-safe', methods=['POST'])
def insert_safe():
    data = request.json
    collection = db.vehicles.with_options(write_concern=WriteConcern(w='majority'))
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route('/count-tesla-primary', methods=['GET'])
def count_tesla():
    collection = db.vehicles.with_options(read_preference=ReadPreference.PRIMARY)
    count = collection.count_documents({"Make": "TESLA"})
    return jsonify({"count": count}), 200

@app.route('/count-bmw-secondary', methods=['GET'])
def count_bmw():
    collection = db.vehicles.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = collection.count_documents({"Make": "BMW"})
    return jsonify({"count": count}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
