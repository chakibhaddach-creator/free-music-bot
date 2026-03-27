import os
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 أرسل اسم الأغنية")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("⏳ جاري البحث...")

    try:
        url = f"https://api.vreden.my.id/api/spotify-download?query={query}"
        res = requests.get(url).json()

        if "result" not in res:
            await update.message.reply_text("❌ لم يتم العثور على الأغنية")
            return

        download_url = res["result"]["download"]

        audio = requests.get(download_url)

        with open("song.mp3", "wb") as f:
            f.write(audio.content)

        await update.message.reply_audio(audio=open("song.mp3", "rb"))

        os.remove("song.mp3")

    except:
        await update.message.reply_text("❌ حدث خطأ")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    import asyncio
    asyncio.run(application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=10000)