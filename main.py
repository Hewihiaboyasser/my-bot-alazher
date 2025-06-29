
import telebot
from telebot import types
import json
import os

# التوكن الخاص بالبوت
TOKEN = '7850057458:AAGs-sL_rvj4ntvzVLCmN-GdqG1Qw5AS0po'
bot = telebot.TeleBot(TOKEN)

# معرف الأدمن (Telegram user ID)
ADMIN_ID = 1768016876

# ملفات البيانات
MENU_FILE = 'menu.json'
USERS_FILE = 'users.json'
BANNED_FILE = 'banned.json'

# تحميل البيانات من الملفات
def load_data(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

# حفظ البيانات إلى الملفات
def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# تحميل القوائم والمستخدمين والحظر
menu = load_data(MENU_FILE, {})
users = load_data(USERS_FILE, [])
banned = load_data(BANNED_FILE, [])

# حالة البوت
bot_active = True

# عرض قائمة حسب المسار
def build_menu(path):
    parts = path.strip().split('/')
    current = menu
    for part in parts:
        if part in current:
            current = current[part]
        else:
            return types.InlineKeyboardMarkup(), {}
    markup = types.InlineKeyboardMarkup()
    for key in current:
        markup.add(types.InlineKeyboardButton(key, callback_data=path + '/' + key))
    if path != '':
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data='/'.join(parts[:-1])))
    return markup, current

# أمر /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in banned:
        return
    if message.chat.id not in users:
        users.append(message.chat.id)
        save_data(USERS_FILE, users)
    markup, _ = build_menu('')
    bot.send_message(message.chat.id, "✨ مرحبًا بك في البوت التعليمي", reply_markup=markup)

# التعامل مع الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.message.chat.id in banned:
        return
    path = call.data
    markup, _ = build_menu(path)
    bot.edit_message_text(f"📂 القائمة: {path or 'الرئيسية'}", call.message.chat.id, call.message.message_id, reply_markup=markup)

# إضافة زر
@bot.message_handler(commands=['add'])
def add_button(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "📍 أرسل المسار الذي تريد الإضافة فيه (مثال: الدروس 📚/المستوى الأول 🧱):")
    bot.register_next_step_handler(message, get_add_path)

def get_add_path(message):
    path = message.text.strip()
    bot.send_message(message.chat.id, "📝 أرسل اسم الزر الجديد:")
    bot.register_next_step_handler(message, lambda m: finish_add(path, m))

def finish_add(path, message):
    name = message.text.strip()
    parts = path.strip().split('/')
    current = menu
    for part in parts:
        current = current.setdefault(part, {})
    current[name] = {}
    save_data(MENU_FILE, menu)
    bot.send_message(message.chat.id, f"✅ تم إضافة الزر '{name}' إلى '{path}'.")

# إرسال نشرة
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "✍️ أرسل الرسالة التي تريد إرسالها للجميع:")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    count = 0
    for user in users:
        try:
            bot.send_message(user, f"📢 {message.text}")
            count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"📬 تم إرسال النشرة إلى {count} عضو.")

# حظر عضو
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "🚫 أرسل ID العضو الذي تريد حظره:")
    bot.register_next_step_handler(message, finish_ban)

def finish_ban(message):
    try:
        uid = int(message.text.strip())
        if uid not in banned:
            banned.append(uid)
            save_data(BANNED_FILE, banned)
            bot.send_message(message.chat.id, f"🚫 تم حظر العضو {uid}")
    except:
        bot.send_message(message.chat.id, "❌ خطأ في ID")

# فك الحظر
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "✅ أرسل ID العضو لفك الحظر:")
    bot.register_next_step_handler(message, finish_unban)

def finish_unban(message):
    try:
        uid = int(message.text.strip())
        if uid in banned:
            banned.remove(uid)
            save_data(BANNED_FILE, banned)
            bot.send_message(message.chat.id, f"✅ تم فك الحظر عن العضو {uid}")
    except:
        bot.send_message(message.chat.id, "❌ خطأ في ID")

# عدد المستخدمين
@bot.message_handler(commands=['users'])
def count_users(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👥 عدد الأعضاء: {len(users)}")

# إيقاف وتشغيل البوت
@bot.message_handler(commands=['stopbot'])
def stop_bot(message):
    global bot_active
    if message.chat.id == ADMIN_ID:
        bot_active = False
        bot.send_message(message.chat.id, "⛔ تم إيقاف البوت.")

@bot.message_handler(commands=['startbot'])
def start_bot(message):
    global bot_active
    if message.chat.id == ADMIN_ID:
        bot_active = True
        bot.send_message(message.chat.id, "✅ تم تشغيل البوت.")

# بدء التشغيل
print("✅ البوت يعمل الآن...")
bot.infinity_polling() 
