import logging
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# ⚠️ استبدل هذا النص بالتوكن الذي حصلت عليه من BotFather
TOKEN = "9058665997:AAGkve0db6dMlEOLe_h3JkFgpJxaT-HO6aM" 

# User-Agents لمحاكاة أجهزة مختلفة (موبايل، كمبيوتر، متصفحات)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط فيديو يوتيوب لزيادة المشاهدات.\nمثال: https://www.youtube.com/watch?v=xxxxx")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # التأكد أن الرابط هو يوتيوب
    if not ('youtube.com/watch?v=' in url or 'youtu.be/' in url):
        await update.message.reply_text("يرجى إرسال رابط فيديو يوتيوب صحيح.")
        return

    video_id = None
    if 'v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        
    if not video_id:
        await update.message.reply_text("لم أستطع استخراج معرف الفيديو.")
        return

    views_added = 0
    total_views_to_add = 10  # عدد المشاهدات في كل مرة
    
    await update.message.reply_text(f"🔄 جاري زيادة المشاهدات... ({total_views_to_add} مشاهدة)")

    for i in range(total_views_to_add):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            
            # طلب فتح الصفحة كما لو كان مستخدم حقيقي
            response = requests.get(
                f"https://www.youtube.com/watch?v={video_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                views_added += 1
                # انتظار عشوائي بين 2 و 5 ثوانٍ لمحاكاة سلوك بشري
                time.sleep(random.uniform(2, 5))
                
        except Exception as e:
            pass

    await update.message.reply_text(f"✅ تمت زيادة {views_added} مشاهدة بنجاح!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running... ✅")
    app.run_polling()

if __name__ == '__main__':
    main()