from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)


# ---------------------------------------------------------------------------
# Chroma setup
# ---------------------------------------------------------------------------

# TODO: initialize Chroma client
# TODO: initialize embedding model (sentence-transformers)
# TODO: get or create Chroma collection

# ---------------------------------------------------------------------------
# RAG helpers
# ---------------------------------------------------------------------------

def retrieve_context(query: str) -> str:
    # TODO: embed the query
    # TODO: query Chroma for top-k similar documents
    # TODO: return concatenated context string
    pass

def index_document(text: str, metadata: dict) -> None:
    # TODO: embed the text
    # TODO: store in Chroma with metadata
    pass

# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

def build_prompt(message: str, preference: str, last_message: str, context: str) -> str:
    # TODO: combine context + preference + conversation history into a prompt
    pass

def call_llm(prompt: str) -> str:
    # TODO: POST to LLM_API_URL with the prompt
    # TODO: parse and return the response text
    pass

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/getResponse", methods=["POST"])
def get_response():
    data = request.get_json()

    # TODO: validate required fields (chatId, message, preference, lastMessage)
    # TODO: call retrieve_context(message)
    # TODO: call build_prompt(message, preference, last_message, context)
    # TODO: call call_llm(prompt)
    # TODO: return jsonify({ "chatId": ..., "llmResponse": ... })

    return jsonify({"chatId": None, "llmResponse": None})


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)

