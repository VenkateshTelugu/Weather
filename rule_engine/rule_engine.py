# rule_engine.py

from ast import Node
from models import Rule, db
import re

def create_rule(rule_string):
    # A simple parser for rule_string (placeholder logic)
    # You would replace this with a full parser for your needs
    # Example: parse "age > 30" into an AST Node

    if "AND" in rule_string or "OR" in rule_string:
        tokens = re.split(r'(\s+)', rule_string)
        root = Node("operator", tokens[1].strip())
        left_expr = create_rule(tokens[0].strip())
        right_expr = create_rule(' '.join(tokens[2:]).strip())
        root.left = left_expr
        root.right = right_expr
        return root
    else:
        # Simple operand node (like "age > 30")
        op = re.match(r"(\w+)\s*([\>\=<]+)\s*(\d+|\'.*\')", rule_string)
        if op:
            return Node("operand", {"field": op.group(1), "operator": op.group(2), "value": op.group(3)})
    return None

def combine_rules(rules):
    if not rules:
        return None

    # Simple combination logic: AND all rules
    combined = Node("operator", "AND")
    combined.left = create_rule(rules[0])
    for rule in rules[1:]:
        new_node = create_rule(rule)
        combined.right = new_node
    return combined

def evaluate_rule(ast, data):
    if ast.type == "operand":
        field = ast.value["field"]
        operator = ast.value["operator"]
        value = ast.value["value"]
        
        if field not in data:
            return False
        
        if operator == '>':
            return data[field] > (int(value.strip("'")) if isinstance(value, str) and value.isnumeric() else value)
        elif operator == '<':
            return data[field] < (int(value.strip("'")) if isinstance(value, str) and value.isnumeric() else value)
        elif operator == '=':
            return data[field] == value.strip("'")

    if ast.type == "operator":
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)

    return False
