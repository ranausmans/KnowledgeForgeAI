from flask import Flask, request, jsonify
from knowledge_graph.graph_manager import GraphManager

app = Flask(__name__)
graph_manager = GraphManager()

@app.route('/subgraph', methods=['GET'])
def get_subgraph():
    entity_name = request.args.get('entity')
    depth = int(request.args.get('depth', 2))
    
    if not entity_name:
        return jsonify({"error": "Entity name is required"}), 400
    
    subgraph = graph_manager.get_subgraph(entity_name, depth)
    
    return jsonify({
        "nodes": [dict(node) for node in subgraph['nodes']],
        "relationships": [dict(rel) for rel in subgraph['relationships']]
    })

if __name__ == '__main__':
    app.run(debug=True)
