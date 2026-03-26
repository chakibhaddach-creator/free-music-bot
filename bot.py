import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 أرسل اسم الأغنية")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    await update.message.reply_text("⏳ جاري البحث...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
        }

        # البحث فقط (بدون تحميل)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            url = info['entries'][0]['url']

        await update.message.reply_text("⏳ جاري التحميل...")

        # تحميل الصوت
        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])

        # إرسال الملف
        await update.message.reply_audio(audio=open("song.mp3", 'rb'))

        os.remove("song.mp3")

    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()