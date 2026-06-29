import feedparser
from discord.ext import tasks
import discord

INSTA_TARGET_ACCOUNTS = [
    "triplescosmos",
]

DISCORD_CHANNEL_ID = 1520037247846715463

last_post_ids = {}
_discord_client = None

@tasks.loop(minutes=5)
async def check_instagram():
    global last_post_ids
    for account in INSTA_TARGET_ACCOUNTS:
        try:
            rss_url = f"https://rss.app/feeds/v1.1/_Pz5FJoJV5JV5JV5J.json"
            feed = feedparser.parse(rss_url)

            if not feed.entries:
                print(f"⚠️ {account} 피드가 비어있음")
                continue

            latest = feed.entries[0]
            post_id = latest.get("id", "")

            if account not in last_post_ids:
                last_post_ids[account] = post_id
                print(f"✅ {account} 초기화 완료")
                continue

            if post_id != last_post_ids[account]:
                last_post_ids[account] = post_id

                post_url = latest.get("link", "")
                description = latest.get("summary", "")[:200]

                embed = discord.Embed(
                    title=f"📸 @{account} 새 게시물!",
                    url=post_url,
                    description=description,
                    color=0xE1306C
                )

                channel = _discord_client.get_channel(DISCORD_CHANNEL_ID)
                if channel:
                    await channel.send(embed=embed)

        except Exception as e:
            print(f"⚠️ 오류 ({account}): {e}")

def start(discord_client):
    global _discord_client
    _discord_client = discord_client
    check_instagram.start()
    print("✅ 인스타그램 모니터링 시작")
