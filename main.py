import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার তথ্য এখানে দিন
BOT_TOKEN = '8315570920:AAEVbhuUhCFpJYVW8Ls-92H2VzCn1oW7Reg'
ADMIN_ID = 8273597769  # আপনার টেলিগ্রাম আইডি এখানে দিন

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"হ্যালো {user.first_name}!\n"
        "আমাদের সাপোর্ট টিমে আপনাকে স্বাগতম। আপনার যেকোনো সমস্যার কথা এখানে লিখুন, "
        "আমাদের টিম দ্রুত আপনার সাথে যোগাযোগ করবে।"
    )
    await update.message.reply_text(welcome_text)

# ইউজার মেসেজ অ্যাডমিনের কাছে পাঠানো (Support System)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id == ADMIN_ID:
        # অ্যাডমিন যদি রিপ্লাই দেয় (Reply to user)
        if update.message.reply_to_message:
            try:
                # অরিজিনাল ইউজারের আইডি টেক্সট থেকে বের করা (সহজ করার জন্য)
                # অথবা নিচের লজিক ব্যবহার করুন
                original_msg = update.message.reply_to_message
                # এখানে আমরা ধরে নিচ্ছি অ্যাডমিন ইউজারের মেসেজে রিপ্লাই দিচ্ছে
                # নোট: প্রফেশনাল বটের জন্য ডাটাবেস ব্যবহার করা ভালো
                await context.bot.send_message(
                    chat_id=original_msg.forward_from.id if original_msg.forward_from else original_msg.caption_entities[0].url.split('=')[1],
                    text=f"সাপোর্ট টিম: {update.message.text}"
                )
                await update.message.reply_text("✅ উত্তর পাঠানো হয়েছে।")
            except Exception as e:
                await update.message.reply_text("❌ উত্তর পাঠানো যায়নি। ইউজারকে সরাসরি আইডি দিয়ে মেসেজ দিন।")
    else:
        # ইউজার মেসেজ দিলে তা অ্যাডমিনকে ফরোয়ার্ড করা
        await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        await update.message.reply_text("📩 আপনার মেসেজটি আমাদের সাপোর্ট টিমের কাছে পাঠানো হয়েছে। দয়া করে অপেক্ষা করুন।")

# অ্যাডমিন প্যানেল কমান্ড
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("বট স্ট্যাটাস", callback_data='status')],
            [InlineKeyboardButton("ইউজারদের ব্রডকাস্ট করুন", callback_data='broadcast')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('🛠 অ্যাডমিন প্যানেল:', reply_markup=reply_markup)
    else:
        await update.message.reply_text("দুঃখিত, এই কমান্ডটি শুধুমাত্র অ্যাডমিনের জন্য।")

# বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'status':
        await query.edit_message_text(text="বট বর্তমানে অনলাইন আছে এবং সঠিকভাবে কাজ করছে।")

def main():
    # অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(BOT_TOKEN).build()

    # হ্যান্ডলার যোগ করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    # বট চালু করা
    print("বট চালু হচ্ছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
