from modules.title_generator import generate_youtube_titles
from modules.description_generator import generate_youtube_description
from modules.tag_suggester import suggest_youtube_tags
from modules.script_generator import generate_script
from modules.channel_tracker import (
    get_channel_data,
    get_videos_from_playlist,
    get_video_stats,
    show_top_5_videos,
    show_upload_frequency,
    metadata_analysis,
    analyze_channel_with_llm,
    export_to_csv
)

def title_generator_flow():
    print("\n🎬 YouTube Assistant – Title Generator")
    print("-" * 50)
    video_idea = input("Enter your video idea: ")
    keywords_input = input("Enter keywords (comma-separated, or leave blank): ")
    keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []

    while True:
        print("\n⏳ Generating titles...\n")
        try:
            titles = generate_youtube_titles(video_idea, keywords)
            print("✅ Suggested Titles:\n")
            for i, title in enumerate(titles, 1):
                print(f"{i}. {title.strip('-•123. ')}")

            print("\n💬 What would you like to do next?")
            print("1. Accept these titles")
            print("2. Ask for changes")
            print("3. Regenerate with new idea/keywords")
            print("4. Exit to main menu")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Titles accepted. You're all set!")
                break
            elif choice == "2":
                feedback = input("Enter feedback for how to improve the titles: ")
                video_idea += f" (Rewrite with this style: {feedback})"
            elif choice == "3":
                video_idea = input("Enter your new video idea: ")
                keywords_input = input("Enter new keywords (comma-separated, or leave blank): ")
                keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []
            elif choice == "4":
                print("🔙 Returning to main menu...\n")
                break
            else:
                print("❌ Invalid option. Try again.")
        except Exception as e:
            print(f"❌ Error: {e}")
            break


def description_generator_flow():
    print("\n📄 YouTube Assistant – Description Generator")
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
            print("4. Exit to main menu")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Description accepted. Ready to upload!")
                break
            elif choice == "2":
                feedback = input("Enter feedback for how to improve the description: ")
                description = generate_youtube_description(video_idea, keywords, style_feedback=feedback)
                print("\n✅ Updated Description:\n")
                print(description)
            elif choice == "3":
                video_idea = input("Enter your new video idea: ")
                keywords_input = input("Enter new keywords (comma-separated): ")
                keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else []
            elif choice == "4":
                print("🔙 Returning to main menu...\n")
                break
            else:
                print("❌ Invalid option. Try again.")
        except Exception as e:
            print(f"❌ Error: {e}")
            break


def tag_suggester_flow():
    print("\n🏷️ YouTube Assistant – Tag Suggestion Engine")
    print("-" * 50)
    content_input = input("Enter your video title or description: ")

    while True:
        print("\n⏳ Generating tags...\n")
        try:
            tags = suggest_youtube_tags(content_input)
            print("✅ Suggested Tags:\n")
            print(tags)

            print("\n💬 What would you like to do next?")
            print("1. Accept these tags")
            print("2. Ask for a rewrite with feedback")
            print("3. Try new content")
            print("4. Exit to main menu")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                print("🎉 Tags accepted. You're ready to publish!")
                break
            elif choice == "2":
                feedback = input("Enter feedback for how to improve the tags: ")
                tags = suggest_youtube_tags(content_input, style_feedback=feedback)
                print("\n✅ Updated Tags:\n")
                print(tags)
            elif choice == "3":
                content_input = input("Enter new video title or description: ")
            elif choice == "4":
                print("🔙 Returning to main menu...\n")
                break
            else:
                print("❌ Invalid option. Try again.")
        except Exception as e:
            print(f"❌ Error: {e}")
            break


def script_generator_flow():
    print("\n🎤 YouTube Assistant – Script Generator")
    print("-" * 50)
    video_idea = input("Enter your video idea or title: ")
    keywords_input = input("Enter keywords (comma-separated, or leave blank): ")
    tone = input("What tone/style do you want? (e.g., motivational, funny, storytelling, expert-level): ")

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


def channel_tracker_flow():
    print("\n📊 YouTube Assistant – Channel Performance Tracker")
    print("-" * 50)
    channel_input = input("Enter YouTube channel username or URL: ")

    try:
        channel = get_channel_data(channel_input)
        print(f"\n✅ Channel: {channel['channel_title']}")
        print(f"📅 Created: {channel['published_at']}")
        print(f"👥 Subscribers: {channel['subscriber_count']}")
        print(f"▶️ Videos: {channel['video_count']}")
        print(f"👁️ Total Views: {channel['view_count']}")

        videos_basic = get_videos_from_playlist(channel["uploads_playlist_id"])
        video_ids = [v["video_id"] for v in videos_basic]
        video_details = get_video_stats(video_ids)

        show_top_5_videos(video_details)
        show_upload_frequency(video_details)
        metadata_analysis(video_details)
        export_to_csv(video_details, channel["channel_title"])

        print("\n🧠 LLM Optimization Feedback:")
        sample = video_details[:5]
        print(analyze_channel_with_llm(sample))

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("📺 YouTube Assistant AI – Main Menu")
    print("=" * 50)

    while True:
        print("\nChoose a tool to use:")
        print("1. 🎬 Title Generator")
        print("2. 📄 Description Generator")
        print("3. 🏷️ Tag Suggestion Engine")
        print("4. 🎤 Script Generator")
        print("5. 📊 Channel Performance Tracker")
        print("6. ❌ Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            title_generator_flow()
        elif choice == "2":
            description_generator_flow()
        elif choice == "3":
            tag_suggester_flow()
        elif choice == "4":
            script_generator_flow()
        elif choice == "5":
            channel_tracker_flow()
        elif choice == "6":
            print("👋 Exiting YouTube Assistant. Goodbye!")
            break
        else:
            print("❌ Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()