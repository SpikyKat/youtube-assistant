import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API details
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def generate_youtube_description(video_idea, keywords=None, style_feedback=None):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    keywords_str = ", ".join(keywords) if keywords else ""
    style_instruction = f" Write it in this style: {style_feedback}." if style_feedback else ""

    prompt = f"""You are an expert YouTube content strategist and SEO writer.
Write an engaging, SEO-optimized YouTube video description based on this idea:
"{video_idea}"
Keywords to include: {keywords_str}.
The description should:
- Start with a strong hook/intro
- Mention the value of the video
- Include relevant keywords naturally
- Use appropriate emojis to grab attention
- End with a strong call to action
- Add 3–5 trending and relevant hashtags
{style_instruction}

Make the tone natural and suitable for YouTube viewers."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a YouTube description expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# 🎯 Interactive CLI
if __name__ == "__main__":
    print("📄 YouTube Assistant – Description Generator")
    print("-" * 50)

    video_idea = input("Enter your video idea or brief summary: ")
    keywords_input = input("Enter keywords (comma-separated, or leave blank): ")
    keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []

    while True:
        print("\n⏳ Generating description...\n")
        try:
            description = generate_youtube_description(video_idea, keywords)
            print("✅ Suggested Description:\n")
            print(description)

            print("\n💬 What would you like to do next?")
            print("1. Accept this description")
            print("2. Ask for a rewrite with feedback")
            print("3. Regenerate with new idea/keywords")
            print("4. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Description accepted. You're ready to upload!")
                break
            elif choice == "2":
                feedback = input("Enter how you'd like to improve it (e.g., more exciting, more emojis, shorter, etc.): ")
                print("\n🔁 Regenerating with your feedback...\n")
                description = generate_youtube_description(video_idea, keywords, style_feedback=feedback)
                print("✅ New Description:\n")
                print(description)
            elif choice == "3":
                video_idea = input("Enter your new video idea or summary: ")
                keywords_input = input("Enter new keywords (comma-separated): ")
                keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []
            elif choice == "4":
                print("👋 Exiting Description Generator. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        except Exception as e:
            print(f"❌ Error: {e}")
            break
