import os
import requests
import pandas as pd
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
from groq import Groq
import io

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

def get_channel_data(channel_input):
    try:
        if "@" in channel_input and "youtube.com" in channel_input:
            handle = channel_input.split("@")[-1].strip("/")
            search_url = f"{YOUTUBE_API_BASE}/search?part=snippet&q={handle}&type=channel&key={YOUTUBE_API_KEY}"
            search_res = requests.get(search_url).json()
            if "items" not in search_res or not search_res["items"]:
                raise Exception("❌ Channel not found using handle search.")
            channel_id = search_res["items"][0]["snippet"]["channelId"]
        elif "/channel/" in channel_input:
            channel_id = channel_input.split("/channel/")[-1].split("/")[0]
        elif "youtube.com" not in channel_input:
            # Assume it's a plain username
            search_url = f"{YOUTUBE_API_BASE}/channels?part=snippet,statistics,contentDetails&forUsername={channel_input}&key={YOUTUBE_API_KEY}"
            res = requests.get(search_url).json()
            if "items" not in res or not res["items"]:
                raise Exception("❌ Channel not found with username.")
            return parse_channel_data(res["items"][0])
        else:
            raise Exception("❌ Invalid YouTube channel input format.")

        # Get channel details from ID
        url = f"{YOUTUBE_API_BASE}/channels?part=snippet,statistics,contentDetails&id={channel_id}&key={YOUTUBE_API_KEY}"
        res = requests.get(url).json()
        if "items" not in res or not res["items"]:
            raise Exception("❌ Channel not found with resolved ID.")
        return parse_channel_data(res["items"][0])

    except Exception as e:
        raise Exception(f"Failed to fetch channel data: {str(e)}")

def parse_channel_data(data):
    return {
        "channel_title": data["snippet"]["title"],
        "description": data["snippet"].get("description", ""),
        "published_at": data["snippet"]["publishedAt"],
        "subscriber_count": int(data["statistics"].get("subscriberCount", 0)),
        "view_count": int(data["statistics"].get("viewCount", 0)),
        "video_count": int(data["statistics"].get("videoCount", 0)),
        "uploads_playlist_id": data["contentDetails"]["relatedPlaylists"]["uploads"]
    }

def get_videos_from_playlist(playlist_id, max_results=50):
    videos = []
    next_page_token = ""
    while True:
        url = f"{YOUTUBE_API_BASE}/playlistItems?part=snippet&maxResults={max_results}&playlistId={playlist_id}&key={YOUTUBE_API_KEY}&pageToken={next_page_token}"
        res = requests.get(url).json()
        for item in res.get("items", []):
            snippet = item["snippet"]
            videos.append({
                "video_id": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "description": snippet.get("description", ""),
                "published_at": snippet["publishedAt"]
            })
        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break
    return videos

def get_video_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        url = f"{YOUTUBE_API_BASE}/videos?part=statistics,snippet&id={','.join(chunk)}&key={YOUTUBE_API_KEY}"
        res = requests.get(url).json()
        for item in res.get("items", []):
            stats.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "tags": item["snippet"].get("tags", []),
                "published_at": item["snippet"]["publishedAt"],
                "view_count": int(item["statistics"].get("viewCount", 0)),
                "like_count": int(item["statistics"].get("likeCount", 0))
            })
    return stats

def export_to_csv(video_details, channel_title):
    df = pd.DataFrame(video_details)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer

def show_top_5_videos(video_details):
    return sorted(video_details, key=lambda x: x["view_count"], reverse=True)[:5]

def upload_frequency_chart(video_details):
    df = pd.DataFrame(video_details)
    df['published_at'] = pd.to_datetime(df['published_at'])
    freq = df['published_at'].dt.to_period("M").value_counts().sort_index()
    return freq

def metadata_optimization(video_details):
    repeated_titles = set()
    seen = set()
    for vid in video_details:
        if vid["title"] in seen:
            repeated_titles.add(vid["title"])
        seen.add(vid["title"])

    missing_descriptions = sum(1 for v in video_details if not v["description"].strip())
    missing_tags = sum(1 for v in video_details if not v["tags"])
    hashtags = []
    for v in video_details:
        hashtags += [word for word in v["description"].split() if word.startswith("#")]
    most_common = Counter(hashtags).most_common(5)

    return {
        "repeated_titles": list(repeated_titles),
        "missing_descriptions": missing_descriptions,
        "missing_tags": missing_tags,
        "common_hashtags": most_common
    }

def analyze_channel_with_llm(video_samples):
    if not GROQ_API_KEY:
        return "🔐 Groq API Key not found."
    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        "You are a YouTube SEO expert. Analyze the following video titles and descriptions and provide suggestions to improve SEO, use of keywords, hashtags, and engagement:\n\n"
    )
    for i, video in enumerate(video_samples, 1):
        prompt += f"{i}. Title: {video['title']}\n   Description: {video['description'][:300]}\n\n"
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
