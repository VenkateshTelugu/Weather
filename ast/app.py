from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from models import Node  # Import Node class from models.py
from rules import evaluate_rule  # Import evaluate_rule function from rules.py

app = Flask(__name__)

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rule_engine'  # Change the URI as needed
mongo = PyMongo(app)

# API Endpoint to Create a New Rule
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')
    if not rule_string:
        return jsonify({'error': 'Missing rule_string'}), 400
    
    # Create the AST from the rule string
    root_node = create_rule_node(rule_string)  # Implement this function
    mongo.db.rules.insert_one({'rule_string': rule_string, 'ast': root_node})  # Store the rule in the database
    return jsonify({'message': 'Rule created successfully'}), 201

# API Endpoint to Fetch All Rules
@app.route('/get_rules', methods=['GET'])
def get_rules():
    rules = mongo.db.rules.find()  # Retrieve all rules from the database
    return jsonify([{'rule_string': rule['rule_string'], 'ast': rule['ast']} for rule in rules]), 200

# API Endpoint to Evaluate a Rule
@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json  # Get user attributes from JSON body
    rule_id = data.get('rule_id')  # Get the rule ID to evaluate
    
    rule = mongo.db.rules.find_one({'_id': rule_id})  # Load the rule from the database
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404

    root_node = rule['ast']  # Load the AST for evaluation
    result = evaluate_rule(root_node, data)  # Evaluate the rule
    return jsonify({'result': result})

# Function to Create AST Node from Rule String
def create_rule_node(rule_string):
    # TODO: Implement the logic to parse the rule string and create an AST
    # This should return a Node object representing the rule.
    pass

if __name__ == '__main__':
    app.run(debug=True)
