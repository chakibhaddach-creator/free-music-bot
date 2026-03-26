
         import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

user_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 تحميل أغنية", callback_data="music")]
    ]
    await update.message.reply_text(
        "🔥 FREE MUSIC BOT\nأرسل اسم الأغنية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "music":
        user_mode[query.from_user.id] = "music"
        await query.message.reply_text("🎵 أرسل اسم الأغنية")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("⏳ جاري البحث...")

    try:
        # API مجاني لتحميل الصوت
        url = f"https://api.vevioz.com/api/button/mp3/{text}"

        await update.message.reply_text(f"✅ اضغط هنا لتحميل:\n{url}")

    except:
        await update.message.reply_text("❌ حدث خطأ")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()