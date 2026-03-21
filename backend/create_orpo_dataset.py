from datasets import load_dataset, Dataset
from google import genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

STYLES = {
    "step_by_step": {
        "instruction": "Solve this math problem step by step, clearly labeling each step.",
        "rejected_instruction": "Give a short one sentence answer to this math problem, no steps.",
    },
    "short_simple": {
        "instruction": "Explain this math problem in a short and simple way, avoid technical jargon, maximum 3 sentences.",
        "rejected_instruction": "Solve this math problem in a long and detailed way using formal mathematical notation and technical language.",
    },
    "short_technical": {
        "instruction": "Give a short and technical answer to this math problem using formal mathematical notation, maximum 3 sentences.",
        "rejected_instruction": "Explain this math problem in a long and simple way using plain language and analogies.",
    },
    "long_simple": {
        "instruction": "Explain this math problem in a long and detailed way using simple language, analogies and real world examples. Avoid technical jargon.",
        "rejected_instruction": "Give a short and technical answer to this math problem using formal mathematical notation, maximum 3 sentences.",
    },
    "long_technical": {
        "instruction": "Solve this math problem in a long and detailed way using formal mathematical notation, proofs and technical language.",
        "rejected_instruction": "Explain this math problem in a short and simple way, avoid technical jargon, maximum 3 sentences.",
    },
}

STYLES_LIST = list(STYLES.keys())


def generate_response(question: str, instruction: str) -> str:
    prompt = f"""{instruction}

Question: {question}

Provide only the answer, no preamble."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text.strip()


def create_preference_example(question: str, style_key: str) -> dict:
    style = STYLES[style_key]

    chosen = generate_response(question, style["instruction"])
    time.sleep(1)  # avoid rate limiting

    rejected = generate_response(question, style["rejected_instruction"])
    time.sleep(1)

    prompt = f"[{style_key.upper()}] {question}"

    return {
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected,
        "style": style_key,
    }


# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------

print("Loading StackMathQA dataset...")
ds = load_dataset("math-ai/StackMathQA", "stackmathqa100k", split="train")
ds = ds.filter(lambda x: int(x["meta"]["question_score"]) >= 5)
ds = ds.shuffle(seed=42).select(range(500))
print(f"Loaded {len(ds)} examples")

# ---------------------------------------------------------------------------
# Generate preference dataset
# ---------------------------------------------------------------------------

preference_data = []
failed = 0

for i, example in enumerate(ds):
    question = example["Q"]
    style_key = STYLES_LIST[i % len(STYLES_LIST)]  # rotate through styles

    print(f"[{i+1}/500] Generating {style_key} example...")

    try:
        entry = create_preference_example(question, style_key)
        preference_data.append(entry)

        # save every 50 examples in case of crash
        if (i + 1) % 50 == 0:
            checkpoint = Dataset.from_list(preference_data)
            checkpoint.save_to_disk(f"./preference_dataset_checkpoint_{i+1}")
            print(f"  Checkpoint saved at {i+1} examples")

    except Exception as e:
        print(f"  Failed on example {i+1}: {e}")
        failed += 1
        time.sleep(5)  # wait longer on error
        continue

# ---------------------------------------------------------------------------
# Save final dataset
# ---------------------------------------------------------------------------

print(f"\nDone! Generated {len(preference_data)} examples ({failed} failed)")

final_dataset = Dataset.from_list(preference_data)
final_dataset.save_to_disk("./preference_dataset")
final_dataset.push_to_hub("malomorgen/math-preference-orpo", private=True)

print("Dataset saved locally and pushed to HuggingFace!")
print(final_dataset)
