import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 تحميل أغنية", callback_data="music")],
        [InlineKeyboardButton("🎬 تحميل فيديو", callback_data="video")]
    ]
    await update.message.reply_text(
        "🔥 FREE MUSIC BOT\nاختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "music":
        user_mode[query.from_user.id] = "music"
        await query.message.reply_text("🎵 أرسل اسم الأغنية")

    elif query.data == "video":
        user_mode[query.from_user.id] = "video"
        await query.message.reply_text("🎬 أرسل اسم الفيديو")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    mode = user_mode.get(user_id)

    if not mode:
        await update.message.reply_text("اضغط /start أولاً")
        return

    await update.message.reply_text("⏳ جاري التحميل...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best' if mode == "music" else 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if mode == "music" else []
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{text}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0])

        if mode == "music":
            file_name = file_name.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            await update.message.reply_audio(audio=open(file_name, 'rb'))
        else:
            await update.message.reply_video(video=open(file_name, 'rb'))

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()