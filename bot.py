
import os
import telebot
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN"
ADMIN_ID = int(os.getenv("ADMIN_ID") or 7525798243)

bot = telebot.TeleBot(BOT_TOKEN)

# Load VPN stock from Excel
def load_stock():
    try:
        df = pd.read_excel("vpn_stock.xlsx")
        return df.to_dict(orient="records")
    except:
        return []

vpn_stock = load_stock()

@bot.message_handler(commands=["start"])
def start(msg):
    text ="👋 স্বাগতম VPN দোকানে! নিচের অপশন থেকে একটি নির্বাচন করুন।"

"
    for vpn in set([v['VPN Name'] for v in vpn_stock]):
        text += f"🔹 {vpn}
"
    text += "
VPN নিতে চাইলে /buy লিখুন।"
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["buy"])
def buy(msg):
    text = "💳 VPN নিতে হলে টাকা পাঠান:

"
    text += "📱 Bkash/Nagad: 01747126892
"
    text += "💬 টাকা পাঠিয়ে 'আমি টাকা পাঠিয়েছি' লিখুন।"
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["confirm"])
def confirm(msg):
    if msg.from_user.id != ADMIN_ID:
        bot.send_message(msg.chat.id, "⛔️ শুধু Admin এই কমান্ড ব্যবহার করতে পারে।")
        return
    try:
        parts = msg.text.split()
        user_id = int(parts[1])
        if vpn_stock:
            acc = vpn_stock.pop(0)
            bot.send_message(user_id, f"✅ আপনার VPN অ্যাকাউন্ট:
📧 {acc['Email']}
🔑 {acc['Password']}")
            bot.send_message(msg.chat.id, "✅ ইউজারকে VPN পাঠানো হয়েছে।")
        else:
            bot.send_message(msg.chat.id, "⚠️ আর কোন VPN stock নাই।")
    except:
        bot.send_message(msg.chat.id, "❌ confirm <user_id> format e command dao.")

bot.polling()
