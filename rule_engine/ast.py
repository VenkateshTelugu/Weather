# ast.py

class Node:
    def __init__(self, node_type, value=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value      # Optional value for operand nodes
        self.left = None        # Left child reference
        self.right = None       # Right child reference

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"
