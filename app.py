from flask import Flask, request, jsonify
from rag_chain import query_rag

app = Flask(__name__)

@app.route("/api/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = query_rag(question)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
