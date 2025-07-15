import os

def load_graphql_query(filename: str) -> str:
    base_path = os.path.dirname(os.path.abspath(__file__)) 
    full_path = os.path.join(base_path, filename)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()