import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def suggest_youtube_tags(content_input, style_feedback=None):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    style_instruction = f" Style: {style_feedback}." if style_feedback else ""

    prompt = f"""You are an expert YouTube SEO optimizer.
Based on the following video content, generate a list of the top 15 SEO-optimized YouTube tags.
The tags should be short, lowercase, comma-separated, and relevant to the content. Include keyword variations and trending phrases.
Content: "{content_input}"{style_instruction}
Output only the tags as a comma-separated list. No extra explanation."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate trending and relevant YouTube tags."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# ▶️ Interactive test
if __name__ == "__main__":
    print("🏷️ YouTube Assistant – Tag Suggestion Engine")
    print("-" * 50)

    content_input = input("Enter video title or description: ")

    while True:
        print("\n⏳ Suggesting tags...\n")
        try:
            tags = suggest_youtube_tags(content_input)
            print("✅ Suggested Tags:\n")
            print(tags)

            print("\n💬 What next?")
            print("1. Accept these tags")
            print("2. Ask for a different tone/style")
            print("3. Enter new content")
            print("4. Exit to main menu")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Tags saved. You're all set!")
                break
            elif choice == "2":
                feedback = input("Style feedback (e.g., more trending, broader, niche-specific): ")
                tags = suggest_youtube_tags(content_input, style_feedback=feedback)
                print("\n✅ Updated Tags:\n")
                print(tags)
            elif choice == "3":
                content_input = input("Enter new video title or description: ")
            elif choice == "4":
                print("🔙 Returning to main menu...\n")
                break
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print(f"❌ Error: {e}")
            break
