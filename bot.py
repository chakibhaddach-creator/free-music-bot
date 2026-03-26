import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# start
def start(update, context):
    update.message.reply_text("🎵 أرسل اسم الأغنية")

# message
def handle_message(update, context):
    query = update.message.text

    update.message.reply_text("⏳ جاري البحث...")

    try:
        url = f"https://api.vreden.my.id/api/spotify-download?query={query}"
        res = requests.get(url).json()

        if "result" not in res:
            update.message.reply_text("❌ لم يتم العثور على الأغنية")
            return

        download_url = res["result"]["download"]
        title = res["result"]["title"]

        update.message.reply_text(f"🎧 جاري تحميل: {title}")

        audio = requests.get(download_url)
        file_name = "song.mp3"

        with open(file_name, "wb") as f:
            f.write(audio.content)

        update.message.reply_audio(audio=open(file_name, "rb"))

        os.remove(file_name)

    except:
        update.message.reply_text("❌ حدث خطأ")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)