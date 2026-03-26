import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 أرسل اسم الأغنية")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("⏳ جاري البحث...")

    try:
        # API احترافي (بحث + تحميل)
        url = f"https://api.vreden.my.id/api/spotify-download?query={query}"

        res = requests.get(url).json()

        if "result" not in res:
            await update.message.reply_text("❌ لم يتم العثور على الأغنية")
            return

        download_url = res["result"]["download"]
        title = res["result"]["title"]

        await update.message.reply_text(f"🎧 جاري تحميل: {title}")

        # تحميل الملف
        audio = requests.get(download_url)

        file_name = "song.mp3"
        with open(file_name, "wb") as f:
            f.write(audio.content)

        # إرسال داخل Telegram
        await update.message.reply_audio(
            audio=open(file_name, "rb"),
            title=title
        )

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()