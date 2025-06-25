import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API details
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def generate_youtube_titles(video_idea, keywords=None, n_titles=5, style_feedback=None):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    keywords_str = ", ".join(keywords) if keywords else ""

    # Add style to prompt if provided
    style_instruction = f" Rewrite the titles with this style: {style_feedback}." if style_feedback else ""

    prompt = f"""You are a YouTube SEO expert.
Generate {n_titles} high-converting YouTube video titles for the following idea:
Idea: "{video_idea}"
Keywords to include: {keywords_str}.{style_instruction}
Make them engaging, short, and optimized for high CTR."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert in creating viral YouTube video titles."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip().split("\n")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
