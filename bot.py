import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# API key Railway environment থেকে নেওয়া হবে
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# এখানে সরাসরি client বানানোর দরকার নেই
# client = OpenAI() এখন ব্যবহার করবো ঠিকভাবে নিচে

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই! আমি 🤖 BotBhai — তোমার ChatGPT powered বন্ধু!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🧠 ভাবছি...")

    try:
        client = OpenAI()  # ← এখানে শুধু এটা রাখো
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("😢 কিছু ভুল হয়েছে!")
        print("Error:", e)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 BotBhai is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
