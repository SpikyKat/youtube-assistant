import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def generate_script(video_idea, keywords=None, tone_feedback=None):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    keywords_str = ", ".join(keywords) if keywords else ""
    tone_instruction = f" Style: {tone_feedback}." if tone_feedback else ""

    prompt = f"""You are a professional YouTube scriptwriter.
Write a full YouTube script for the following video idea:
Idea: "{video_idea}"
Include keywords: {keywords_str}
Structure: Hook/Intro → Main Content (3–5 points) → Conclusion/CTA
Make the language engaging and natural for a spoken video.
{tone_instruction}
Output should be clear and structured as a script."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate structured, audience-friendly YouTube scripts."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# ▶️ Interactive CLI
if __name__ == "__main__":
    print("🎤 YouTube Assistant – Script Generator")
    print("-" * 50)

    video_idea = input("Enter your video idea or title: ")
    keywords_input = input("Enter keywords (comma-separated, or leave blank): ")
    tone = input("What tone/style do you want? (e.g., motivational, funny, storytelling, etc.): ")

    keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []

    while True:
        print("\n⏳ Generating script...\n")
        try:
            script = generate_script(video_idea, keywords, tone_feedback=tone)
            print("✅ Suggested Script:\n")
            print(script)

            print("\n💬 What would you like to do next?")
            print("1. Accept this script")
            print("2. Rewrite with a different tone/style")
            print("3. Try a new topic")
            print("4. Exit to main menu")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Script accepted. Ready to record!")
                break
            elif choice == "2":
                tone = input("Enter new tone/style (e.g., emotional, fast-paced, expert-level): ")
            elif choice == "3":
                video_idea = input("Enter new video idea: ")
                keywords_input = input("Enter keywords (comma-separated): ")
                tone = input("Enter tone/style: ")
                keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []
            elif choice == "4":
                print("🔙 Returning to main menu...\n")
                break
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print(f"❌ Error: {e}")
            break
