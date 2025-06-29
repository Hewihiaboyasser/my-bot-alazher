
import telebot
from telebot import types

# توكن البوت
TOKEN = '7670747634:AAHz1_yih0s8DeeiwRNIlNL2GDk9d9fdfpw'
bot = telebot.TeleBot(TOKEN)

# آيدي الأدمن
ADMIN_ID = 1768016876

# تخزين المستخدمين والمحظورين
users = set()
banned_users = set()

# حالة البوت (شغال أو لا)
bot_active = True

# أمر /start
@bot.message_handler(commands=['start'])
# التعامل مع زر الرجوع
@bot.message_handler(func=lambda message: message.text == "رجوع ⬅️ BACK")
def go_back(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 الدروس", "☎️ تواصل معنا")
    bot.send_message(message.chat.id, "تم الرجوع إلى القائمة الرئيسية ⬅️", reply_markup=markup)
def start(message):
    global users
    if message.chat.id in banned_users:
        return
    users.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 الدروس", "📞 تواصل معنا")
    if message.chat.id == ADMIN_ID:
        markup.add("➕ إضافة زر", "📢 نشرة", "🚫 حظر", "⛔ إيقاف البوت", "✅ تشغيل البوت")
    bot.send_message(message.chat.id, "✨ أهلاً بك في البوت التعليمي", reply_markup=markup)

# التعامل مع الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global bot_active

    if message.chat.id in banned_users:
        return

    if not bot_active and message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "🚫 البوت متوقف حالياً.")
        return

    text = message.text.strip()

    if text == "📚 الدروس":
        bot.send_message(message.chat.id, "📘 اختر المستوى:\n1️⃣ المستوى الأول\n2️⃣ المستوى الثاني")

    elif text == "📞 تواصل معنا":
        bot.send_message(message.chat.id, "📧 للتواصل معنا: example@email.com")

    elif text == "➕ إضافة زر" and message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "✏️ أرسل اسم الزر الجديد:")
        bot.register_next_step_handler(msg, add_button)

    elif text == "📢 نشرة" and message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "✍️ أرسل محتوى النشرة:")
        bot.register_next_step_handler(msg, broadcast)

    elif text == "🚫 حظر" and message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "🔒 أرسل ID المستخدم الذي تريد حظره:")
        bot.register_next_step_handler(msg, ban_user)

    elif text == "⛔ إيقاف البوت" and message.chat.id == ADMIN_ID:
        bot_active = False
        bot.send_message(message.chat.id, "⛔ تم إيقاف البوت.")

    elif text == "✅ تشغيل البوت" and message.chat.id == ADMIN_ID:
        bot_active = True
        bot.send_message(message.chat.id, "✅ تم تفعيل البوت.")

# إضافة زر ديناميكي
def add_button(message):
    new_btn = message.text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 الدروس", "📞 تواصل معنا", new_btn)
    markup.add("🔙 رجوع")
    bot.send_message(message.chat.id, f"✅ تم إضافة الزر: {new_btn}", reply_markup=markup)

# إرسال نشرة جماعية
def broadcast(message):
    text = message.text
    success = 0
    fail = 0
    for user in users:
        try:
            bot.send_message(user, f"📢 {text}")
            success += 1
        except:
            fail += 1
    bot.send_message(message.chat.id, f"📬 تم الإرسال إلى {success} عضو (فشل إلى {fail})")

# حظر مستخدم
def ban_user(message):
    try:
        user_id = int(message.text.strip())
        banned_users.add(user_id)
        bot.send_message(message.chat.id, f"🚫 تم حظر العضو: {user_id}")
    except:
        bot.send_message(message.chat.id, "❌ المعرف غير صحيح.")

# تشغيل البوت
print("✅ البوت يعمل الآن...")
bot.infinity_polling()
