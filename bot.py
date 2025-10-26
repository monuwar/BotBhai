import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই! আমি 🤖 BotBhai — তোমার ChatGPT powered বন্ধু!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🧠 ভাবছি...")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "তুমি BotBhai, একজন বন্ধুসুলভ বাংলা ChatGPT সহকারী।"},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        print("❌ Error:", e)
        await update.message.reply_text("😢 কিছু ভুল হয়েছে!")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 BotBhai is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
