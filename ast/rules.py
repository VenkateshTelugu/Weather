# class Node:
#     def __init__(self, type, left=None, right=None, value=None):
#         self.type = type        # e.g., "operator" or "operand"
#         self.left = left        # Reference to left child node
#         self.right = right      # Reference to right child node (for operators)
#         self.value = value      # Optional value for operand nodes (e.g., for comparisons)

# rules.py

def evaluate_rule(node, data):
    if node.type == 'operand':
        # Assuming node.value is structured as (attribute, operator, comparison_value)
        attribute, operator, comparison_value = node.value
        
        # Retrieve the actual value from the data using the attribute name
        actual_value = data.get(attribute)

        # Perform the comparison based on the operator
        if operator == '>':
            return actual_value > comparison_value
        elif operator == '<':
            return actual_value < comparison_value
        elif operator == '==':
            return actual_value == comparison_value
        elif operator == '!=':
            return actual_value != comparison_value
        elif operator == '>=':
            return actual_value >= comparison_value
        elif operator == '<=':
            return actual_value <= comparison_value

    elif node.type == 'operator':
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)

        # Implement AND/OR logic based on node.value
        if node.value == 'AND':
            return left_eval and right_eval
        elif node.value == 'OR':
            return left_eval or right_eval

    return False  # Default return value if none of the conditions are met
