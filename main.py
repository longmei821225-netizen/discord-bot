import discord
from discord.ext import tasks
import feedparser
import os
import instagram_checker

BOT_TOKEN = os.environ["TOKEN"]
DISCORD_CHANNEL_ID = 1520123459274018856
YOUTUBE_CHANNEL_ID = "UCJnL-TBcsYrF2SLs7tmiC8Q"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_video_id = None

def get_latest_video():
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
    feed = feedparser.parse(url)
    if feed.entries:
        return feed.entries[0]
    return None

@tasks.loop(minutes=5)
async def check_youtube():
    global last_video_id
    video = get_latest_video()
    if not video:
        return

    video_id = video.yt_videoid
    if last_video_id is None:
        last_video_id = video_id
        return

    if video_id != last_video_id:
        last_video_id = video_id
        channel = client.get_channel(1520123459274018856)
      await channel.send(
            f"@everyone 새 영상 업로드!\n**{video.title}**\nhttps://www.youtube.com/watch?v={video_id}"
        )
        )

@client.event
async def on_ready():
    print(f"✅ {client.user} 시작됨!")
    check_youtube.start()
    try:
        instagram_checker.start(client)
    except Exception as e:
        print(f"⚠️ 인스타그램 시작 오류: {e}")

client.run(BOT_TOKEN)
