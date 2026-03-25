import argparse
import json
import logging
import requests
from google import genai
from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils import embedding_functions
from evalQ import eval_questions, EvalQ

load_dotenv()
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Evaluate math LLM models")
parser.add_argument(
    "--mode",
    choices=["base", "finetuned", "finetuned_rag"],
    required=True,
    help="Which model configuration to evaluate"
)
args = parser.parse_args()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
BASE_MODEL = os.getenv("BASE_MODEL")
FINETUNED_MODEL = os.getenv("FINETUNED_MODEL")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------------------------------------------------------------------
# Ollama check
# ---------------------------------------------------------------------------

def check_ollama(model_name: str):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        if model_name not in models:
            logging.error(f"Model '{model_name}' is not downloaded in Ollama.")
            logging.error(f"Downloaded models: {models}")
            logging.error(f"Please download it first: ollama run {model_name}")
            exit(1)
        logging.info(f"✓ Ollama is running and model '{model_name}' is available.")
    except requests.exceptions.ConnectionError:
        logging.error(f"Cannot connect to Ollama at {OLLAMA_URL}.")
        logging.error("Ollama is not running. Please start it from: https://ollama.com/download")
        exit(1)
    except Exception as e:
        logging.error(f"Unexpected error while checking Ollama: {e}")
        exit(1)

# ---------------------------------------------------------------------------
# Chroma setup (only for finetuned_rag mode)
# ---------------------------------------------------------------------------

collection = None

if args.mode == "finetuned_rag":
    logging.info("Setting up ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = chroma_client.get_collection(
        name="math_qa",
        embedding_function=embedding_fn,
    )
    logging.info(f"✓ ChromaDB loaded with {collection.count()} documents.")

# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

def retrieve_context(query: str) -> str:
    if collection is None:
        return ""
    results = collection.query(query_texts=[query], n_results=3)
    return "\n\n".join(results["documents"][0])


def call_ollama(model_name: str, prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False,
        }
    )
    response.raise_for_status()
    return response.json()["response"]


def build_prompt(question: str, style: str, context: str = "") -> str:
    style_instructions = {
        "step_by_step": "Solve this math problem step by step, clearly labeling each step.",
        "short_simple": "Explain this math problem in a short and simple way, avoid technical jargon, maximum 3 sentences.",
        "short_technical": "Give a short and technical answer using formal mathematical notation, maximum 3 sentences.",
        "long_simple": "Explain this math problem in a long and detailed way using simple language and analogies. Avoid technical jargon.",
        "long_technical": "Solve this math problem in a long and detailed way using formal mathematical notation, proofs and technical language.",
    }
    instruction = style_instructions.get(style, "Answer this math problem.")

    if context:
        return f"""{instruction}

Relevant examples:
{context}

Question: {question}"""
    else:
        return f"""{instruction}

Question: {question}"""


# ---------------------------------------------------------------------------
# Gemini evaluator
# ---------------------------------------------------------------------------

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

EVAL_PROMPT_TEMPLATE = """You are a math teacher evaluating a student's answer.

Question: {question}

Ground Truth Answer: {gt}

Student's Answer: {answer}

Requested explanation style: {style}

Please evaluate the student's answer on the following criteria and return a JSON object only, no extra text:

{{
  "math_score": <0-8, where 8=fully correct, 6=minor error, 4=correct approach wrong execution, 2=partially correct, 0=wrong>,
  "style_score": <0-6, where 6=perfectly matches requested style, 4=mostly matches, 2=partially matches, 0=ignores style>,
  "quality_score": <0-4, where 4=very clear and complete, 3=mostly clear, 2=somewhat clear, 1=hard to follow, 0=incomprehensible>,
  "feedback": "<one sentence explaining the scores>"
}}"""


def evaluate_with_gemini(eq: EvalQ) -> dict:
    prompt = EVAL_PROMPT_TEMPLATE.format(
        question=eq.q,
        gt=eq.gt,
        answer=eq.a,
        style=eq.style,
    )
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    raw = response.text.strip()
    # strip markdown code fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Main evaluation loop
# ---------------------------------------------------------------------------

if args.mode == "base":
    model_name = BASE_MODEL
else:
    model_name = FINETUNED_MODEL

check_ollama(model_name)

logging.info(f"Starting evaluation in mode: {args.mode}")
logging.info(f"Using model: {model_name}")
logging.info(f"Total questions: {len(eval_questions)}")

for i, eq in enumerate(eval_questions):
    logging.info(f"\n[{i+1}/{len(eval_questions)}] Field: {eq.field} | Style: {eq.style}")
    logging.info(f"Question: {eq.q[:80]}...")

    # build prompt with or without RAG context
    context = ""
    if args.mode == "finetuned_rag":
        context = retrieve_context(eq.q)
        logging.info(f"Retrieved {len(context)} chars of RAG context.")

    prompt = build_prompt(eq.q, eq.style, context)

    # call local model
    try:
        eq.a = call_ollama(model_name, prompt)
        logging.info(f"Answer: {eq.a[:100]}...")
    except Exception as e:
        logging.error(f"Failed to get answer from Ollama: {e}")
        eq.a = ""
        continue

    # evaluate with Gemini
    try:
        scores = evaluate_with_gemini(eq)
        eq.math_score = scores["math_score"]
        eq.style_score = scores["style_score"]
        eq.quality_score = scores["quality_score"]
        eq.feedback = scores.get("feedback", "")
        logging.info(f"Scores — math: {eq.math_score}/8 | style: {eq.style_score}/6 | quality: {eq.quality_score}/4 | total: {eq.total}/18")
        logging.info(f"Feedback: {scores.get('feedback', '')}")
    except Exception as e:
        logging.error(f"Failed to evaluate with Gemini: {e}")
        continue

# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------

output_file = f"results_{args.mode}.json"

results = []
for eq in eval_questions:
    results.append({
        "field": eq.field,
        "style": eq.style,
        "question": eq.q,
        "ground_truth": eq.gt,
        "answer": eq.a,
        "math_score": eq.math_score,
        "style_score": eq.style_score,
        "quality_score": eq.quality_score,
        "total": eq.total,
        "feedback": eq.feedback,
    })

with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

logging.info(f"\nResults saved to {output_file}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

total_math = sum(eq.math_score for eq in eval_questions)
total_style = sum(eq.style_score for eq in eval_questions)
total_quality = sum(eq.quality_score for eq in eval_questions)
total_overall = sum(eq.total for eq in eval_questions)
max_possible = len(eval_questions) * 18

logging.info("\n" + "="*50)
logging.info(f"FINAL RESULTS — mode: {args.mode}")
logging.info("="*50)
logging.info(f"Math score:    {total_math}/{len(eval_questions)*8}")
logging.info(f"Style score:   {total_style}/{len(eval_questions)*6}")
logging.info(f"Quality score: {total_quality}/{len(eval_questions)*4}")
logging.info(f"Overall:       {total_overall}/{max_possible} ({100*total_overall/max_possible:.1f}%)")

# per-field breakdown
logging.info("\nPer-field breakdown:")
fields = list(set(eq.field for eq in eval_questions))
for field in fields:
    field_qs = [eq for eq in eval_questions if eq.field == field]
    field_total = sum(eq.total for eq in field_qs)
    field_max = len(field_qs) * 18
    logging.info(f"  {field}: {field_total}/{field_max} ({100*field_total/field_max:.1f}%)")
