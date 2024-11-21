import os
import telebot
from anthropic import Anthropic

# Инициализация клиентов
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
claude_client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот на основе Claude.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

def main():
    bot.delete_webhook()
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()

