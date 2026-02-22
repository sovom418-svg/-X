import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার তথ্য
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 8273597769  # আপনার এডমিন আইডি

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🛡️ Premium VPN", callback_data='vpn'), InlineKeyboardButton("🎨 Adobe Explore", callback_data='adobe')],
        [InlineKeyboardButton("📺 YouTube Premium", callback_data='youtube'), InlineKeyboardButton("🤖 ChatGPT Plus", callback_data='chatgpt')],
        [InlineKeyboardButton("💎 Gemini Pro", callback_data='gemini'), InlineKeyboardButton("💳 Payment System", callback_data='payment')],
        [InlineKeyboardButton("📞 Contact Admin", callback_data='contact_admin')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = f"হ্যালো {user.first_name}!\nTrendy Tone শপে আপনাকে স্বাগত। আমাদের সার্ভিসগুলো দেখতে নিচের বাটনগুলো ব্যবহার করুন।"
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# বাটন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'vpn':
        text = "🛡️ **Premium VPN Services:**\n\n✅ NordVPN\n✅ ExpressVPN\n✅ Surfshark\n✅ CyberGhost\n\nঅর্ডার করতে সরাসরি মেসেজ দিন।"
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'adobe':
        text = "🎨 **Adobe Explore:**\n\n🔹 ১ মাস মেয়াদী\n🔹 ৩ মাস মেয়াদী\n\nপছন্দমতো প্যাকেজটি বেছে নিয়ে আমাদের জানান।"
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'youtube':
        text = "📺 **YouTube Premium:**\n\n✅ ১ মাস মেয়াদী\n✅ ব্যাকগ্রাউন্ড প্লে ও বিজ্ঞাপনহীন।"
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'chatgpt':
        text = "🤖 **ChatGPT Plus:**\n\n✅ ১ মাস মেয়াদী - সচল (Available)\n❌ ১ বছর মেয়াদী - [SOLD OUT]"
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'gemini':
        text = "💎 **Gemini Pro:**\n\n✅ ১ মাস মেয়াদী সাবস্ক্রিপশন।"
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'payment':
        text = (
            "💳 **Payment System:**\n\n"
            "🔸 বিকাশ: 01642012385\n"
            "🔸 নগদ: 01788098356\n"
            "🔸 রকেট: 01642012385\n"
            "🔸 বাইন্যান্স ID: 929079815\n\n"
            "পেমেন্ট করার পর ট্রানজিশন আইডির স্ক্রিনশট এখানে পাঠান।"
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'contact_admin':
        await query.message.reply_text("আপনার সমস্যা বা অর্ডার সম্পর্কে এখানে লিখুন। এডমিন সরাসরি আপনার সাথে কথা বলবে।")

# সাপোর্ট ও অর্ডার ফরওয়ার্ডিং
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                # এডমিন যখন ইউজারকে উত্তর দিবে
                target_id = update.message.reply_to_message.forward_from.id
                await context.bot.send_message(chat_id=target_id, text=f"Admin: {update.message.text}")
                await update.message.reply_text("✅ ইউজারকে উত্তর পাঠানো হয়েছে।")
            except:
                await update.message.reply_text("❌ রিপ্লাই দেওয়া সম্ভব হয়নি। ইউজারের প্রাইভেসি চেক করুন।")
    else:
        # ইউজার মেসেজ দিলে সরাসরি আপনার কাছে আসবে
        await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        await update.message.reply_text("📩 আপনার মেসেজটি এডমিনের কাছে পাঠানো হয়েছে। অনুগ্রহ করে অপেক্ষা করুন।")

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing in environment variables!")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Trendy Tone Bot is Running...")
    application.run_polling()

if __name__ == '__main__':
    main()
