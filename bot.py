import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from browser_use import Agent, ChatGoogle

# متغیرهای محیطی برای اجرای بدون مانیتور و پایدار در لینوکس
os.environ["DISPLAY"] = ""
os.environ["PLAYWRIGHT_HEADLESS"] = "1"

TELEGRAM_BOT_TOKEN = "8760014581:AAHgQq2zxLB9ywMnva3CZeSUMRHstf94tLs"
os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6J7CYX1n8MsH7Q_ZG-4yB9b6hV5X9-2mCZ83ke_vBfqqw"

llm = ChatGoogle(model="gemini-1.5-flash")

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("در حال پردازش دستور با مرورگر...")

    try:
        agent = Agent(
            task=prompt,
            llm=llm
        )
        history = await agent.run(max_steps=12)
        result = history.final_result()
        await status_msg.edit_text(f"نتیجه عملیات:\n\n{result}")
    except Exception as e:
        await status_msg.edit_text(f"خطا در اجرا: {str(e)}")

if __name__ == "__main__":
    print("ALL_SYSTEMS_COMPATIBLE")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task))
    app.run_polling(drop_pending_updates=True)
