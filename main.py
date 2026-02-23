    import telebot
from telebot import types

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton("🛒 Buy VPN")
    item2 = types.KeyboardButton("📂 My Orders")
    item3 = types.KeyboardButton("📞 Support")
    
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Welcome to Secure Surf Zone!", reply_markup=markup)

bot.polling()
