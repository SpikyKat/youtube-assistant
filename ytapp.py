import os
import pandas as pd
import io
import matplotlib.pyplot as plt
import streamlit as st
from modules.title_generator import generate_youtube_titles
from modules.description_generator import generate_youtube_description
from modules.tag_suggester import suggest_youtube_tags
from modules.script_generator import generate_script
from modules.channel_tracker import (
    get_channel_data,
    get_videos_from_playlist,
    get_video_stats,
    analyze_channel_with_llm,
    show_top_5_videos,
    upload_frequency_chart,
    metadata_optimization,
    export_to_csv
)

def title_generator_flow():
    st.header("🎬 YouTube Title Generator")
    idea = st.text_input("Enter your video idea")
    keywords = st.text_input("Enter keywords (comma-separated)").split(",")
    if st.button("Generate Titles") and idea:
        titles = generate_youtube_titles(idea, keywords)
        st.write("### Suggested Titles:")
        for i, title in enumerate(titles, 1):
            st.write(f"{i}. {title.strip('-•123. ')}")

def description_generator_flow():
    st.header("📄 YouTube Description Generator")
    idea = st.text_input("Enter your video idea or summary")
    keywords = st.text_input("Enter keywords (comma-separated)").split(",")
    if st.button("Generate Description") and idea:
        desc = generate_youtube_description(idea, keywords)
        st.text_area("Generated Description", desc, height=200)

def tag_suggester_flow():
    st.header("🏷️ YouTube Tag Suggester")
    content = st.text_input("Enter your video title or description")
    if st.button("Suggest Tags") and content:
        tags = suggest_youtube_tags(content)
        st.text_area("Suggested Tags", tags)

def script_generator_flow():
    st.header("🎤 YouTube Script Generator")
    topic = st.text_input("Enter video topic or idea")
    tone = st.text_input("Preferred tone/style (funny, serious, expert, etc.)")
    keywords = st.text_input("Enter keywords (comma-separated)").split(",")
    if st.button("Generate Script") and topic:
        script = generate_script(topic, keywords, tone_feedback=tone)
        st.text_area("Generated Script", script, height=300)

def channel_tracker_flow():
    st.header("📊 YouTube Channel Performance Tracker")
    channel_input = st.text_input("Enter YouTube channel username or URL")
    if st.button("Analyze Channel") and channel_input:
        try:
            channel = get_channel_data(channel_input)
            st.success(f"Analyzing channel: {channel['channel_title']}")
            st.write(f"**Created on:** {channel['published_at']}")
            st.write(f"**Subscribers:** {channel['subscriber_count']} | **Videos:** {channel['video_count']} | **Views:** {channel['view_count']}")

            videos_basic = get_videos_from_playlist(channel["uploads_playlist_id"])
            video_ids = [v["video_id"] for v in videos_basic]
            stats = get_video_stats(video_ids)

            st.subheader("🥇 Top 5 Videos")
            top_videos = show_top_5_videos(stats)
            df_top = pd.DataFrame(top_videos)[["title", "view_count", "like_count", "published_at"]]
            st.table(df_top.rename(columns={
                "title": "Title",
                "view_count": "Views",
                "like_count": "Likes",
                "published_at": "Published"
            }))

            st.subheader("📅 Upload Frequency")
            freq = upload_frequency_chart(stats)
            fig, ax = plt.subplots()
            freq.plot(kind='bar', ax=ax)
            ax.set_ylabel("Number of Videos")
            st.pyplot(fig)

            st.subheader("🧠 Metadata Optimization")
            meta = metadata_optimization(stats)
            if meta["repeated_titles"]:
                st.warning(f"⚠️ Repeated Titles Detected: {', '.join(meta['repeated_titles'])}")
            else:
                st.success("✅ All video titles are unique!")
            st.info(f"📝 Videos missing descriptions: {meta['missing_descriptions']}")
            st.info(f"🏷️ Videos missing tags: {meta['missing_tags']}")
            if meta['common_hashtags']:
                st.write("### 📌 Most Common Hashtags:")
                for tag, count in meta['common_hashtags']:
                    st.write(f"{tag}: {count} times")

            st.subheader("📁 Download CSV Report")
            csv = export_to_csv(stats, channel["channel_title"])
            st.download_button("Download CSV", csv, file_name="channel_report.csv", mime="text/csv")

            st.subheader("🤖 LLM Insights")
            feedback = analyze_channel_with_llm(stats[:5])
            st.text_area("LLM Feedback", feedback, height=300)

        except Exception as e:
            st.error(f"❌ Error: {e}")

def main():
    st.set_page_config(page_title="YouTube Assistant AI", layout="wide", initial_sidebar_state="expanded")
    st.title("📺 YouTube Assistant AI")
    st.sidebar.title("🚀 Choose a Tool")
    choice = st.sidebar.radio("Select Module:", [
        "🎬 Title Generator",
        "📄 Description Generator",
        "🏷️ Tag Suggester",
        "🎤 Script Generator",
        "📊 Channel Tracker"
    ])

    if choice == "🎬 Title Generator":
        title_generator_flow()
    elif choice == "📄 Description Generator":
        description_generator_flow()
    elif choice == "🏷️ Tag Suggester":
        tag_suggester_flow()
    elif choice == "🎤 Script Generator":
        script_generator_flow()
    elif choice == "📊 Channel Tracker":
        channel_tracker_flow()

if __name__ == "__main__":
    main()
