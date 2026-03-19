from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
import chromadb
from chromadb.utils import embedding_functions
from google import genai
import os
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "math_qa"

app = Flask(__name__)
CORS(app)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ---------------------------------------------------------------------------
# Chroma setup
# ---------------------------------------------------------------------------

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"},
)

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

    # validate
    required = ["chatId", "message", "preference", "lastMessage"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    chat_id = data["chatId"]
    message = data["message"]
    preference = data["preference"]
    last_message = data["lastMessage"]

    # RAG - retrieve context from Chroma
    rag_results = collection.query(
        query_texts=[message],
        n_results=3,
    )
    context_docs = rag_results["documents"][0]
    context = "\n\n".join(context_docs)

    # build prompt
    prompt = f"""You are a math tutor. Use the following relevant examples from a math Q&A database to help answer the question.

Explanation style: {preference}

Relevant examples:
{context}

Previous message: {last_message}

Now answer this question in the '{preference}' style:
{message}
"""
    logging.info("---------RAG context-----------")
    logging.info(context)
    # call Gemini
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    llm_response = response.text

    return jsonify({
        "chatId": chat_id,
        "llmResponse": llm_response,
    })


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)

