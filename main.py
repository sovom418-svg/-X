    import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# আপনার তথ্য এখানে বসান
BOT_TOKEN = '8315570920:AAEVbhuUhCFpJYVW8Ls-92H2VzCn1oW7Reg'
ADMIN_ID = 123456789  # আপনার আইডি

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমাদের সাপোর্ট টিমে স্বাগতম। আপনার সমস্যাটি এখানে লিখুন।")

# মেসেজ হ্যান্ডলিং (সাপোর্ট সিস্টেম)
async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # অ্যাডমিন যদি কোনো মেসেজে রিপ্লাই দেয়
    if user_id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                # অরিজিনাল ইউজারের আইডি খুঁজে বের করা
                original_msg = update.message.reply_to_message
                # নোট: ফরোয়ার্ড করা মেসেজ থেকে আইডি নেওয়া
                target_user_id = original_msg.forward_from.id
                
                await context.bot.send_message(chat_id=target_user_id, text=f"সাপোর্ট টিম: {update.message.text}")
                await update.message.reply_text("✅ ইউজারকে উত্তর পাঠানো হয়েছে।")
            except:
                await update.message.reply_text("❌ রিপ্লাই দেওয়া যায়নি (ইউজারের প্রাইভেসি সেটিংসের কারণে)।")
    else:
        # ইউজার মেসেজ দিলে তা অ্যাডমিনকে ফরোয়ার্ড করা
        await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        await update.message.reply_text("📩 আপনার মেসেজটি টিমের কাছে পৌঁছেছে। অনুগ্রহ করে অপেক্ষা করুন।")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, support_handler))
    
    print("বটটি চলছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
