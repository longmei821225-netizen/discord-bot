from discord.ext import tasks
import discord
import datetime
import pytz

DISCORD_CHANNEL_ID = 1520037247846715463

MEMBERS = [
    {"name": "서연", "month": 8, "day": 6},
    {"name": "혜린", "month": 4, "day": 12},
    {"name": "지우", "month": 10, "day": 24},
    {"name": "채연", "month": 12, "day": 4},
    {"name": "유연", "month": 2, "day": 9},
    {"name": "수민", "month": 10, "day": 3},
    {"name": "나경", "month": 10, "day": 13},
    {"name": "유빈", "month": 2, "day": 3},
    {"name": "에데", "month": 12, "day": 20},
    {"name": "다현", "month": 1, "day": 8},
    {"name": "토네", "month": 3, "day": 10},
    {"name": "연지", "month": 1, "day": 8},
    {"name": "니엔", "month": 6, "day": 2},
    {"name": "박소현", "month": 10, "day": 13},
    {"name": "신위", "month": 5, "day": 25},
    {"name": "마유", "month": 5, "day": 12},
    {"name": "린", "month": 4, "day": 12},
    {"name": "주빈", "month": 1, "day": 16},
    {"name": "하연", "month": 8, "day": 1},
    {"name": "시온", "month": 4, "day": 3},
    {"name": "채원", "month": 5, "day": 2},
    {"name": "설린", "month": 11, "day": 30},
    {"name": "서아", "month": 6, "day": 11},
    {"name": "지연", "month": 2, "day": 13},
]

_discord_client = None

@tasks.loop(minutes=1)
async def check_birthday():
    kst = pytz.timezone("Asia/Seoul")
    now = datetime.datetime.now(kst)

    if now.hour != 0 or now.minute != 0:
        return

    today_month = now.month
    today_day = now.day

    channel = _discord_client.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return

    for member in MEMBERS:
        if member["month"] == today_month and member["day"] == today_day:
            await channel.send(f"🎂 오늘은 **{member['name']}이**의 생일이에요!")

def start(discord_client):
    global _discord_client
    _discord_client = discord_client
    check_birthday.start()
    print("✅ 생일 알림 시작")
