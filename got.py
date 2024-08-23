import telebot
from googletrans import Translator

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('7296559290:AAEUMr8iugnSqRbKNlrijTSTMQ2ap_5pXvk')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text
    bot.send_message(message.chat.id, translated_text)

bot.polling()