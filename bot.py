import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Gemini configuration
genai.configure(api_key=GEMINI_API_KEY)

# Check available models (temporary for debugging)
def check_available_models():
    try:
        models = genai.list_models()
        print("Available models:", models)
    except Exception as e:
        print("Error listing models:", e)

# Call model list on startup
check_available_models()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই! আমি 🤖 BotBhai — এখন Gemini দ্বারা চালিত! ✨")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🧠 ভাবছি...")

    try:
        # Use a valid model for the chat (replace with correct model)
        response = genai.generate_text(
            model="gemini-1.5",  # Use a valid model name from available models list
            prompt=user_message
        )
        reply = response.text
        await update.message.reply_text(reply)

    except Exception as e:
        print("❌ Error:", e)
        await update.message.reply_text("😢 কিছু ভুল হয়েছে!")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 BotBhai (Gemini) is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
