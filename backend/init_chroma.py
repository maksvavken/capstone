from datasets import load_dataset
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "math_qa"
TARGET_COUNT = 1000
MIN_SCORE = 5

# ---------------------------------------------------------------------------
# Init Chroma
# ---------------------------------------------------------------------------

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"},
)

# ---------------------------------------------------------------------------
# Load and filter dataset
# ---------------------------------------------------------------------------

print("Loading dataset...")
ds = load_dataset("math-ai/StackMathQA", "stackmathqa100k", split="train")

print(f"Filtering for question_score >= {MIN_SCORE}...")
ds = ds.filter(lambda x: int(x["meta"]["question_score"]) >= MIN_SCORE)

print(f"Found {len(ds)} questions after filtering. Taking first {TARGET_COUNT}...")
ds = ds.select(range(min(TARGET_COUNT, len(ds))))

# ---------------------------------------------------------------------------
# Index into Chroma
# ---------------------------------------------------------------------------

print("Indexing into Chroma...")

ids = []
documents = []
metadatas = []

for i, example in enumerate(ds):
    doc_id = f"math_{i}"
    document = f"Question: {example['Q']}\nAnswer: {example['A']}"

    metadata = {
        "question": example["Q"],   # chroma has metadata size limits
        "url": example["meta"].get("url", ""),
        "source": example["meta"].get("source", ""),
        "question_score": str(example["meta"].get("question_score", "0")),
    }

    ids.append(doc_id)
    documents.append(document)
    metadatas.append(metadata)

    # batch insert every 100 to avoid memory issues
    if len(ids) == 100:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        print(f"  Indexed {i + 1}/{TARGET_COUNT}...")
        ids, documents, metadatas = [], [], []

# insert remaining
if ids:
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

print(f"Done! Collection '{COLLECTION_NAME}' now has {collection.count()} documents.")
