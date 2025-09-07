import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERNAME = "@Hichkas1390"   # فقط همین یوزرنیم اجازه دسترسی دارد

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and ("@" + update.effective_user.username) == ALLOWED_USERNAME:
        await update.message.reply_text("سلام! فایل بفرست تا لینکش رو بسازم ✅")
    else:
        await update.message.reply_text("⛔️ شما اجازه استفاده از این ربات را ندارید.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.username or ("@" + update.effective_user.username) != ALLOWED_USERNAME:
        return

    file = None
    if update.message.document:
        file = update.message.document
    elif update.message.video:
        file = update.message.video
    elif update.message.audio:
        file = update.message.audio
    elif update.message.photo:
        file = update.message.photo[-1]

    if file:
        file_obj = await file.get_file()
        file_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_obj.file_path}"
        await update.message.reply_text(f"🔗 لینک فایل شما:\n{file_link}")
    else:
        await update.message.reply_text("لطفاً یک فایل (عکس، ویدیو، سند...) ارسال کنید.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
