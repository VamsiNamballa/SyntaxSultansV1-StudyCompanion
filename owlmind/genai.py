import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()


# Hugging Face API token (read from environment)
HF_TOKEN = os.getenv("HF_TOKEN")
# print(f"HF Token Loaded: {HF_TOKEN}")  # Debugging the token value

# Hugging Face model endpoint (Switched to gpt2 Instruct)
API_URL = "https://api-inference.huggingface.co/models/gpt2"


# Authorization headers
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def ask_genai(prompt: str) -> str:
    """
    Send a prompt to Hugging Face Inference API and get model-generated response.
    """

    # If token is missing, fallback automatically to mock GenAI
    if not HF_TOKEN:
        return f"[GenAI Simulated Response]: Based on your input, here is the answer:\n{prompt}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 750,  # Increase to allow longer tutor explanations
            "temperature": 0.7,     # Creativity control
            "top_p": 0.9,           # Top-p sampling
            "do_sample": True,      # Enable sampling
            "repetition_penalty": 1.1,  # Penalize repetitive outputs
        }
    }

    retries = 3
    backoff_factor = 2
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            generated_text = response.json()

            # Print the raw response from Hugging Face for debugging
            print(f"Raw response from Hugging Face: {generated_text}")

            # Handling response format:
            if isinstance(generated_text, list) and "generated_text" in generated_text[0]:
                return generated_text[0]["generated_text"]
            elif isinstance(generated_text, dict) and "generated_text" in generated_text:
                return generated_text["generated_text"]
            elif isinstance(generated_text, list) and "summary_text" in generated_text[0]:
                return generated_text[0]["summary_text"]
            elif isinstance(generated_text, dict) and "summary_text" in generated_text:
                return generated_text["summary_text"]
            else:
                return "[GenAI Response Error] Unexpected output format."

        except requests.exceptions.RequestException as e:
            print(f"Error occurred during request: {e}")
            if attempt < retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return f"[GenAI Simulated Response]: Based on your input, here is the answer:\n{prompt}"
