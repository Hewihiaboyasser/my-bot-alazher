import telebot
from telebot import types
import json

# التوكن الخاص فيك
TOKEN = '7670747634:AAHz1_yih0s8DeeiwRNIlNL2GDk9d9fdfpw'
# معرف الأدمن (اختياري)
ADMIN_ID = 1768016876

bot = telebot.TeleBot(TOKEN)

# تحميل البيانات من ملف JSON
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"الرئيسية": {}}

# حفظ البيانات
def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📚 الدروس", "📞 تواصل معنا")
    bot.send_message(message.chat.id, "🌟 أهلاً بك في البوت التعليمي", reply_markup=markup)

# الرد على الأزرار
@bot.message_handler(func=lambda message: True)
def reply_buttons(message):
    if message.text == "📚 الدروس":
        bot.send_message(message.chat.id, "📘 يرجى اختيار المستوى:\n1️⃣ المستوى الأول\n2️⃣ المستوى الثاني")
    elif message.text == "📞 تواصل معنا":
        bot.send_message(message.chat.id, "للتواصل معنا: example@email.com")
    elif message.text == "1️⃣ المستوى الأول":
        bot.send_message(message.chat.id, "📖 هذا المحتوى الخاص بالمستوى الأول.")
    elif message.text == "2️⃣ المستوى الثاني":
        bot.send_message(message.chat.id, "📖 هذا المحتوى الخاص بالمستوى الثاني.")
    else:
        bot.send_message(message.chat.id, "❓ لم أفهم رسالتك، الرجاء استخدام الأزرار.")

# تشغيل البوت
bot.polling(none_stop=True)
