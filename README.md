# 📺 YouTube Assistant AI

A powerful Streamlit-based application to assist YouTubers and content creators with title generation, description writing, tag suggestions, script generation, and channel performance analysis — powered by LLMs and the YouTube Data API.

## 🚀 Features

- 🎬 **YouTube Title Generator** – Suggests optimized and catchy titles using keywords.
- 📄 **Description Generator** – Writes SEO-friendly video descriptions.
- 🏷️ **Tag Suggester** – Recommends relevant hashtags and tags.
- 🎤 **Script Generator** – Generates video scripts with custom tone and keywords.
- 📊 **Channel Performance Tracker** – Analyzes public YouTube channel stats:
  - 🥇 Top 5 most viewed videos
  - 📅 Upload frequency chart
  - 🧠 Metadata optimization insights (titles, descriptions, hashtags)
  - 📁 CSV export of video stats
  - 🤖 LLM-based SEO feedback using Groq's LLaMA

 ## 📂 Project Structure

 youtube_assistant_ai/
├── assets/ # Static assets (optional)
├── modules/ # Contains all feature modules
│ ├── title_generator.py
│ ├── description_generator.py
│ ├── tag_suggester.py
│ ├── script_generator.py
│ └── channel_tracker.py
├── utils/ # Utility functions (optional)
├── .env # Environment variables (NOT committed)
├── main.py # Python core logic (can be renamed to ytapp.py)
├── ytapp.py # Streamlit app entrypoint
├── requirements.txt # Python dependencies
├── README.md # Project overview
└── launch_ytapp.bat # Windows batch file to run the app


## ⚙️ Installation

1. **Clone the repository**:
   git clone https://github.com/yourusername/youtube-assistant-ai.git
   cd youtube-assistant-ai
2. **Create and activate a virtual environment (optional but recommended)**:
    python -m venv venv
    venv\Scripts\activate
3. **Install Dependencies**:
    pip install -r requirements.txt
4. **Setup environment variables**:
   Create a .env file in the root with
     YOUTUBE_API_KEY=your_youtube_api_key
     GROQ_API_KEY=your_groq_api_key
5. **Run the App**

 **📈 Sample Output**

 ![Screenshot 2025-06-25 120107](https://github.com/user-attachments/assets/2b1e2b59-50f2-4b01-9734-65f6b49a9b7f)

 ![Screenshot 2025-06-25 120132](https://github.com/user-attachments/assets/c9b7d596-16fb-4b3a-a06e-9c410f7c54af)

 ![Screenshot 2025-06-25 120216](https://github.com/user-attachments/assets/c4710bd4-2f2b-4809-b29d-407cf125e676)

 ![Screenshot 2025-06-25 120248](https://github.com/user-attachments/assets/7d504b8e-9dd5-41e0-a6bc-844fdaae25c9)



**🔐 Environment Variables**
Make sure to set these in .env:

Variable	                      Purpose
YOUTUBE_API_KEY	                Access YouTube Data API v3
GROQ_API_KEY	                  Use LLaMA3-70B for LLM insights

**📄 License**
MIT License © 2025 Rahul Ghantasala

