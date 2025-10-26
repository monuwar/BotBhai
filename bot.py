import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# Environment variables (Railway ও লোকাল দু’জায়গায় কাজ করবে)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenAI ক্লায়েন্ট সেটআপ
client = OpenAI(api_key=OPENAI_API_KEY)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই! আমি 🤖 BotBhai — তোমার ChatGPT powered বন্ধু! কিছু লিখে পাঠাও ✨")

# সাধারণ মেসেজ হ্যান্ডলার
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🧠 ভাবছি...")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("😢 কিছু ভুল হয়েছে! আবার চেষ্টা করো।")
        print("Error:", e)

# অ্যাপ চালু করা
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 BotBhai is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
