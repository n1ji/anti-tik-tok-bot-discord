import datetime
import os
import re

import discord

BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")  # Set the DISCORD_TOKEN environment variable

# Integer channel IDs (right-click a channel in Discord with Developer Mode on -> Copy Channel ID)
TARGET_CHANNEL_ID = 0  # Channel where TikTok links get re-posted
MAIN_CHANNEL_ID = 0    # Channel to watch; TikTok links posted here are moved and deleted

FILE_NAME = "tiktok_urls.txt"  # File that stores the URLs

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Matches tiktok.com links with any subdomain (www, vm, vt, m, ...) or none
TIKTOK_URL_PATTERN = re.compile(
    r"https?://(?:[a-z0-9-]+\.)*tiktok\.com(?:/\S*)?",
    re.IGNORECASE,
)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != MAIN_CHANNEL_ID:
        return

    urls = TIKTOK_URL_PATTERN.findall(message.content)
    if not urls:
        return

    print(f"TikTok URL(s) detected: {urls}")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(f"{timestamp} - {message.author} - {url}\n")

    try:
        target_channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
        await target_channel.send(
            f"From {message.author.mention}:\n" + "\n".join(urls),
            allowed_mentions=discord.AllowedMentions.none(),
        )
    except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
        # Don't delete the original if the repost failed
        print(f"Could not post to target channel {TARGET_CHANNEL_ID}: {e}")
        return

    try:
        await message.delete()
        print(f"Deleted message from {message.author}")
    except (discord.Forbidden, discord.NotFound, discord.HTTPException) as e:
        print(f"Could not delete message (needs Manage Messages permission?): {e}")


if not BOT_TOKEN:
    raise SystemExit("Set the DISCORD_TOKEN environment variable before running.")
if not TARGET_CHANNEL_ID or not MAIN_CHANNEL_ID:
    raise SystemExit("Set TARGET_CHANNEL_ID and MAIN_CHANNEL_ID to integer channel IDs.")

client.run(BOT_TOKEN)
