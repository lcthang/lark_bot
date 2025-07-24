import os
import requests
from constants import *
from .lark_handler import *


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --- Step 1: Detect if chat intends to create JD ---
def detect_jd_intent(chat_history: str):
    prompt = JD_INTENT_PROMPT.format(chat_history=chat_history)
    result = call_openrouter(prompt)
    print("Chat History::: %s" % chat_history)
    print("JD Intent Detection %s" % result)
    return result.strip().lower().startswith("yes")


# --- Step 2: Extract key job info ---
def extract_job_info(chat_history: str) -> str:
    prompt = JOB_INFO_PROMPT.format(chat_history=chat_history)
    return call_openrouter(prompt)


# --- Step 3: Generate JD from structured info ---
def generate_job_description(info: str):
    company_name = get_company_name()
    prompt = JOB_DESCRIPTION_PROMPT.format(company_name=company_name, info=info)
    return call_openrouter(prompt)


def call_openrouter(prompt):
    api_key = OPENROUTER_API_KEY
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Failed to generate response."
