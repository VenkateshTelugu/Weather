from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/rule_engine_db"
mongo = PyMongo(app)

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_data = request.json
    mongo.db.rules.insert_one(rule_data)
    return jsonify({"message": "Rule created successfully!"}), 201

@app.route('/rules', methods=['GET'])
def get_rules():
    rules = mongo.db.rules.find()
    return dumps(rules)

if __name__ == '__main__':
    app.run(debug=True)
