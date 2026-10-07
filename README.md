# Anti TikTok Bot (Discord)

A small Discord bot for servers where a friend keeps sending TikTok links in chat. It removes the link from the conversation, reposts it in a dedicated channel, and keeps a log of everything it has caught.

## What it does

When someone posts a TikTok link (`tiktok.com` or `vm.tiktok.com`), the bot:

1. Saves each link with a timestamp and the author's name to `tiktok_urls.txt`
2. Posts the link into your links channel (`TARGET_CHANNEL_ID`)
3. Deletes the original message

Only messages sent while the script is running are handled.

## Requirements

- Python 3
- [discord.py](https://pypi.org/project/discord.py/): `pip install discord.py`
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

## Setup

1. Create an application in the Developer Portal, open the **Bot** tab and click **Reset Token**. Copy the token.
2. On the same tab, enable the **Message Content Intent**. The bot needs it to read links.
3. Set your bot token as an environment variable (don't paste it into the script):

   ```bash
   export DISCORD_TOKEN="your bot token"
   ```

4. In `anti tik tok bot.py`, fill in the two channel IDs at the top. They must be plain numbers, not quoted text:

   | Setting | What to put there |
   |---|---|
   | `TARGET_CHANNEL_ID` | ID of the channel where caught TikTok links are reposted |
   | `MAIN_CHANNEL_ID` | ID of the channel the bot watches. TikTok links posted here are reposted and deleted; other channels are ignored |

   To get a channel ID, enable Developer Mode in Discord, right-click the channel and choose **Copy Channel ID**.
5. Invite the bot to your server through the **OAuth2** tab. Give it permission to read messages, send messages and **Manage Messages** (needed to delete).
6. Run it:

   ```bash
   python "anti tik tok bot.py"
   ```

An older step-by-step guide with screenshots is in [`outdated/tutorial.docx`](outdated/tutorial.docx). It describes the previous setup (token and channel IDs inside the script), so follow the steps above instead.

> **Keep your token private.** Never commit your real bot token to GitHub. If it leaks, reset it in the Developer Portal.

## Issues

Questions or problems? Open an [issue](https://github.com/n1ji/anti-tik-tok-bot-discord/issues). They are checked about once a week.

Made by n1ji (plaui).
