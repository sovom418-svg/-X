import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার তথ্য
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 8273597769

# ডাটা স্টোর (বট রিস্টার্ট দিলে এটি রিসেট হবে, স্থায়ী করতে চাইলে ডাটাবেস লাগবে)
# এখানে ডিফল্ট টেক্সটগুলো রাখা হয়েছে
bot_data = {
    'vpn_text': "🛡️ **Premium VPN Services:**\n\n✅ NordVPN\n✅ ExpressVPN\n✅ Surfshark\n✅ CyberGhost",
    'payment_text': "💳 **Payment System:**\n\n🔸 বিকাশ: 01642012385\n🔸 নগদ: 01788098356\n🔸 রকেট: 01642012385\n🔸 বাইন্যান্স ID: 929079815",
    'is_editing': False
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛡️ Premium VPN", callback_data='vpn'), InlineKeyboardButton("🎨 Adobe Explore", callback_data='adobe')],
        [InlineKeyboardButton("💳 Payment System", callback_data='payment')],
        [InlineKeyboardButton("📞 Contact Admin", callback_data='contact_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Trendy Tone শপে স্বাগতম!", reply_markup=reply_markup)

# অ্যাডমিন প্যানেল কমান্ড
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("📝 VPN টেক্সট পরিবর্তন", callback_data='edit_vpn')],
            [InlineKeyboardButton("📝 পেমেন্ট টেক্সট পরিবর্তন", callback_data='edit_pay')]
        ]
        await update.message.reply_text("🛠 অ্যাডমিন মোড: কোন মেনু পরিবর্তন করবেন?", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'vpn':
        await query.message.reply_text(bot_data['vpn_text'], parse_mode='Markdown')
    elif query.data == 'payment':
        await query.message.reply_text(bot_data['payment_text'], parse_mode='Markdown')
    elif query.data == 'edit_vpn' and update.effective_user.id == ADMIN_ID:
        bot_data['is_editing'] = 'vpn'
        await query.message.reply_text("নতুন VPN টেক্সটটি লিখে পাঠান:")
    elif query.data == 'edit_pay' and update.effective_user.id == ADMIN_ID:
        bot_data['is_editing'] = 'pay'
        await query.message.reply_text("নতুন পেমেন্ট ডিটেইলস লিখে পাঠান:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id == ADMIN_ID and bot_data.get('is_editing'):
        target = bot_data['is_editing']
        if target == 'vpn':
            bot_data['vpn_text'] = text
        elif target == 'pay':
            bot_data['payment_text'] = text
        
        bot_data['is_editing'] = False
        await update.message.reply_text("✅ মেনু আপডেট সফল হয়েছে!")
    else:
        # সাপোর্ট সিস্টেম (মেসেজ ফরওয়ার্ডিং)
        if user_id != ADMIN_ID:
            await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            await update.message.reply_text("📩 আপনার মেসেজ অ্যাডমিনকে পাঠানো হয়েছে।")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
