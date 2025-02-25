from pyrogram import Client, filters
import os
import logging
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Initialize bot
app = Client("phantomshield", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Enable logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Protection Status (Dictionary to track enabled/disabled state)
protection_enabled = {}

# ✅ Blacklisted Words (With Variations)
blacklisted_words = [
    "rape", "cp", "child porn", "abuse", "molest", "nude kids",
    "dark web", "selling cp", "snuff", "pedo", "child video",
    "forced video", "illegal content", "trafficking", "cp videos"
]

# ✅ Command: /start (Check if Bot is Working)
@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_command(client, message):
    await message.reply_text("✅ **PhantomShieldBot is ACTIVE!**\nUse /test to check bot status.")

# ✅ Command: /test (Check Bot Status)
@app.on_message(filters.command("test") & (filters.private | filters.group))
async def test_command(client, message):
    await message.reply_text("✅ **PhantomShieldBot is Running Smoothly!**")

# ✅ Command: /protection ON | OFF (Enable or Disable Filtering)
@app.on_message(filters.command("protection") & filters.group)
async def toggle_protection(client, message):
    chat_id = message.chat.id
    command_args = message.text.split(" ")

    if len(command_args) < 2:
        await message.reply_text("⚠️ Usage: `/protection ON` or `/protection OFF`")
        return

    action = command_args[1].lower()

    if action == "on":
        protection_enabled[chat_id] = True
        await message.reply_text("✅ **Protection Enabled!**\nMessages with blacklisted words will be deleted.")
    elif action == "off":
        protection_enabled[chat_id] = False
        await message.reply_text("❌ **Protection Disabled!**\nNo filtering will be applied.")
    else:
        await message.reply_text("⚠️ Invalid option! Use `/protection ON` or `/protection OFF`.")

# ✅ Detect & DELETE Blacklisted Messages (Only if Protection is Enabled)
@app.on_message(filters.text & ~filters.private)  # Ensure it detects group messages
async def filter_blacklisted_words(client, message):
    chat_id = message.chat.id

    # ✅ If protection is disabled, do nothing
    if chat_id not in protection_enabled or not protection_enabled[chat_id]:
        return

    logger.info(f"📩 Received message: {message.text}")  # Debugging log

    if any(word in message.text.lower() for word in blacklisted_words):
        try:
            await message.delete()
            logger.info(f"🚨 Deleted risky message: {message.text}")
        except Exception as e:
            logger.error(f"❌ Failed to delete message: {e}")

# ✅ Block @AbuseNotifications Automatically
@app.on_message(filters.user("AbuseNotifications") & filters.group)
async def delete_abuse_notifications(client, message):
    await message.delete()
    logger.info("🚨 Deleted message from @AbuseNotifications.")

# ✅ Start the Bot
if __name__ == "__main__":
    logger.info("✅ PhantomShieldBot is running!\n")
    app.run()
