print("✅ Telegram Bot Admin Panel (Arabic)")

import telebot from telebot import types import json

TOKEN = '7670747634:AAHz1_yih0s8DeeiwRNIlNL2GDk9d9fdfpw' ADMIN_ID = 1768016876  # ضع رقم الأدمين هنا bot = telebot.TeleBot(TOKEN)

➕ حالة البوت

bot_enabled = True

➕ قاعدة بيانات محلية

try: with open('users.json', 'r', encoding='utf-8') as f: users = json.load(f) except: users = {"members": [], "blocked": []}

➕ حفظ البيانات

def save_users(): with open('users.json', 'w', encoding='utf-8') as f: json.dump(users, f, ensure_ascii=False)

➕ /start

@bot.message_handler(commands=['start']) def start(message): if message.chat.id not in users['members'] and message.chat.id != ADMIN_ID: users['members'].append(message.chat.id) save_users()

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add('📚 الدروس', '📞 تواصل معنا')
if message.chat.id == ADMIN_ID:
    markup.add('🛠 الإدارة')

bot.send_message(message.chat.id, '👋 أهلاً بك في البوت التعليمي', reply_markup=markup)

➕ رسائل المستخدم

@bot.message_handler(func=lambda m: True) def handle_all(message): global bot_enabled if message.chat.id in users['blocked'] and message.chat.id != ADMIN_ID: return

if not bot_enabled and message.chat.id != ADMIN_ID:
    bot.send_message(message.chat.id, '🚫 البوت متوقف حالياً.')
    return

if message.text == '📚 الدروس':
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📘 المستوى الأول', '📗 المستوى الثاني')
    markup.add('🔙 رجوع')
    bot.send_message(message.chat.id, 'يرجى اختيار المستوى:', reply_markup=markup)

elif message.text in ['📘 المستوى الأول', '📗 المستوى الثاني']:
    bot.send_message(message.chat.id, f'🔍 جاري عرض محتوى {message.text}')

elif message.text == '📞 تواصل معنا':
    bot.send_message(message.chat.id, '📧 للتواصل معنا: example@email.com')

elif message.text == '🔙 رجوع':
    start(message)

elif message.text == '🛠 الإدارة' and message.chat.id == ADMIN_ID:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('➕ إضافة زر', '📢 نشرة جماعية')
    markup.add('🚫 حظر عضو', '✅ إلغاء الحظر')
    markup.add('🔴 إيقاف البوت', '🟢 تشغيل البوت')
    markup.add('🔙 رجوع')
    bot.send_message(message.chat.id, '🎛 لوحة التحكم:', reply_markup=markup)

elif message.text == '📢 نشرة جماعية' and message.chat.id == ADMIN_ID:
    bot.send_message(message.chat.id, '✍️ أرسل الرسالة الآن وسيتم إرسالها للجميع.')
    bot.register_next_step_handler(message, broadcast)

elif message.text == '➕ إضافة زر' and message.chat.id == ADMIN_ID:
    bot.send_message(message.chat.id, '✍️ أرسل اسم الزر الجديد:')
    bot.register_next_step_handler(message, add_custom_button)

elif message.text == '🚫 حظر عضو' and message.chat.id == ADMIN_ID:
    bot.send_message(message.chat.id, '📌 أرسل ID العضو لحظره:')
    bot.register_next_step_handler(message, block_user)

elif message.text == '✅ إلغاء الحظر' and message.chat.id == ADMIN_ID:
    bot.send_message(message.chat.id, '📌 أرسل ID العضو لإلغاء الحظر:')
    bot.register_next_step_handler(message, unblock_user)

elif message.text == '🔴 إيقاف البوت' and message.chat.id == ADMIN_ID:
    bot_enabled = False
    bot.send_message(message.chat.id, '🚫 تم إيقاف البوت.')

elif message.text == '🟢 تشغيل البوت' and message.chat.id == ADMIN_ID:
    bot_enabled = True
    bot.send_message(message.chat.id, '✅ تم تشغيل البوت.')

➕ وظائف الإدارة

def broadcast(message): for user_id in users['members']: try: bot.send_message(user_id, f'📢 {message.text}') except: pass bot.send_message(message.chat.id, '✅ تم إرسال الرسالة للجميع.')

def block_user(message): try: uid = int(message.text) if uid not in users['blocked']: users['blocked'].append(uid) save_users() bot.send_message(message.chat.id, '🚫 تم حظر العضو.') except: bot.send_message(message.chat.id, '❌ فشل في الحظر.')

def unblock_user(message): try: uid = int(message.text) if uid in users['blocked']: users['blocked'].remove(uid) save_users() bot.send_message(message.chat.id, '✅ تم إلغاء الحظر.') except: bot.send_message(message.chat.id, '❌ فشل في إلغاء الحظر.')

def add_custom_button(message): label = message.text markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.add(label, '🔙 رجوع') bot.send_message(message.chat.id, f'✅ تم إضافة الزر: {label}', reply_markup=markup)

print('✅ Bot is running...') bot.polling(none_stop=True)

