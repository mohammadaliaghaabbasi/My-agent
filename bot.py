import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from browser_use import Agent, ChatGoogle, Browser, BrowserConfig

# کلیدها و توکن اختصاصی
TELEGRAM_BOT_TOKEN = "8760014581:AAHgQq2zxLB9ywMnva3CZeSUMRHstf94tLs"
os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6J7CYX1n8MsH7Q_ZG-4yB9b6hV5X9-2mCZ83ke_vBfqqw"

# تنظیم مدل هوش مصنوعی
llm = ChatGoogle(model="gemini-1.5-flash")

# تنظیم جامع مرورگر سازگار با محیط Codespaces و سرورهای بدون مانیتور
browser = Browser(
    config=BrowserConfig(
        headless=True,
        extra_chromium_args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--single-process"
        ]
    )
)

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("در حال باز کردن مرورگر و پردازش دستور...")

    try:
        agent = Agent(
            task=prompt,
            llm=llm,
            browser=browser
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
