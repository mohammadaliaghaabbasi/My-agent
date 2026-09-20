import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from browser_use import Agent, ChatGoogle

TELEGRAM_BOT_TOKEN = "8760014581:AAFb8j7tR6r_0uLqup9SjqT_7tM-tf3LRRs"
os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6J7CYX1n8MsH7Q_ZG-4yB9b6hV5X9-2mCZ83ke_vBfqqw"

# اتصال مستقیم و رسمی browser-use به جمینای
llm = ChatGoogle(model="gemini-1.5-flash")

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("در حال باز کردن مرورگر و اجرای تسک...")

    try:
        agent = Agent(
            task=prompt,
            llm=llm
        )
        history = await agent.run()
        result = history.final_result()
        await update.message.reply_text(f"نتیجه عملیات:\n\n{result}")
    except Exception as e:
        await update.message.reply_text(f"خطا در اجرا: {str(e)}")

if __name__ == "__main__":
    print("READY")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task))
    app.run_polling()
