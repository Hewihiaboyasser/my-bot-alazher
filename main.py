import telebot
from telebot import types

# توكن البوت
TOKEN = '7670747634:AAHz1_yih0s8DeeiwRNIlNL2GDk9d9fdfpw'
bot = telebot.TeleBot(TOKEN)

# آيدي الأدمن
ADMIN_ID = 1768016876

# قائمة الأعضاء (لتجربة النشرة)
users = set()

# حالة البوت (مفعل/معطل)
bot_active = True

# استقبال /start
@bot.message_handler(commands=['start'])
def start(message):
    global users
    users.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 الدروس", "☎️ تواصل معنا")
    if message.from_user.id == ADMIN_ID:
        markup.add("⚙️ لوحة التحكم")
    bot.send_message(message.chat.id, "🌟 أهلاً بك في البوت التعليمي", reply_markup=markup)

# استقبال الأوامر من الجميع
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    global bot_active
    if not bot_active and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ البوت متوقف حالياً.")
        return

    if message.text == "📚 الدروس":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📘 المستوى الأول", "📙 المستوى الثاني")
        markup.add("🔙 رجوع")
        bot.send_message(message.chat.id, "يرجى اختيار المستوى:", reply_markup=markup)

    elif message.text == "📘 المستوى الأول":
        bot.send_message(message.chat.id, "📘 هنا محتوى المستوى الأول.")

    elif message.text == "📙 المستوى الثاني":
        bot.send_message(message.chat.id, "📙 هنا محتوى المستوى الثاني.")

    elif message.text == "📞 تواصل معنا":
        bot.send_message(message.chat.id, "للتواصل معنا: example@email.com")

    elif message.text == "🔙 رجوع":
        start(message)

    elif message.text == "⚙️ لوحة التحكم" and message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ إضافة زر", "📢 إرسال نشرة")
        markup.add("🚫 حظر عضو", "🔁 إيقاف / تشغيل البوت")
        markup.add("🔙 رجوع")
        bot.send_message(message.chat.id, "لوحة التحكم:", reply_markup=markup)

    elif message.text == "➕ إضافة زر" and message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "أرسل اسم الزر الجديد:")

        @bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
        def add_btn(msg):
            btn = msg.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(btn, "🔙 رجوع")
            bot.send_message(msg.chat.id, f"✅ تم إضافة الزر: {btn}", reply_markup=markup)

    elif message.text == "📢 إرسال نشرة" and message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "✏️ أرسل محتوى النشرة الآن:")

        @bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
        def broadcast(msg):
            for user in users:
                try:
                    bot.send_message(user, msg.text)
                except:
                    pass
            bot.send_message(msg.chat.id, "✅ تم إرسال النشرة.")

    elif message.text == "🚫 حظر عضو" and message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🔒 أرسل ID العضو المراد حظره:")

        @bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
        def block_user(msg):
            uid = int(msg.text)
            if uid in users:
                users.remove(uid)
                bot.send_message(msg.chat.id, f"🚫 تم حظر العضو {uid}")
            else:
                bot.send_message(msg.chat.id, "هذا العضو غير موجود في القائمة.")

    elif message.text == "🔁 إيقاف / تشغيل البوت" and message.from_user.id == ADMIN_ID:
        bot_active = not bot_active
        status = "✅ مفعل" if bot_active else "⛔ متوقف"
        bot.send_message(message.chat.id, f"حالة البوت الآن: {status}")

# تشغيل البوت
print("✅ البوت يعمل الآن...")
bot.infinity_polling()
