import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

TELEGRAM_BOT_TOKEN = "8760014581:AAHgQq2zxLB9ywMnva3CZeSUMRHstf94tLs"
GEMINI_KEY = "AQ.Ab8RN6L2lm0vkR6PWCXvh1yTqJPpY5LrOgnP4HWqKCdpGIzmAg"

# تنظیم مستقیم متغیرهای محیطی سیستم
os.environ["GOOGLE_API_KEY"] = GEMINI_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_KEY
os.environ["DISPLAY"] = ""
os.environ["PLAYWRIGHT_HEADLESS"] = "1"

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_KEY
)

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("در حال پردازش دستور در وب...")

    try:
        agent = Agent(
            task=prompt,
            llm=llm
        )
        history = await agent.run(max_steps=10)
        result = history.final_result()
        await status_msg.edit_text(f"نتیجه عملیات:\n\n{result}")
    except Exception as e:
        await status_msg.edit_text(f"خطا در اجرا: {str(e)}")

if __name__ == "__main__":
    print("ONLINE_GENAI_READY")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task))
    app.run_polling(drop_pending_updates=True)
