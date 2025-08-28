from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# فقط توکن BotFather لازمه
BOT_TOKEN = "7519002098:AAHbu2B1b1Mh85f2GYQoAifa8umx77BNGiA"

ADMIN_PASS = "mySecret123"
admins = set()
files = {}
upload_mode = set()

# ورود به پنل
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ لطفا رمز رو هم وارد کنید. مثال:\n/login mySecret123")
        return
    if context.args[0] == ADMIN_PASS:
        admins.add(update.effective_user.id)
        await update.message.reply_text("✅ ورود موفق! شما الان ادمین هستید.")
    else:
        await update.message.reply_text("❌ رمز اشتباهه!")

# پنل
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admins:
        return
    text = """
🔐 پنل ادمین:
1️⃣ /upload - فعال کردن حالت آپلود
2️⃣ /files - لیست فایل‌ها
3️⃣ /logout - خروج از پنل
"""
    await update.message.reply_text(text)

# فعال کردن آپلود
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in admins:
        upload_mode.add(update.effective_user.id)
        await update.message.reply_text("📂 حالت آپلود فعال شد. هر فایلی بفرستید ذخیره میشه.")

# ذخیره فایل
async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in upload_mode and update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        files[file_name] = file_id
        await update.message.reply_text(f"✅ فایل ذخیره شد: {file_name}")

# لیست فایل‌ها
async def send_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not files:
        await update.message.reply_text("❌ هنوز فایلی آپلود نشده.")
        return
    for name, fid in files.items():
        await context.bot.send_document(update.effective_chat.id, fid, caption=f"📂 {name}")

# خروج
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins.discard(update.effective_user.id)
    upload_mode.discard(update.effective_user.id)
    await update.message.reply_text("🚪 از پنل خارج شدید.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("files", send_files))
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(MessageHandler(filters.Document.ALL, save_file))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
