import os
import telebot
import requests

# ✅ Directly set your API key and Telegram token
BOT_TOKEN = "8074828538:AAFvAf6XItWMKAJSVMSSbKtI5-mIKUU9OS4"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hi Vivek! 🤖 I’m your AI English helper.\nSend me a sentence and I’ll correct your grammar.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    original = message.text
    prompt = f"Correct the grammar and punctuation:\n\n{original}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://openrouter.ai/",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = res.json()
        fixed = result["choices"][0]["message"]["content"]
        bot.reply_to(message, f"✅ Corrected:\n{fixed}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
