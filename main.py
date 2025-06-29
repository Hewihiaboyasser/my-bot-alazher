
import telebot
import json

TOKEN = '7670747634:AAHz1_yih0s8DeeiwRNIlNL2GDk9d9fdfpw'
ADMIN_ID = 1768016876

bot = telebot.TeleBot(TOKEN)

# Load data
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"الرئيسية": {}}

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# Helper function to generate buttons
def generate_buttons(menu_name):
    markup = telebot.types.InlineKeyboardMarkup()
    if menu_name in data:
        for btn, target in data[menu_name].items():
            markup.add(telebot.types.InlineKeyboardButton(text=btn, callback_data=target))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = generate_buttons("الرئيسية")
    bot.send_message(message.chat.id, "أهلاً بك في البوت التعليمي 🌟
اختر من القائمة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    if call.data in data:
        markup = generate_buttons(call.data)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text=f"📂 {call.data}:", reply_markup=markup)
    else:
        bot.send_message(chat_id, data.get(call.data, f"📄 {call.data}"))

# Add button (for admin only)
@bot.message_handler(commands=['add'])
def add_button(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ ليس لديك صلاحية.")
    msg = bot.reply_to(message, "📌 أرسل اسم القائمة (مثلاً: الرئيسية أو الدروس):")
    bot.register_next_step_handler(msg, process_menu_name)

def process_menu_name(msg):
    menu = msg.text
    msg2 = bot.reply_to(msg, "🆕 أرسل نص الزر الجديد (مثلاً: المستوى الأول):")
    bot.register_next_step_handler(msg2, lambda m: process_button_text(m, menu))

def process_button_text(msg, menu):
    button = msg.text
    msg2 = bot.reply_to(msg, "💬 أرسل المحتوى أو اسم القائمة الجديدة التي يفتحها الزر:")
    bot.register_next_step_handler(msg2, lambda m: save_button(menu, button, m.text))

def save_button(menu, button, target):
    data = load_data()
    if menu not in data:
        data[menu] = {}
    data[menu][button] = target
    save_data(data)
    bot.reply_to(msg, f"✅ تم إضافة الزر '{button}' إلى '{menu}'.")

bot.infinity_polling()
